#!/usr/bin/env python

from wsgiref.simple_server import make_server

from my_wsgi_framework.framework import Application
from fronts import fronts
from pages import pages
from settings import PORT


app = Application(pages, fronts)


with make_server('', PORT, app) as httpd:
    print(f"Запуск на порту {PORT}...")
    httpd.serve_forever()
