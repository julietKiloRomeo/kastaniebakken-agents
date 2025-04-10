from selenium import webdriver

import time
import json
import html
import html2text
import os

import dotenv
dotenv.load_dotenv()

from datetime import date, timedelta

def current_or_coming_week():

    target_date = date.today()

    # Check if it's weekend (Saturday or Sunday)
    is_weekend = target_date.isoweekday() >= 6   # Saturday=6, Sunday=7
    look_at_next_week_instead = is_weekend
    if look_at_next_week_instead:
        target_date += timedelta(days=7)

    # Get ISO calendar week and year
    week_number = target_date.isocalendar()[1]
    year = target_date.isocalendar()[0]
    
    return dict(week=week_number, year=year)



def login(driver):
    name_input_path = '//*[@id="UserName"]'
    name_input = driver.find_element('xpath', name_input_path)
    name_input.send_keys(os.environ["FI_USER"])
    time.sleep(0.1)

    pass_input_path = '//*[@id="Password"]'
    pass_input = driver.find_element('xpath', pass_input_path)
    pass_input.send_keys(os.environ["FI_PASS"])
    time.sleep(0.1)

    submit_path = "//input[@type='submit' and @value='Login']"
    submit = driver.find_element('xpath', submit_path)

    submit.click()
    time.sleep(0.1)


def read_schedule_json(driver):
    time.sleep(0.2)
    root_element = driver.find_element("id", "root")
    
    time.sleep(0.2)
    # Get the JSON string from the custom data attribute
    json_str = root_element.get_attribute("data-clientlogic-settings-weeklyplansapp")
    
    # Optionally, if you need to unescape HTML entities (Selenium might return it decoded already)
    
    json_str = html.unescape(json_str)
    
    # Parse the JSON string into a Python dictionary
    return json.loads(json_str)

def add_section(plan, section):
    return f"""{plan}
    
{section}"""

def format_schedule(schedule):
    plan = ""
    
    general = schedule['SelectedPlan']['GeneralPlan']['LessonPlans'][0]['Content']
    plan = add_section(plan, general)
    
    for day in schedule['SelectedPlan']['DailyPlans']:
        plan = add_section(plan, "## "+day["Day"] + "<br>")
    
        for lesson in day["LessonPlans"]:
            plan = add_section(plan, "### "+lesson["Subject"]["Title"])
            plan = add_section(plan, lesson["Content"])


    # Optional: unescape HTML entities (Selenium, for instance, might already provide decoded HTML)
    clean_html = html.unescape(plan)
    
    # Convert HTML to Markdown
    markdown_converter = html2text.HTML2Text()
    markdown_converter.body_width = 0  # Disable line wrapping
    return markdown_converter.handle(clean_html)


def read_the_schedule():
    """schedule = read_the_schedule()
    """

    url = f"""http://{os.environ["SELENIUM_HOST"]}:{os.environ["SELENIUM_PORT"]}"""
    driver = webdriver.Remote(
        command_executor=url,
        options = webdriver.ChromeOptions(),    
    )


    week_and_year = current_or_coming_week()
    week = week_and_year["week"]
    year = week_and_year["year"]
    week_url = f"https://birkerodprivatskole.m.skoleintra.dk/parent/3057/Alvildeitem/weeklyplansandhomework/item/class/{week}-{year}"
    
    driver.get(week_url)
    driver.implicitly_wait(30)
    
    login(driver)
    
    for i in range(5):
        try:
            schedule = read_schedule_json(driver)
            print(f"Done after {i+1} tries!")
            break
        except:
            time.sleep(0.2)

#    driver.close()
            
    return format_schedule(schedule)




