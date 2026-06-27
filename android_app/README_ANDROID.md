# 📱 St. Thomas Marthoma Church — Android Management App

## Overview
This is a native Android management app for church admins to manage the website content from their phone.

## Tech Stack
- **Language:** Kotlin
- **Architecture:** MVVM + Repository pattern
- **Networking:** Retrofit2 + OkHttp
- **UI:** Material Design 3 + ViewBinding
- **Auth:** JWT token via Django REST Framework

## Setup Instructions

### 1. Add Django REST Framework to your backend
```bash
pip install djangorestframework djangorestframework-simplejwt
```

Add to `settings.py`:
```python
INSTALLED_APPS += ['rest_framework']
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAdminUser'],
}
```

### 2. App Features
- **Dashboard** — View member count, donation stats, prayer requests
- **Prayer Requests** — View, update status (New → Acknowledged → Praying → Resolved)
- **Queries** — Read and respond to pastoral queries
- **Events** — Add/edit/delete upcoming events
- **Service Timings** — Update weekly service schedule
- **Sunday Readings** — Update this week's Bible readings and hymn numbers
- **Donations** — View donation history and export CSV
- **Gallery** — Upload/remove photos
- **Push Notifications** — Receive alerts for new prayer requests, queries, donations

### 3. Build (Android Studio)
1. Open `android_app/` in Android Studio (Hedgehog or later)
2. Update `BASE_URL` in `Constants.kt` to your server IP
3. Build → Run on device or emulator (API 26+)

---
