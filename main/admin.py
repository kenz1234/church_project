from django.contrib import admin
from django.utils.html import format_html
from .models import (OrganizationTiming, Priest, SundayReading, ServiceTiming, Event, CommitteeMember,
                     Organization, PrayerRequest, Query, Donation, GalleryPhoto, SiteContent)


@admin.register(ServiceTiming)
class ServiceTimingAdmin(admin.ModelAdmin):
    list_display = ('name', 'day', 'time', 'location', 'is_active')
    list_filter = ('day', 'is_active')
    list_editable = ('is_active',)
    ordering = ('day', 'time')


@admin.register(SundayReading)
class SundayReadingAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'hymn1',
        'hymn2',
        'offertory',
        'communion',
    )
    ordering = ('-date',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time', 'category', 'status', 'location')
    list_filter = ('category', 'status')
    list_editable = ('status',)
    ordering = ('date',)
    search_fields = ('name', 'description')
    date_hierarchy = 'date'


@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'photo_preview',
        'role',
        'phone',
        'email',
        'order',
        'is_active'
    )

    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    search_fields = ('name', 'role')

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;">',
                obj.photo.url
            )
        return "-"

    photo_preview.short_description = "Photo"

@admin.register(Priest)
class PriestAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenure', 'order')
    list_editable = ('order',)


@admin.register(Organization)
class OrganizationPreviewAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'name',
        'founded',
        'leader',
        'order',
        'is_active'
    )

    list_editable = ('order', 'is_active')

    fieldsets = (
        ('Organization Preview', {
            'fields': (
                'name',
                'description',
                'preview_image',
                'founded',
                'leader',
                'order',
                'is_active',
            )
        }),
    )

    def image_preview(self, obj):
        if obj.preview_image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.preview_image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"

@admin.register(OrganizationTiming)
class OrganizationTimingAdmin(admin.ModelAdmin):
    list_display = ('name', 'timing', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    ordering = ('display_order',) 


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'submitted_at')
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('name', 'message')
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('Requester Info', {'fields': ('name', 'phone', 'email')}),
        ('Request', {'fields': ('message',)}),
        ('Admin', {'fields': ('status', 'admin_notes', 'submitted_at')}),
    )


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'query_type', 'status', 'submitted_at')
    list_filter = ('query_type', 'status')
    list_editable = ('status',)
    search_fields = ('name', 'message')
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('Contact Info', {'fields': ('name', 'phone', 'email')}),
        ('Query', {'fields': ('query_type', 'message')}),
        ('Admin Response', {'fields': ('status', 'admin_notes', 'admin_response', 'submitted_at')}),
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'colored_amount', 'purpose', 'gateway', 'donated_at')
    list_filter = ('purpose', 'gateway')
    search_fields = ('donor_name', 'transaction_id')
    readonly_fields = ('donated_at',)
    date_hierarchy = 'donated_at'

    def colored_amount(self, obj):
        return format_html('<strong style="color:#2D6A4F">₹{}</strong>', obj.amount)
    colored_amount.short_description = 'Amount'


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = (
        'caption',
        'event_name',
        'redirect_url',
        'order',
        'is_active',
        'uploaded_at'
    )

    list_editable = ('order', 'is_active')


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
