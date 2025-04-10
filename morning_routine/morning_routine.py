"""Welcome to Reflex! This file outlines the steps to create a basic app."""
import reflex as rx
import os
from rxconfig import config
import pathlib
from typing import List
# Define weekday order globally for easy reference
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

WEEKDAY_ORDER = {
    "monday":0, 
    "tuesday":1, 
    "wednesday":2, 
    "thursday":3, 
    "friday":4, 
    "saturday":5, 
    "sunday":6, 
}

class State(rx.State):
    """The app state."""
    weekday_content: dict = {"Monday":""}
    available_weekdays: List[str] = ["Monday"]
    
    def load_markdown_files(self):
        """Load all markdown files from the crew_output directory."""
        self.weekday_content = {}
        self.available_weekdays = []
        
        # Path to the markdown files
        directory = "crew_output"
        
        # Check if directory exists
        if not os.path.exists(directory):
            raise Exception(f"we are at {os.pwd}")
        print("--------------")
        
        # Read all markdown files
        for filename in pathlib.Path('./crew_output').glob("*.md"):
            # Extract weekday from filename (assuming format: week-XX-Weekday.md)
            parts = filename.name.split('-')
            if len(parts) >= 3:
                weekday = parts[2].replace('.md', '')
                
                # Read file content
                with filename.open('r') as file:
                    content = file.read()
                
                # Store content with weekday as key
                self.weekday_content[weekday] = content
                self.available_weekdays.append(weekday)
        
        # Sort available weekdays by their natural order
        self.available_weekdays = sorted(self.available_weekdays, key=lambda day: WEEKDAY_ORDER.get(day.lower(), 10))
            
    def on_mount(self):
        """Load markdown files when app starts."""
        self.load_markdown_files()

def weekday_tab(weekday: str) -> rx.Component:
    """Create a tab for a specific weekday."""
    return rx.tabs.content(
        rx.container(
            rx.color_mode.button(position="top-right"),
            rx.vstack(
                rx.markdown(State.weekday_content[weekday]),
                spacing="5",
                justify="center",
                min_height="85vh",
            ),
        ),
        value=weekday,
    )

def index() -> rx.Component:
    """The main page of the app."""
    return rx.cond(
        State.available_weekdays,  # Check if we have any available weekdays
        rx.tabs.root(
            rx.tabs.list(
                rx.foreach(
                    State.available_weekdays,
                    lambda day: rx.tabs.trigger(day, value=day),
                )
            ),
            rx.foreach(
                State.available_weekdays,
                lambda day: weekday_tab(day),
            ),
            default_value="Monday",
            on_mount=State.on_mount,
        ),
        rx.text(f"No weekday data found. Please check the crew_output directory. {pathlib.Path('./crew_output').resolve()}"),
    )

# Initialize and setup the app
app = rx.App()
app.add_page(index)