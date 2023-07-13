from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("createlisting/", views.createlisting, name="createlisting"),
    path("closedlistings/", views.closedlistings, name="closedlistings"),
    path("listings/<str:name>/", views.getlisting, name="getlisting"),
    path("listings/<str:name>/placebid/", views.placebid, name="placebid"),
    path("listings/<str:name>/closelisting/", views.closelisting, name="closelisting"),
    path("listings/<str:name>/comment/", views.comment, name="comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category_type>/", views.category, name="category")
]
