from django.urls import path

from .views import home, post_detail, product_search


urlpatterns = [
    path("", home, name="home"),
    path("search/", product_search, name="product_search"),
    path("blog/<slug:slug>/", post_detail, name="post_detail"),
]


