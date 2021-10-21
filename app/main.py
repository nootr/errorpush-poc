#!/usr/bin/env python3

"""Errorpush/rollbar PoC

This proof-of-concept uses the rollbar library to send messages to an errorpush
instance.
"""

import os
import logging
import rollbar

from flask import Flask


ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ROLLBAR_ENDPOINT = os.environ.get("ROLLBAR_ENDPOINT")


app = Flask(__name__)

rollbar.init(ACCESS_TOKEN, "app", endpoint=ROLLBAR_ENDPOINT)


class LogHandler(logging.Handler):
    def emit(self, record):
        rollbar.report_message(record.msg, level=record.levelname.lower())


logger = logging.getLogger(__name__)
logger.addHandler(LogHandler())


@app.route('/')
def home():
    levels = {"error", "warning", "info"}
    links = [f"<p><a href=\"/{level}\">{level}</a></p>" for level in levels]
    return ''.join(links)


@app.route('/error')
def error():
    logger.error("This is an error")
    return "An error has been sent!"


@app.route('/warning')
def warning():
    logger.warning("This is a warning")
    return "A warning has been sent!"


@app.route('/info')
def info():
    logger.info("This is info")
    return "Info has been sent!"


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8080,
    )
