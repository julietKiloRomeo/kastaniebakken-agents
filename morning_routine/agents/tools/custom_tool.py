from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure Chrome options for headless mode
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode0
#chrome_options.add_argument("--disable-gpu")  # Optional: disable GPU acceleration
#chrome_options.add_argument("--window-size=1920,1080")  # Optional: set window size

import time
import json
import html

import dotenv
dotenv.load_dotenv()

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
        plan = add_section(plan, "## "+day["Day"])
    
        for lesson in day["LessonPlans"]:
            plan = add_section(plan, "### "+lesson["Subject"]["Title"])
            plan = add_section(plan, lesson["Content"])
    return plan


def read_the_schedule():
    # Initialize the Chrome driver with these options
    url = f"""http://{os.environ["SELENIUM_HOST"]}:{os.environ["SELENIUM_PORT"]}"""
    driver = webdriver.Remote(
        command_executor=url,
        options = webdriver.ChromeOptions(),    
    )
    
    week_url = "https://birkerodprivatskole.m.skoleintra.dk/parent/3057/Alvildeitem/weeklyplansandhomework/item/class/{week}-{year}"
    
    driver.get(week_url.format(week=14, year=2025))
    driver.implicitly_wait(30)
    
    login(driver)
    
    for i in range(5):
        try:
            schedule = read_schedule_json(driver)
            print(f"Done after {i+1} tries!")
            break
        except:
            time.sleep(0.2)
            
    return format_schedule(schedule)







class FIToolInput(BaseModel):
    """Input schema for FICustomTool."""
    argument: str = Field(..., description="the name of the student to find the schedule for") # this is a lie :)

class FITool(BaseTool):
    name: str = "Intra tool"
    description: str = (
        "Read the weekly schedule from forældreintra"
    )
    args_schema: Type[BaseModel] = FIToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return read_the_schedule()
