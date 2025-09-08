from django.shortcuts import render, get_object_or_404
from .models import Post 
from products.models import Product, Category


def home(request):
    all_posts = Post.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'all_posts': all_posts,
        'products': products,
        'categories': categories
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    # Get the current post
    single_post = get_object_or_404(Post, slug=slug)

    # Query recent articles (exclude the current post and limit to 3)
    recent_articles = (
        Post.objects.exclude(id=single_post.id)  # Exclude the current post
        .order_by('-date_updated')[:3]  # Get the 3 most recent articles
    )

    # Query a single random product
    recommended_products = Product.objects.order_by('?').first()

    context = {
        'single_post': single_post,
        'recent_articles': recent_articles,
        'product': recommended_products
    }
    return render(request, 'blog/blog-detail.html', context)



