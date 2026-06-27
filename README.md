# ✝️ St. Thomas Marthoma Church — Django Web Application

**Complete church management system with animated website + admin panel + Android app foundation.**

---

## 🚀 Quick Start

```bash
# 1. Clone / unzip the project
cd church_project

# 2. Install dependencies
pip install django pillow

# 3. Apply migrations
python manage.py migrate

# 4. Create admin superuser
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver

# 6. Visit the site
http://localhost:8000/          → Public website
http://localhost:8000/admin/    → Hidden admin panel (login required)
```

---

## 📄 Pages

| URL | Description |
|-----|-------------|
| `/` | Home — Hero, Timings, Organizations, Committee, Prayer/Query buttons |
| `/history/` | Church history with animated timeline |
| `/events/` | Events list + Photo gallery |
| `/donate/` | Donation page with animated "Work in Progress" theme |
| `/prayerrequest/` | Dedicated prayer request form (sends email) |
| `/queries/` | Pastoral queries form with contact details |
| `/admin/` | **Admin-only** management panel |

---

## 🔐 Admin Panel (`/admin/`)

Login: `admin` / `church@2026` *(change this in production!)*

**Manage everything from admin:**
- ⛪ **Service Timings** — Add/edit/delete Sunday & weekday service times
- 📖 **Sunday Readings** — Update Bible readings & hymn numbers weekly
- 📅 **Events** — Create/manage upcoming events
- 👥 **Committee Members** — Update parish leadership
- 🏛 **Organizations** — Manage church ministries
- 🙏 **Prayer Requests** — View, track status (New → Acknowledged → Praying → Resolved)
- 📩 **Queries** — View and respond to pastoral queries
- 💰 **Donations** — Track donation records
- 🖼 **Gallery** — Upload/manage photos
- ✏️ **Site Content** — Edit hero text, contact info, YouTube link

---

## ✅ Changes Made from Original HTML

1. **Removed "Weekday Services"** as a separate tab — now integrated inline
2. **Prayer Requests** → Separate page at `/prayerrequest/` with email notification
3. **Queries** → Separate page at `/queries/` with Gmail + phone contact cards
4. **Donate page** → Animated "Work in Progress" banner with spinning gears, progress bar, shimmer effect
5. **Admin panel** → Hidden at `/admin/`, all content editable via Django admin with proper models
6. **All sections** → Reveal-on-scroll animations, hover effects, floating icons
7. **Full Django backend** → Database-driven content, form submissions saved to DB

---

## 📧 Email Setup (for Prayer Requests & Queries)

Edit `church_site/settings.py`:
```python
EMAIL_HOST_USER = 'your-church-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'  # Gmail App Password
CHURCH_EMAIL = 'your-church-gmail@gmail.com'
```

Generate Gmail App Password: Google Account → Security → 2-Step Verification → App Passwords

---

## 📱 Android App

See `android_app/README_ANDROID.md` for full setup.

Requires Django REST Framework:
```bash
pip install djangorestframework djangorestframework-simplejwt
```

Features: Dashboard, Prayer Requests mgmt, Query responses, Event CRUD, Readings update, Donations view, Push notifications.

---

## 🏗️ Production Deployment

```bash
pip install gunicorn whitenoise
# Update SECRET_KEY, DEBUG=False, ALLOWED_HOSTS in settings.py
python manage.py collectstatic
gunicorn church_site.wsgi:application
```

---

*Built for St. Thomas Marthoma Church, Kavungumprayar · Designed by Kenz M Saju*
