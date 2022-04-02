from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    fontawesome = models.CharField(max_length=255, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    eye_catching_img = models.ImageField(
        upload_to="post_images/", null=True, blank=True
    )  # 画像の保存先はMEDIA_ROOTのサブディレクトリ
    content = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # その記事を公開する（is_publicをTrueにする）際に
        # 公開日が設定されていない（つまり初めて公開した）時に
        # 現在の日時をpublished_atに設定する
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to="post_content_images/")
