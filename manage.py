# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import logging

from app.app import App

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.ini')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')


def run():
    logging.basicConfig(level=LOG_LEVEL)

    app = App(CONFIG_FILE)
    app.init()
    app.run()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()
