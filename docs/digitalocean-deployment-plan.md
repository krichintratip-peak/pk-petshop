# DigitalOcean Deployment Plan - Petshop Django

## 📋 ภาพรวม

แผนการ deploy โปรเจค Petshop Django ไปยัง DigitalOcean ด้วย Docker

---

## 🏗️ Architecture ที่แนะนำ

### แนวทางที่เลือก: **DigitalOcean Droplet + Docker Compose**

เหตุผล:
- ควบคุมได้เต็มรูปแบบ
- ราคาประหยัดสำหรับ small-medium project
- ตรงกับ Docker setup ที่มีอยู่แล้ว
- ไม่ต้องปรับโครงสร้างโปรเจคมาก

### Components

```
┌─────────────────────────────────────────────────────────────┐
│                    DigitalOcean Droplet                     │
│                      (Ubuntu 22.04 LTS)                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Nginx     │  │  Gunicorn   │  │    PostgreSQL       │ │
│  │  (Reverse   │──│   (Django)  │──│  (Database)         │ │
│  │   Proxy)    │  │             │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│        │                                                    │
│        ▼                                                    │
│  ┌─────────────┐                                            │
│  │  Certbot   │  (SSL/HTTPS - Let's Encrypt)              │
│  └─────────────┘                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💰 ค่าใช้จ่ายโดยประมาณ

| Component | Spec | ราคา/เดือน |
|-----------|------|-----------|
| Droplet (Basic) | 1 vCPU / 2GB RAM / 50GB SSD | ~$12 (~420 THB) |
| Domain (optional) | .com or .co.th | ~$10-15/ปี |
| SSL Certificate | Let's Encrypt (ฟรี) | $0 |
| **รวม** | | **~$12-15/เดือน** |

---

## 📁 โครงสร้างไฟล์ที่ต้องสร้าง

```
petshop/
├── docker-compose.prod.yml          # compose สำหรับ production
├── docker-compose.override.yml      # override สำหรับ local dev
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf                   # config สำหรับ reverse proxy
├── scripts/
│   ├── deploy.sh                    # script deploy อัตโนมัติ
│   └── init-ssl.sh                  # ตั้งค่า SSL ครั้งแรก
├── .env.prod.example                # template environment variables
└── docs/
    └── deployment-guide.md          # คู่มือ deployment ละเอียด
```

---

## 🔧 ขั้นตอนการ Deploy

### Phase 1: เตรียมโปรเจค (1-2 ชั่วโมง)

1. **สร้าง production compose file**
2. **สร้าง Nginx config**
3. **สร้าง environment files**
4. **ทดสอบ build locally**

### Phase 2: ตั้งค่า DigitalOcean (1 ชั่วโมง)

1. **สร้าง Droplet**
   - OS: Ubuntu 22.04 LTS
   - Plan: Basic ($12/month)
   - Datacenter: ใกล้ผู้ใช้มากที่สุด (Singapore หรือ Bangalore)
   - SSH Key: สร้างและดาวน์โหลด

2. **เชื่อมโยง Domain (ถ้ามี)**
   - ชี้ A record ไปยัง IP Droplet
   - รอ DNS propagate (~5-30 นาที)

### Phase 3: Deploy ขึ้น Server (1-2 ชั่วโมง)

1. **ติดตั้ง Docker และ Docker Compose**
2. **Clone repo**
3. **ตั้งค่า environment**
4. **Build และ run**
5. **ตั้งค่า SSL**
6. **ทดสอบ**

### Phase 4: CI/CD (Optional - 2-3 ชั่วโมง)

1. **ตั้งค่า GitHub Actions**
2. **สร้าง deploy pipeline**

---

## 🔐 ความปลอดภัยที่ต้องทำ

- [ ] เปลี่ยน SSH port จาก 22
- [ ] ตั้งค่า UFW Firewall
- [ ] ปิด root login
- [ ] ใช้ SSH key เท่านั้น
- [ ] ตั้งค่า Fail2ban
- [ ] ใช้ strong Django SECRET_KEY
- [ ] ตั้งค่า CSRF_TRUSTED_ORIGINS
- [ ] ใช้ HTTPS เท่านั้น (force SSL)
- [ ] ปิด DEBUG mode

---

## 📈 การ Scaling ในอนาคต

ถ้า traffic เพิ่ม:

1. **Upgrade Droplet**: เพิ่ม RAM/CPU
2. **Managed Database**: ย้าย PostgreSQL ไป DigitalOcean Managed DB
3. **Load Balancer**: ถ้าต้องการ high availability
4. **Spaces**: สำหรับ media files (S3-compatible storage)

---

## ⏱️ Timeline โดยประมาณ

| งาน | เวลา |
|-----|------|
| เตรียมโปรเจค + ทดสอบ local | 2 ชม. |
| ตั้งค่า DigitalOcean | 1 ชม. |
| Deploy ขึ้น server | 2 ชม. |
| ตั้งค่า SSL + ทดสอบ | 1 ชม. |
| CI/CD (optional) | 3 ชม. |
| **รวม** | **6-9 ชม.** |

---

## 🎯 ขั้นตอนถัดไป

ถ้าคุณต้องการให้ผมเริ่มทำ:

1. **สร้าง production files** (docker-compose.prod.yml, nginx config)
2. **สร้าง deployment scripts**
3. **เขียนคู่มือ deployment ละเอียด**

ให้พิมพ์ว่า **"เริ่มสร้างไฟล์ production"** แล้วผมจะทำให้ทันทีครับ
