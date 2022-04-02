from django.urls import path

from .views import (
    IndexView,
    PostDetailView,
    CategoryPostView,
    SubCategoryPostView,
)

# ここでapp_nameを指定すると、{% url %}テンプレートタグ使用時に
# URLパターン名の頭にアプリケーションの名前空間をつけて:で区切る
app_name = "blog"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("post/<str:slug>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "category/<str:category_slug>/",
        CategoryPostView.as_view(),
        name="category_post",
    ),
    path(
        "category/<str:category_slug>/<str:sub_category_slug>/",
        SubCategoryPostView.as_view(),
        name="sub_category_post",
    ),
]
