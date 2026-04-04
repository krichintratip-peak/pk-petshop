"""
One-off: refresh ขนมแมวเลีย + ทรายแมว images; add paper/corn/charcoal litter products.
Run: python manage.py shell < scripts/update_lick_litter_media.py
   or: python manage.py shell -c "exec(open('scripts/update_lick_litter_media.py', encoding='utf-8').read())"
"""
import os
import urllib.request
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.conf import settings
from django.core.files import File

from blog.models import Post
from products.models import Category, Product

# Unsplash — w=1400&q=85 (Unsplash License; attribute in site footer/docs if needed)
ASSETS = [
    ("_tmp_lick_pouch.jpg", "https://images.unsplash.com/photo-1750279785829-1369c41e8db2?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_lick_stick.jpg", "https://images.unsplash.com/photo-1750279785897-ba67fd35dde1?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_lick_liquid.jpg", "https://images.unsplash.com/photo-1603451757941-b11957205f69?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_cat_box.jpg", "https://images.unsplash.com/photo-1727510153658-643787acb16a?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_granules.jpg", "https://images.unsplash.com/photo-1724080241975-943438470755?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_sand.jpg", "https://images.unsplash.com/photo-1614587469816-65f010b9d179?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_sand_wet.jpg", "https://images.unsplash.com/photo-1599760121427-118bed4a10a5?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_fine_sand.jpg", "https://images.unsplash.com/photo-1758467614651-02bad4840a42?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_silica.jpg", "https://images.unsplash.com/photo-1672090630681-e69da8006146?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_wood_chips.jpg", "https://images.unsplash.com/photo-1737202294763-4f5d087d139c?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_tofu_pellets.jpg", "https://images.unsplash.com/photo-1639843606783-b2f9c50a7468?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_paper.jpg", "https://images.unsplash.com/photo-1715522594847-67c90b5b8667?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_corn.jpg", "https://images.unsplash.com/photo-1668350102568-d998ada9af9c?w=1400&q=85&auto=format&fit=crop"),
    ("_tmp_litter_charcoal.jpg", "https://images.unsplash.com/photo-1734415646846-c64d73f9f4f3?w=1400&q=85&auto=format&fit=crop"),
]

TMP_DIR = os.path.join(settings.MEDIA_ROOT, "_tmp_import")
os.makedirs(TMP_DIR, exist_ok=True)

for fname, url in ASSETS:
    dest = os.path.join(TMP_DIR, fname)
    if not os.path.isfile(dest) or os.path.getsize(dest) < 5000:
        print("Downloading", fname, "...")
        urllib.request.urlretrieve(url, dest)

line = getattr(settings, "LINE_ORDER_URL", "https://line.me/R/ti/p/@Dr.peakmaker")


def save_image_field(obj, field_name, tmp_name, upload_name):
    path = os.path.join(TMP_DIR, tmp_name)
    with open(path, "rb") as f:
        getattr(obj, field_name).save(upload_name, File(f), save=True)


# —— ขนมแมวเลีย ——
cat = Category.objects.get(slug="cat-lick-treats")
save_image_field(cat, "image", "_tmp_lick_pouch.jpg", "cat-lick-treats-hero.jpg")

pouch = "_tmp_lick_pouch.jpg"
stick = "_tmp_lick_stick.jpg"
liquid = "_tmp_lick_liquid.jpg"

mapping_lick = [
    ("lick-treat-tuna-4", pouch, "lick-treat-tuna.jpg"),
    ("lick-treat-chicken-6", stick, "lick-treat-chicken.jpg"),
    ("lick-treat-liver-6", liquid, "lick-treat-liver.jpg"),
]
for slug, tmp, upload in mapping_lick:
    p = Product.objects.get(slug=slug)
    save_image_field(p, "image", tmp, upload)

try:
    post = Post.objects.get(slug="cat-lick-treats-guide")
    save_image_field(post, "featured_image", "_tmp_lick_pouch.jpg", "blog-lick-treat-guide-hero.jpg")
except Post.DoesNotExist:
    pass

# —— หมวดทรายแมว ——
cl = Category.objects.get(slug="cat-litter")
save_image_field(cl, "image", "_tmp_litter_cat_box.jpg", "cat-litter-category-hero.jpg")

