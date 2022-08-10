import settings

from quopri import decodestring
from jinja2 import Environment, FileSystemLoader


def render(template_name, folder=None, **kwargs):
    if not folder:
        folder = settings.TEMPLATES_FOLDER
    env = Environment(loader=FileSystemLoader(folder))
    template = env.get_template(template_name)
    return template.render(**kwargs)


class NotFound404:
    def __call__(self, request):
        return "404 NOT FOUND", "404 Requested Page Not Fount"


class Application:
    def __init__(self, pages, fronts):
        self.pages = pages
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ["PATH_INFO"]
        # pprint(environ)
        if path in self.pages:
            view = self.pages[path]
        else:
            view = NotFound404()
        request = {}
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
