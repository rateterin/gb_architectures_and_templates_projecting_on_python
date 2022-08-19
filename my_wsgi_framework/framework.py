import settings

from quopri import decodestring
from jinja2 import Environment, FileSystemLoader
from pprint import pprint


def render(template_name, folder=None, **kwargs):
    if not folder:
        folder = settings.TEMPLATES_FOLDER
    env = Environment(loader=FileSystemLoader(folder))
    template = env.get_template(template_name)
    return template.render(**kwargs)


def parse_params_from_data(data: str) -> dict:
    result_dict = {}
    if not data:
        return {}
    data = data.split("&")
    result_dict = {k: v for (k, v) in [el.split("=") for el in data]}
    return result_dict


def get_params_from_get(env):
    query_string = env.get("QUERY_STRING")
    result = parse_params_from_data(query_string)
    return result


def get_params_from_post(env):
    data_length = env.get("CONTENT_LENGTH")
    data_length = int(data_length) if data_length else 0
    data = env.get("wsgi.input").read(data_length) if data_length > 0 else b""
    result = parse_params_from_data(data.decode(encoding="utf-8"))
    return result


def do_with_post(params):
    if "internal" in params.keys():
        if params["internal"] == "cont_page_msg":
            sender = params["email"]
            message = params["message"]
            print("---Сообщение---")
            print(f"Отправитель: {sender}")
            pprint(message)


class NotFound404:
    def __call__(self, request):
        return "404 NOT FOUND", "404 Requested Page Not Fount"


class Application:
    def __init__(self, pages, fronts):
        self.pages = pages
        self.fronts = fronts

    def __call__(self, environ, start_response):
        method = environ.get("REQUEST_METHOD")
        if method == "POST":
            params = get_params_from_post(environ)
            params = self.decode_value(params)
            do_with_post(params)
        if method == "GET":
            params = get_params_from_get(environ)
            params = self.decode_value(params)

        path = environ.get("PATH_INFO")
        if path in self.pages:
            view = self.pages[path]
        else:
            view = NotFound404()
        request = {}
        request["params"] = params
        for front in self.fronts:
            front(request)
        status_code, body = view(request)
        start_response(status_code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
