from django.db.models import Count, Q

from .models import Category, SubCategory


def common(request):
    category_list = Category.objects.annotate(
        num_posts=Count("post", filter=Q(post__is_public=True))
    ).order_by("-num_posts")
    sub_category_list = SubCategory.objects.annotate(
        num_posts=Count("post", filter=Q(post__is_public=True))
    ).order_by("-num_posts")
    category_sub_cateogry_dict = {}
    for category in category_list:
        category_sub_cateogry_dict[category] = sub_category_list.filter(
            parent_category__name=category
        )
    context = {
        "category_sub_category_dict": category_sub_cateogry_dict,
    }
    return context
