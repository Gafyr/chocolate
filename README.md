# 🍫 The Chocolate Factory — Mini-MRP System

Kichik shokolad fabrikasi uchun inventar va ishlab chiqarishni boshqarish bo'yicha Mini-MRP (MVP) tizimi.

## 🚀 Texnologiyalar Steki
- **Backend:** Python (FastAPI)
- **Database:** PostgreSQL / SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, Tailwind CSS, JavaScript (Vanilla)
- **Containerization:** Docker & Docker-Compose

## 📌 Asosiy Xususiyatlar va ACID Tranzaksiya
- 1 dona "Qora shokolad" ishlab chiqarish uchun ombordan **50g Kakao** va **20g Shakar** sarflanadi.
- **Atomar Tranzaksiya (ACID):** Ishlab chiqarish jarayoni bitta atomar tranzaksiyada bajariladi. Agar xom ashyo yetarli bo'lmasa, ma'lumotlar bazasiga hech qanday o'zgartirish kiritilmaydi va tranzaksiya bekor qilinadi (`rollback`).
- Amallar tarixi (`production_logs`) bazada to'liq saqlanadi.

## 🛠 Ishga tushirish yo'riqnomasi

### Option 1: Docker bilan (Tavsiya etiladi)
```bash
docker-compose up --build