from my_wsgi_framework.framework import render


class HomeView():
    def __call__(self, request):
        return "200 OK", render("home.html")


class AboutView():
    def __call__(self, request):
        return "200 OK", render("about.html")


class ContactsView():
    def __call__(self, request):
        return "200 OK", render("contacts.html")
