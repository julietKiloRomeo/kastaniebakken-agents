#!/usr/bin/env python
import warnings


from morning_routine.agents.crew import MorningRoutine
from morning_routine import scraper

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

schedule = scraper.read_the_schedule()

week = 15
for weekday in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
    inputs = {
        "schedule":schedule,
        "weekday":weekday,
        "week":week,
    }
    result = MorningRoutine().crew().kickoff(inputs=inputs)
    print("- "*30)
    print(weekday)
    print(result)
