from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import (OrganizationTiming, Priest, ServiceTiming, SundayReading, Event, CommitteeMember,
                     Organization, PrayerRequest, Query, GalleryPhoto, SiteContent)
import datetime
import json
import os



def get_readings():
    file_path = os.path.join(
        os.path.dirname(__file__),
        "readings.json"
    )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "lesson1": "",
            "lesson2": "",
            "epistle": "",
            "gospel": "",
            "date": ""
        }


def get_live_readings():
    data = cache.get("live_readings")

    if data is None:
        data = scrape_lectionary()
        cache.set("live_readings", data, 60 * 60 * 6)  # Cache for 6 hours

    return data


def home(request):
    content = get_site_content()
    data = scrape_lectionary()
    sunday_readings = get_live_readings()
    sunday_services = ServiceTiming.objects.filter(day='Sunday', is_active=True)
    weekday_services = ServiceTiming.objects.filter(day__in=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Daily'], is_active=True)
    org_timings = ServiceTiming.objects.filter(is_active=True).exclude(day__in=['Sunday','Daily'])
    upcoming_events = Event.objects.filter(date__gte=datetime.date.today(), status='active').order_by('date')[:6]
    committee = CommitteeMember.objects.filter(is_active=True).order_by('order')
    orgs = Organization.objects.filter(is_active=True).order_by('order')
    organizations = OrganizationTiming.objects.filter(is_active=True)
    context = {
        'content': content,
        'sunday_readings': sunday_readings,
        'selected_songs': selected_songs,
        'sunday_services': sunday_services,
        'weekday_services': weekday_services,
        'upcoming_events': upcoming_events,
        'committee': committee,
        'orgs': orgs,
    }
    


    return render(request, 'main/home.html', context)


def history(request):
    content = get_site_content()
    priests = Priest.objects.all()
    return render(request, 'main/history.html', {'content': content, 'priests': priests})


def events(request):
    content = get_site_content()
    upcoming = Event.objects.filter(date__gte=datetime.date.today()).order_by('date')
    past = Event.objects.filter(date__lt=datetime.date.today()).order_by('-date')[:10]
    gallery = GalleryPhoto.objects.filter(is_active=True).order_by('order')[:12]
    return render(request, 'main/events.html', {
        'content': content, 'upcoming': upcoming, 'past': past, 'gallery': gallery
    })


def donate(request):
    content = get_site_content()
    if request.method == 'POST':
        donor_name = request.POST.get('donor_name', '')
        amount = request.POST.get('amount', '')
        purpose = request.POST.get('purpose', '')
        gateway = request.POST.get('gateway', 'razorpay')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        pan = request.POST.get('pan', '')
        messages.success(request, f'Thank you {donor_name}! Redirecting to secure payment... 🔒')
        return redirect('donate')
    return render(request, 'main/donate.html', {'content': content})


def prayer_request(request):
    content = get_site_content()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and message:
            pr = PrayerRequest.objects.create(name=name, phone=phone, email=email, message=message)
            try:
                send_mail(
                    subject=f'🙏 New Prayer Request from {name}',
                    message=f'Name: {name}\nPhone: {phone}\nEmail: {email}\n\nPrayer Request:\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CHURCH_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, '🙏 Your prayer request has been submitted. We will pray for you.')
            return redirect('prayer_request')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'main/prayer_request.html', {'content': content})


def queries(request):
    content = get_site_content()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        query_type = request.POST.get('query_type', 'General Query')
        message = request.POST.get('message', '').strip()
        if name and message:
            Query.objects.create(
                name=name, phone=phone, email=email,
                query_type=query_type, message=message
            )
            try:
                send_mail(
                    subject=f'📩 New {query_type} from {name}',
                    message=f'Name: {name}\nPhone: {phone}\nEmail: {email}\nType: {query_type}\n\nMessage:\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CHURCH_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, '✅ Your query has been submitted. We will get back to you soon.')
            return redirect('queries')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'main/queries.html', {'content': content})
