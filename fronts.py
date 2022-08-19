import logging
import os
from datetime import datetime
from settings import TEMPLATES_FOLDER


if not os.path.isdir("logs"):
    os.mkdir("logs")

logging.basicConfig()
request_log = logging.getLogger("request")
request_log.setLevel(logging.INFO)
request_log.addHandler(logging.FileHandler("logs/request.log"))


def request_log_front(request):
    request_log.info(f"{datetime.now()} :: {request}")


def static(request):
    request["static"] = TEMPLATES_FOLDER


fronts = [request_log_front, static]
