#!/usr/bin/env python3

"""Errorpush/rollbar PoC

This proof-of-concept uses the rollbar library to send messages to an errorpush
instance.
"""

import logging
import rollbar

from flask import Flask


class LogHandler(logging.Handler):
    def emit(self, record):
        rollbar.report_message(record.msg, level=record.levelname.lower())

logger = logging.getLogger(__name__)
logger.addHandler(LogHandler())


app = Flask(__name__)


@app.before_first_request
def init_rollbar():
    access_token = "foobarbaz"
    environment = "app"
    rollbar.init(access_token, environment, endpoint="http://errorpush:5000/")


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
