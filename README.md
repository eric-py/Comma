# Comma | کاما

**یک شبکه اجتماعی کوچک برای انتشار تصاویر و ارتباط کاربران با یکدیگر**  
**A small social network for sharing images and connecting users.**

---

## 🎯 درباره پروژه | About the Project

**Comma** یک پروژه شبکه اجتماعی ساده است که با استفاده از **Django** و **Tailwind CSS** ساخته شده است.  
**Comma** is a simple social network project built using **Django** and **Tailwind CSS**.

این پروژه به عنوان یک مینی پروژه برای نمایش در رزومه طراحی شده است.  
The project is designed as a mini-project to showcase in a portfolio.

---

## ✨ ویژگی‌ها | Features

- **انتشار تصاویر | Image Posting:** کاربران می‌توانند تصاویر خود را منتشر کنند.  
  Users can upload and share their images.  

- **لایک و کامنت | Likes and Comments:** امکان لایک و کامنت گذاری روی پست‌ها.  
  Ability to like and comment on posts.  

- **سیستم فالو کردن | Follow System:** دنبال کردن کاربران دیگر.  
  Follow other users.  

- **پروفایل قابل ویرایش | Editable Profile:** ویرایش اطلاعات پروفایل.  
  Editable user profiles.  

- **ذخیره پست‌ها | Save Posts:** ذخیره پست‌های مورد علاقه برای مرور بعدی.  
  Save favorite posts for later.  

- **رابط کاربری واکنش‌گرا | Responsive UI:** طراحی ریسپانسیو با Tailwind CSS.  
  Responsive design with Tailwind CSS.  

---

## 🛠 پیش‌نیازها | Prerequisites

برای اجرای این پروژه به موارد زیر نیاز دارید:  
You need the following to run this project:

- **Python 3.8+**  
- **Django 3.2+**  
- **Tailwind CSS**

---

## 🚀 نصب و راه‌اندازی | Installation & Setup

### 1️⃣ کلون کردن مخزن | Clone the Repository
```bash
git clone https://github.com/eric-py/comma.git
cd comma
```

### 2️⃣ ایجاد و فعال‌سازی محیط مجازی | Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3️⃣ نصب وابستگی‌ها | Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ نصب و کامپایل Tailwind | Install and Compile Tailwind
```bash
python manage.py tailwind install
python manage.py tailwind start
```

### 5️⃣ مهاجرت دیتابیس | Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ ایجاد کاربر ادمین | Create an Admin User
```bash
python manage.py createsuperuser
```

### 7️⃣ اجرای سرور توسعه | Run Development Server
```bash
python manage.py runserver
```

اکنون می‌توانید به آدرس `http://localhost:8000` در مرورگر خود مراجعه کنید.  
You can now access the app at `http://localhost:8000` in your browser.

---

## 💡 استفاده | Usage

پس از راه‌اندازی:  
After setup:

1. یک حساب کاربری ایجاد کنید.  
   Create a user account.  
2. تصاویر خود را آپلود کنید.  
   Upload your images.  
3. سایر کاربران را دنبال کنید و با آنها تعامل داشته باشید.  
   Follow and interact with other users.  

---

## 📝 نکات | Notes

- **دیتابیس:** SQLite برای محیط توسعه استفاده شده است. برای محیط تولید از دیتابیس‌های قوی‌تر مانند **PostgreSQL** استفاده کنید.  
  SQLite is used for development. Use a robust database like **PostgreSQL** for production.  

- **طراحی رابط کاربری:** از یک قالب ساده استفاده شده است که قابل بهبود است.  
  The UI design uses a basic template that can be enhanced.  