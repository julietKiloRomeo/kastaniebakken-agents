#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from morning_routine.crew import MorningRoutine

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

inputs = {
    'topic': 'AI LLMs',
    'current_year': str(datetime.now().year)
}


result = MorningRoutine().crew().kickoff(inputs=inputs)

print(result)
