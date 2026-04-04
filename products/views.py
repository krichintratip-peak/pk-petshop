from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_detail(request, category_slug, product_slug):
    # Get the category and ensure the product belongs to it
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category, available=True)

    # Query related products (same category, exclude current product)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    context = {
        'category': category,
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/product-detail.html', context)


def category(request, slug):
    # Get the category
    category = get_object_or_404(Category, slug=slug)

    # Get products and FAQs for the category
    products = category.products.filter(available=True)
    faqs = category.faqs.all()

    related_posts = category.related_posts.all().order_by('-date_updated')

    context = {
        'category': category,
        'products': products,
        'faqs': faqs,
        'related_posts': related_posts,
    }
    return render(request, 'products/category.html', context)