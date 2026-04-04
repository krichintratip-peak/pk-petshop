"""
แทนที่รูปหมวด/สินค้า/บทความ อาหารเสริมแมว ด้วยภาพที่มีบริบทแมวหรือสัตวแพทย์ (ไม่ใช่วิตามินคน)
Run: python manage.py shell -c "exec(open('scripts/fix_supplement_cat_images.py', encoding='utf-8').read())"
"""
import os
import urllib.request

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.conf import settings
from django.core.files import File

from blog.models import Post
from products.models import Category, Product

BASE = "https://images.unsplash.com/{pid}?w=1400&q=85&auto=format&fit=crop"

# photo id -> path segment for images.unsplash.com
DOWNLOADS = [
    ("_cat_vet_kitten.jpg", BASE.format(pid="photo-1725409796872-8b41e8eca929")),
    ("_cat_drink_bottle.jpg", BASE.format(pid="photo-1603451757941-b11957205f69")),
    ("_cat_treat_hand.jpg", BASE.format(pid="photo-1765603732941-1a839b7f1d44")),
    ("_cat_eat_bowl.jpg", BASE.format(pid="photo-1596854331442-3cf47265cefb")),
    ("_cat_treats_floor.jpg", BASE.format(pid="photo-1749388930163-30e2eb45f86d")),
    ("_cat_pouch.jpg", BASE.format(pid="photo-1750279785829-1369c41e8db2")),
    ("_blog_supp_cat.jpg", BASE.format(pid="photo-1596854331442-3cf47265cefb")),
]

TMP = os.path.join(settings.MEDIA_ROOT, "_tmp_import")
os.makedirs(TMP, exist_ok=True)


def fetch(url: str, dest: str) -> None:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; PetshopFix/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    if len(data) < 3000:
        raise RuntimeError(f"Bad download: {url}")
    with open(dest, "wb") as f:
        f.write(data)


for fname, url in DOWNLOADS:
    path = os.path.join(TMP, fname)
    if not os.path.isfile(path) or os.path.getsize(path) < 3000:
        print("DL", fname)
        fetch(url, path)


def save_img(obj, field: str, tmp: str, upload: str) -> None:
    with open(os.path.join(TMP, tmp), "rb") as f:
        getattr(obj, field).save(upload, File(f), save=True)


cat_sup = Category.objects.get(slug="cat-supplements")
save_img(cat_sup, "image", "_cat_vet_kitten.jpg", "category-cat-supplements-vet.jpg")

mapping = [
    ("supp-omega3-oil-100ml", "_cat_drink_bottle.jpg", "supp-omega3-oil-cat.jpg"),
    ("supp-omega3-caps-60", "_cat_treat_hand.jpg", "supp-omega-caps-cat.jpg"),
    ("supp-multivitamin-chew-90", "_cat_eat_bowl.jpg", "supp-multivit-cat-bowl.jpg"),
    ("supp-probiotic-powder-30", "_cat_treats_floor.jpg", "supp-probiotic-cat.jpg"),
    ("supp-taurine-liquid-50ml", "_cat_pouch.jpg", "supp-taurine-cat-pouch.jpg"),
]
for slug, tmp, up in mapping:
    p = Product.objects.get(slug=slug)
    save_img(p, "image", tmp, up)
    print("Product", slug)

post = Post.objects.filter(slug="cat-supplement-feeding-guide").first()
if post:
    save_img(post, "featured_image", "_blog_supp_cat.jpg", "blog-supplement-cat-feeding.jpg")
    print("Blog featured updated")

print("Done — รูปอาหารเสริมเป็นบริบทแมวแล้ว")
