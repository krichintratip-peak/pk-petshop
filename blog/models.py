# blog/models.py
from django.db import models
from django.urls import reverse


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='author_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    body = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog_images/',
        null=True,
        blank=True
    )
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='posts')
    related_categories = models.ManyToManyField(
        'products.Category',
        related_name='related_posts',
        blank=True,
        help_text='หมวดสินค้าที่เกี่ยวข้องกับบทความนี้',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    











