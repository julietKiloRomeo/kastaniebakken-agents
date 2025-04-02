"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from morning_routine import scraper

import os


class State(rx.State):
    """The app state."""

    schedule: str= "## Not scraped yet..."

    def scrape(self):
        self.schedule = scraper.read_the_schedule()


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.markdown(State.schedule),
            rx.button("Scrape", on_click=State.scrape),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)
