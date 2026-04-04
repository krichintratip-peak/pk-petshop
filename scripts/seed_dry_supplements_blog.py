"""
เพิ่มอาหารเม็ดหลากหลาย, หมวดอาหารเสริมแมว, สินค้า, บทความ Dr.Meaw, FAQ และลิงก์หมวด
Run: python manage.py shell -c "exec(open('scripts/seed_dry_supplements_blog.py', encoding='utf-8').read())"
"""
import os
import urllib.request
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.conf import settings
from django.core.files import File
from blog.models import Author, Post
from products.models import Category, FAQ, Product

LINE = getattr(settings, "LINE_ORDER_URL", "https://line.me/R/ti/p/@Dr.peakmaker")

REQ = urllib.request.Request


def fetch(url: str, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    r = REQ(url, headers={"User-Agent": "Mozilla/5.0 (compatible; PetshopSeed/1.0)"})
    with urllib.request.urlopen(r, timeout=60) as resp:
        data = resp.read()
    if len(data) < 2000:
        raise RuntimeError(f"Too small: {url}")
    with open(dest, "wb") as f:
        f.write(data)
    print("OK", os.path.basename(dest))


TMP = os.path.join(settings.MEDIA_ROOT, "_tmp_import")
os.makedirs(TMP, exist_ok=True)

# (filename, unsplash url)
DOWNLOADS = [
    ("dry_kibble1.jpg", "https://images.unsplash.com/photo-1764249453874-46864677b10e?w=1400&q=85&auto=format&fit=crop"),
    ("dry_cat_bowl.jpg", "https://images.unsplash.com/photo-1764576504536-dbdfa4cb1d9a?w=1400&q=85&auto=format&fit=crop"),
    ("dry_cat_eating.jpg", "https://images.unsplash.com/photo-1558993457-4bc6ec2c3734?w=1400&q=85&auto=format&fit=crop"),
    ("dry_bowl_close.jpg", "https://images.unsplash.com/photo-1695169954725-fa757fd7315c?w=1400&q=85&auto=format&fit=crop"),
    ("dry_kibble2.jpg", "https://images.unsplash.com/photo-1764249453850-faace6e57444?w=1400&q=85&auto=format&fit=crop"),
    # รูปหมวด/อาหารเสริม: ใช้บริบทแมว (ไม่ใช่วิตามินคน) — สอดคล้อง scripts/fix_supplement_cat_images.py
    ("supp_cat_hero.jpg", "https://images.unsplash.com/photo-1725409796872-8b41e8eca929?w=1400&q=85&auto=format&fit=crop"),
    ("supp_fish_oil.jpg", "https://images.unsplash.com/photo-1603451757941-b11957205f69?w=1400&q=85&auto=format&fit=crop"),
    ("supp_omega_caps.jpg", "https://images.unsplash.com/photo-1765603732941-1a839b7f1d44?w=1400&q=85&auto=format&fit=crop"),
    ("supp_pills.jpg", "https://images.unsplash.com/photo-1596854331442-3cf47265cefb?w=1400&q=85&auto=format&fit=crop"),
    ("supp_bottles.jpg", "https://images.unsplash.com/photo-1749388930163-30e2eb45f86d?w=1400&q=85&auto=format&fit=crop"),
    ("supp_omega_bottle.jpg", "https://images.unsplash.com/photo-1750279785829-1369c41e8db2?w=1400&q=85&auto=format&fit=crop"),
    ("blog_supp.jpg", "https://images.unsplash.com/photo-1596854331442-3cf47265cefb?w=1600&q=85&auto=format&fit=crop"),
]

for fname, url in DOWNLOADS:
    path = os.path.join(TMP, fname)
    if not os.path.isfile(path) or os.path.getsize(path) < 5000:
        fetch(url, path)


def save_img(obj, field: str, tmp_file: str, upload_name: str) -> None:
    p = os.path.join(TMP, tmp_file)
    with open(p, "rb") as f:
        getattr(obj, field).save(upload_name, File(f), save=True)


# —— Author Dr.Meaw ——
author = Author.objects.filter(name__iexact="dr.meaw").first()
if not author:
    author = Author.objects.create(name="Dr.Meaw", bio="สัตวแพทย์และที่ปรึกษาด้านโภชนาการแมว")
elif author.name != "Dr.Meaw":
    author.name = "Dr.Meaw"
    author.save()

# —— หมวดอาหารเสริม ——
sup, _ = Category.objects.get_or_create(
    slug="cat-supplements",
    defaults={
        "name": "อาหารเสริมแมว",
        "description": "วิตามิน โอเมก้า โปรไบโอติก และเกลือแร่เสริมสุขภาพแมว ใช้เสริมจากอาหารหลักตามคำแนะนำสัตวแพทย์",
    },
)
sup.description = (
    "วิตามิน โอเมก้า โปรไบโอติก และเกลือแร่เสริมสุขภาพแมว ใช้เสริมจากอาหารหลักตามคำแนะนำสัตวแพทย์"
)
sup.save()
save_img(sup, "image", "supp_cat_hero.jpg", "category-cat-supplements.jpg")

dry = Category.objects.get(slug="dry-cat-food")

NEW_DRY = [
    {
        "slug": "dry-food-salmon-rice-2kg",
        "name": "อาหารแมวเม็ด แซลมอนและข้าว 2 กก.",
        "price": Decimal("429.00"),
        "desc": "โปรตีนปลาแซลมอน รสชาติถูกปากแมวส่วนใหญ่ เม็ดพอดีคำ เคี้ยวง่าย",
        "body": "<p>เหมาะแมวโตที่ไม่แพ้อาหารทะเล แบ่งให้ตามคำแนะนำบนฉลากและน้ำหนักตัว</p>",
        "tmp": "dry_kibble1.jpg",
        "up": "dry-salmon-rice.jpg",
    },
    {
        "slug": "dry-food-indoor-weight-1-5kg",
        "name": "อาหารแมวเม็ด แมวในบ้าน ควบคุมน้ำหนัก 1.5 กก.",
        "price": Decimal("399.00"),
        "desc": "พลังงานพอเหมาะกับแมวขี้เกียจ ลดความเสี่ยงอ้วนเมื่อใช้ร่วมการควบคุมมื้อ",
        "body": "<p>แนะนำชั่งน้ำหนักเป็นระยะ ปรับปริมาณตามกิจกรรม</p>",
        "tmp": "dry_cat_bowl.jpg",
        "up": "dry-indoor-weight.jpg",
    },
    {
        "slug": "dry-food-hairball-2kg",
        "name": "อาหารแมวเม็ด ลดก้อนขน 2 กก.",
        "price": Decimal("459.00"),
        "desc": "สูตรช่วยระบบขับถ่ายและขน ฟีล์นแมวยาวหรือเลียขนบ่อย",
        "body": "<p>ใช้ร่วมการหวีขนเป็นประจำ ดื่มน้ำให้เพียงพอ</p>",
        "tmp": "dry_cat_eating.jpg",
        "up": "dry-hairball.jpg",
    },
    {
        "slug": "dry-food-senior-2kg",
        "name": "อาหารแมวเม็ด แมวสูงวัย 7+ ปี 2 กก.",
        "price": Decimal("479.00"),
        "desc": "เม็ดนุ่มขึ้น โปรตีนคุณภาพ สารประกอบสำหรับแมววัยเก๋า",
        "body": "<p>หากมีโรคไตหรือข้อควรปรึกษาสัตวแพทย์ก่อนเปลี่ยนสูตร</p>",
        "tmp": "dry_bowl_close.jpg",
        "up": "dry-senior.jpg",
    },
    {
        "slug": "dry-food-grain-free-duck-1-8kg",
        "name": "อาหารแมวเม็ด ไร้ธัญพืช เนื้อเป็ด 1.8 กก.",
        "price": Decimal("519.00"),
        "desc": "โปรตีนเป็ดเป็นหลัก เหมาะแมวแพ้บางชนิดของธัญพืช (ปรึกษาหมอก่อน)",
        "body": "<p>เปลี่ยนสูตรค่อยเป็นค่อยไป 7–10 วัน</p>",
        "tmp": "dry_kibble2.jpg",
        "up": "dry-grain-free-duck.jpg",
    },
]

for row in NEW_DRY:
    p, cr = Product.objects.get_or_create(
        slug=row["slug"],
        defaults={
            "category": dry,
            "name": row["name"],
            "description": row["desc"],
            "body": row["body"],
            "price": row["price"],
            "available": True,
            "line_contact_link": LINE,
        },
    )
    if not cr:
        p.category = dry
        p.name = row["name"]
        p.description = row["desc"]
        p.body = row["body"]
        p.price = row["price"]
        p.line_contact_link = LINE
        p.save()
    save_img(p, "image", row["tmp"], row["up"])
    print("Dry:", p.slug, "created" if cr else "updated")

SUPP_PRODUCTS = [
    {
        "slug": "supp-omega3-oil-100ml",
        "name": "น้ำมันปลา Omega-3 สำหรับแมว 100 มล.",
        "price": Decimal("289.00"),
        "desc": "กรดไขมัน EPA/DHA ช่วยบำรุงผิวหนังและขน หยดผสมอาหารตามคำแนะนำบนฉลาก",
        "body": "<p>เก็บในที่เย็น หลีกเลี่ยงแสง เริ่มจากปริมาณน้อยแล้วสังเกตการย่อย</p>",
        "tmp": "supp_fish_oil.jpg",
        "up": "supp-omega3-oil.jpg",
    },
    {
        "slug": "supp-omega3-caps-60",
        "name": "แคปซูล Omega-3 สำหรับแมว 60 เม็ด",
        "price": Decimal("349.00"),
        "desc": "แคปซูลแบ่งฉีดผสมอาหารหรือตามวิธีใช้บนฉลาก",
        "body": "<p>ไม่แนะนำให้แมวกลืนทั้งเม็ดโดยไม่เจาะหากแมวไม่กิน</p>",
        "tmp": "supp_omega_caps.jpg",
        "up": "supp-omega3-caps.jpg",
    },
    {
        "slug": "supp-multivitamin-chew-90",
        "name": "วิตามินรวมแมว แบบเคี้ยว 90 เม็ด",
        "price": Decimal("269.00"),
        "desc": "วิตามินและเกลือแร่เบื้องต้นเสริมจากอาหารหลักที่ครบถ้วน",
        "body": "<p>ไม่ใช่ยารักษาโรค ห้ามเกินปริมาณแนะนำต่อวัน</p>",
        "tmp": "supp_pills.jpg",
        "up": "supp-multivitamin.jpg",
    },
    {
        "slug": "supp-probiotic-powder-30",
        "name": "โปรไบโอติกผงสำหรับแมว 30 ซอง",
        "price": Decimal("319.00"),
        "desc": "จุลินทรีย์ช่วยสนับสนุนลำไส้ ผสมอาหารเปียกหรือเม็ดเล็กน้อย",
        "body": "<p>แมวป่วยฉับพลันหรือภูมิคุ้มกันต่ำควรปรึกษาหมอก่อน</p>",
        "tmp": "supp_bottles.jpg",
        "up": "supp-probiotic.jpg",
    },
    {
        "slug": "supp-taurine-liquid-50ml",
        "name": "ทอรีนน้ำสำหรับแมว 50 มล.",
        "price": Decimal("199.00"),
        "desc": "กรดอะมิโนสำคัญต่อหัวใจและสายตาแมว หยดผสมอาหารโฮมเมดหรือตามแพทย์แนะนำ",
        "body": "<p>แมวกินอาหารสมดุลตามมาตรฐานอาหารสัตว์เลี้ยง มักได้ทอรีนเพียงพอแล้ว — ใช้เสริมเมื่อมีเหตุผลทางการแพทย์</p>",
        "tmp": "supp_omega_bottle.jpg",
        "up": "supp-taurine-liquid.jpg",
    },
]

for row in SUPP_PRODUCTS:
    p, cr = Product.objects.get_or_create(
        slug=row["slug"],
        defaults={
            "category": sup,
            "name": row["name"],
            "description": row["desc"],
            "body": row["body"],
            "price": row["price"],
            "available": True,
            "line_contact_link": LINE,
        },
    )
    if not cr:
        p.category = sup
        p.name = row["name"]
        p.description = row["desc"]
        p.body = row["body"]
        p.price = row["price"]
        p.line_contact_link = LINE
        p.save()
    save_img(p, "image", row["tmp"], row["up"])
    print("Supp:", p.slug, "created" if cr else "updated")

# —— Blog ——
BLOG_SLUG = "cat-supplement-feeding-guide"
title = "วิธีให้อาหารเสริมแมวที่ถูกต้องและปลอดภัย"
desc = "คู่มือให้อาหารเสริมแบบไม่เกินจำเป็น ลดความเสี่ยงต่อไตและระบบทางเดินอาหาร"
body_html = """
<h2>อาหารเสริมคืออะไร</h2>
<p>อาหารเสริมเป็นการเพิ่มสารอาหารหรือจุลินทรีย์นอกเหนือจากอาหารหลัก ไม่ใช่การรักษาโรคแทนยา และไม่ควรแทนที่อาหารที่มีคุณค่าครบถ้วน</p>
<h2>หลักการสำคัญ</h2>
<ol>
<li><strong>เลือกตามความจำเป็น</strong> แมวกินอาหารเม็ด/เปียกคุณภาพดีมักได้สารอาหารหลักครบแล้ว</li>
<li><strong>นับปริมาณรวม</strong> อย่าให้ซ้ำซ้อนหลายชนิดที่มีส่วนผสมคล้ายกัน (เช่น โอเมก้าหลายตัว)</li>
<li><strong>แบ่งมื้อ</strong> ผสมกับอาหารมื้อเล็กๆ สังเกตอาการท้องเสียหรือไม่กิน</li>
<li><strong>โรคประจำตัว</strong> แมวไต หัวใจ หรือกำลังกินยา ต้องปรึกษาสัตวแพทย์ก่อนเสมอ</li>
</ol>
<h2>เมื่อไรควรปรึกษาหมอ</h2>
<p>ผมร่วงผิดปกติ ท้องเสียเรื้อรัง ซึม กินน้อยลง หรือวางแผนอาหารโฮมเมด — ควรให้หมอช่วยออกแบบโปรตีน แคลเซียม ทอรีน และเกลือแร่ให้เหมาะกับแต่ละตัว</p>
"""

post, pcr = Post.objects.get_or_create(
    slug=BLOG_SLUG,
    defaults={
        "title": title,
        "description": desc,
        "body": body_html,
        "author": author,
    },
)
if not pcr:
    post.title = title
    post.description = desc
    post.body = body_html
    post.author = author
    post.save()

save_img(post, "featured_image", "blog_supp.jpg", "blog-cat-supplement-guide.jpg")
post.related_categories.set([sup])
print("Blog:", post.slug, "linked to", sup.slug)

# —— FAQ อาหารเสริม ——
faqs = [
    (
        "อาหารเสริมแทนอาหารหลักได้ไหม?",
        "ไม่ควร อาหารเสริมไม่ได้ออกแบบให้ครบถ้วนเหมือนอาหารหลัก ใช้เพิ่มเติมตามปริมาณที่ระบุเท่านั้น",
    ),
    (
        "ลูกแมวให้อาหารเสริมได้ตั้งแต่อายุเท่าไร?",
        "ขึ้นกับชนิดสินค้า ควรอ่านฉลากและปรึกษาสัตวแพทย์ โดยเฉพาะลูกแมวต่ำกว่า 12 สัปดาห์",
    ),
    (
        "ให้หลายชนิดพร้อมกันปลอดภัยไหม?",
        "ควรหลีกเลี่ยงการซ้อนส่วนผสมเดิม (เช่น วิตามิน A หรือแคลเซียม) หากไม่แน่ใจให้สลับชนิดหรือปรึกษาหมอ",
    ),
    (
        "แมวไตควรเลือกอาหารเสริมอย่างไร?",
        "แมวไตมักต้องจำกัดฟอสฟอรัสและบางเกลือแร่ ห้ามให้เสริมเองโดยไม่มีคำแนะนำสัตวแพทย์",
    ),
    (
        "ควรให้พร้อมอาหารหรือแยกเวลา?",
        "ส่วนใหญ่ผสมกับอาหารมื้อหลักจะกินง่ายกว่า หากแมวสงสัยให้เริ่มปริมาณน้อยแล้วค่อยๆ เพิ่ม",
    ),
]

for q, a in faqs:
    obj, fcr = FAQ.objects.get_or_create(category=sup, question=q, defaults={"answer": a})
    if not fcr:
        obj.answer = a
        obj.save()
    print("FAQ:", q[:30], "...")

print("Seed dry + supplements + blog + FAQ complete.")
