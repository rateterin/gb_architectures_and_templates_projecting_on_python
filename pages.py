from views import HomeView, AboutView, ContactsView


pages = {
    "/": HomeView(),
    "/about": AboutView(),
    "/contacts": ContactsView(),
}