# slug -> (tmp file, upload name)
mapping_litter = [
    ("cat-litter-clumping-10kg", "_tmp_litter_granules.jpg", "litter-clumping-granules.jpg"),
    ("cat-litter-natural-8kg", "_tmp_litter_sand.jpg", "litter-natural-sand.jpg"),
    ("cat-litter-light-5kg", "_tmp_litter_sand_wet.jpg", "litter-light-absorb.jpg"),
    ("cat-litter-premium-clump-8kg", "_tmp_litter_fine_sand.jpg", "litter-premium-fine.jpg"),
    ("cat-litter-silica-4kg", "_tmp_litter_silica.jpg", "litter-silica-crystals.jpg"),
    ("cat-litter-pine-5kg", "_tmp_litter_wood_chips.jpg", "litter-pine-pellets.jpg"),
    ("cat-litter-tofu-6kg", "_tmp_litter_tofu_pellets.jpg", "litter-tofu-pellets.jpg"),
]
for slug, tmp, upload in mapping_litter:
    p = Product.objects.get(slug=slug)
    save_image_field(p, "image", tmp, upload)

# —— สินค้าทรายแมวเพิ่ม ——
NEW_LITTER = [
    {
        "slug": "cat-litter-paper-5kg",
        "name": "ทรายแมวกระดาษรีไซเคิล 5 กก.",
        "price": Decimal("289.00"),
        "tmp": "_tmp_litter_paper.jpg",
        "upload": "litter-recycled-paper.jpg",
        "description": "ทรายแมวจากกระดาษรีไซเคิล น้ำหนักเบา ฝุ่นน้อย เหมาะแมวแพ้ฝุ่นและบ้านที่เน้นสิ่งแวดล้อม",
        "body": "<p>เม็ดกระดาษดูดซับความชื้นได้ดี สามารถทิ้งลงโถส้วมได้บางสูตรตามคำแนะนำผู้ผลิต เปลี่ยนทรายเป็นประจำเพื่อสุขอนามัย</p>",
    },
    {
        "slug": "cat-litter-corn-4kg",
        "name": "ทรายแมวธัญพืช (ข้าวโพด) ย่อยสลายได้ 4 กก.",
        "price": Decimal("319.00"),
        "tmp": "_tmp_litter_corn.jpg",
        "upload": "litter-corn-based.jpg",
        "description": "ทรายแมวจากแป้งข้าวโพดธรรมชาติ จับก้อนได้ กลิ่นอ่อน เหมาะแมวเลี้ยงในบ้าน",
        "body": "<p>วัสดุจากพืช ลดผลกระทบต่อสิ่งแวดล้อมเมื่อเทียบกับบางชนิดของดินเหนียว เก็บในที่แห้งปิดมิดชิด</p>",
    },
    {
        "slug": "cat-litter-charcoal-10kg",
        "name": "ทรายแมวเบนทonite ผสมถ่านกัมมัน ดูดกลิ่น 10 กก.",
        "price": Decimal("359.00"),
        "tmp": "_tmp_litter_charcoal.jpg",
        "upload": "litter-bentonite-charcoal.jpg",
        "description": "เม็ดดินเหนียวจับก้อนแน่น ผสมถ่านกัมมันช่วยดูดกลิ่น แข็งแรงทนทาน เหมาะใช้หลายแมว",
        "body": "<p>เหมาะสำหรับผู้ที่ต้องการควบคุมกลิ่นในคอนโดหรือห้องแคบ ไม่ควรทิ้งลงโถส้วม</p>",
    },
]

for row in NEW_LITTER:
    p, created = Product.objects.get_or_create(
        slug=row["slug"],
        defaults={
            "category": cl,
            "name": row["name"],
            "description": row["description"],
            "body": row["body"],
            "price": row["price"],
            "available": True,
            "line_contact_link": line,
        },
    )
    if not created:
        p.category = cl
        p.name = row["name"]
        p.description = row["description"]
        p.body = row["body"]
        p.price = row["price"]
        p.available = True
        p.line_contact_link = line
        p.save()
    save_image_field(p, "image", row["tmp"], row["upload"])
    print("Litter product:", p.slug, "created" if created else "updated")

print("Done.")
