import logging
from datetime import datetime
from settings import TEMPLATES_FOLDER


logging.basicConfig()
request_log = logging.getLogger("request")
request_log.addHandler(logging.FileHandler("logs/request.log"))


def request_log_front(request):
    request_log.info(f"{datetime.now()} :: {str(request)}")


def static(request):
    request["static"] = TEMPLATES_FOLDER


fronts = [request_log_front, static]
