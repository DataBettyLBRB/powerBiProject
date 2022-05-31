from operator import contains
from unicodedata import name
import pyautogui
import time

from pywebio.platform.flask import webio_view
from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from flask import Flask

import argparse

app = Flask(__name__)


def get_coordinates(images):
    return pyautogui.locateOnScreen(images, confidence=0.9)


def click_coordinates(coordinates):
    put_text(coordinates)
    return pyautogui.click(coordinates)


def press_key(key):
    return pyautogui.press(key)


def main():
    refresh_button = "refresh.png"
    publish_button = "publish.png"

    refresh_location = get_coordinates(refresh_button)
    publish_location = get_coordinates(publish_button)

    # place the checkboxes on main page
    checkboxes = checkbox("Check", options=["Refresh Button", "Publish Button", "Run Program"])

    for cb in checkboxes:
        # if refresh checked, get coordinates refresh location
        if "Refresh" in cb:
            put_text(refresh_location)
        elif "Publish" in cb:
            put_text(publish_location)
        else:
            click_coordinates(refresh_location)
            time.sleep(2)
            click_coordinates(publish_location)
            press_key('enter')


app.add_url_rule('/', 'webio_view', webio_view(main),
                 methods=['GET', 'POST', 'OPTIONS'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port, auto_open_webbrowser=True)