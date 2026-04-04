from django.db.models import Case, IntegerField, Q, Value, When
from django.shortcuts import get_object_or_404, redirect, render

from .models import Post
from products.models import Category, Product


def product_search(request):
    """ค้นหาสินค้า: ผลลัพธ์เดียวไปหน้ารายละเอียดทันที หลายรายการแสดงลิงก์เลือก"""
    q = (request.GET.get("q") or "").strip()
    if not q:
        return redirect("home")

    qs = (
        Product.objects.filter(available=True)
        .filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(slug__icontains=q)
            | Q(category__name__icontains=q)
        )
        .select_related("category")
        .distinct()
        .annotate(
            _prio=Case(
                When(name__icontains=q, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("_prio", "name")
    )

    n = qs.count()
    if n == 1:
        return redirect(qs.first().get_absolute_url())

    return render(
        request,
        "blog/search_products.html",
        {
            "search_query": q,
            "products": qs,
            "found_count": n,
        },
    )


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

    # Products from categories linked to this post (prefer these over fully random)
    related_categories = list(single_post.related_categories.all())
    if related_categories:
        recommended_products = (
            Product.objects.filter(category__in=related_categories, available=True)
            .order_by('?')
            .first()
        )
    else:
        recommended_products = None
    if recommended_products is None:
        recommended_products = Product.objects.filter(available=True).order_by('?').first()

    related_products = []
    if related_categories:
        related_products = list(
            Product.objects.filter(category__in=related_categories, available=True).distinct()[:8]
        )

    context = {
        'single_post': single_post,
        'recent_articles': recent_articles,
        'product': recommended_products,
        'related_categories': related_categories,
        'related_products': related_products,
    }
    return render(request, 'blog/blog-detail.html', context)



