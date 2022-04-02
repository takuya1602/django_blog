from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import re

from .models import Post, Category, SubCategory


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = super().get_object()
        content_length = len(re.sub(r"<[^>]*?>", "", obj.content))
        context["article_length"] = content_length
        context["read_time"] = int(content_length) / 400
        context["headings"] = re.findall(r"<h(\d)\s*.*?>(.*?)</h\d>", obj.content)
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.is_public and not self.request.user.is_authenticated:
            raise Http404
        return obj


class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"


class CategoryPostView(ListView):
    model = Post
    template_name = "blog/category_post.html"

    def get_queryset(self):
        # "category/<str:category_slug>/"としてURL入力で渡された"category_slug"を
        # self.kwargs["category_slug"]で取得する
        # 実際には"機械学習"などの文字列が格納されていることになる
        category_slug = self.kwargs["category_slug"]
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class SubCategoryPostView(ListView):
    model = Post
    template_name = "blog/sub_category_post.html"

    def get_queryset(self):
        sub_category_slug = self.kwargs["sub_category_slug"]
        self.sub_category = get_object_or_404(SubCategory, slug=sub_category_slug)
        qs = super().get_queryset().filter(sub_category=self.sub_category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sub_category"] = self.sub_category
        return context
