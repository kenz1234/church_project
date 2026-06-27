from django.db import models
from django.utils import timezone


class ServiceTiming(models.Model):
    DAY_CHOICES = [
        ('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
        ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Daily', 'Daily'),
    ]
    name = models.CharField(max_length=200)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    time = models.TimeField()
    location = models.CharField(max_length=200, default='Main Sanctuary')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day', 'time']
        verbose_name = 'Service Timing'
        verbose_name_plural = 'Service Timings'

    def __str__(self):
        return f"{self.name} — {self.day} {self.time.strftime('%I:%M %p')}"


class SundayReading(models.Model):
    date = models.DateField(unique=True)
    hymn1 = models.CharField(max_length=50, blank=True, verbose_name='Opening Hymn 1 No.')
    hymn2 = models.CharField(max_length=50, blank=True, verbose_name='Opening Hymn 2 No.')
    offertory = models.CharField(max_length=50, blank=True, verbose_name='Offertory Song No.')
    communion = models.CharField(max_length=50, blank=True, verbose_name='Communion Hymn No.')
    live_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "song selection"
        verbose_name_plural = "Song Selections"

    def __str__(self):
        return f"Readings for {self.date}"


class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Feast Day', 'Feast Day'), ('Major Feast', 'Major Feast'),
        ('Youth', 'Youth'), ('Education', 'Education'),
        ('Fellowship', 'Fellowship'), ('Community', 'Community'), ('Other', 'Other'),
    ]
    STATUS_CHOICES = [('active', 'Active'), ('draft', 'Draft'), ('completed', 'Completed')]
    name = models.CharField(max_length=300)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.name} ({self.date})"


class CommitteeMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    # ADD THIS
    photo = models.ImageField(
        upload_to='committee_members/',
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    @property
    def initials(self):
        return ''.join(word[0].upper() for word in self.name.split()[:2])

    def __str__(self):
        return self.name
    
    @property
    def initials(self):
        words = (
            self.name.replace('Rev.', '')
            .replace('Rev', '')
            .replace('V.', '')
            .replace('Malpan','')
            .replace('Anicadu', '')
            .replace('Ayroor', '')
            .split()
        )

        if not words:
            return ''

        if len(words) == 1:
            return words[0][0].upper()

        return (words[0][0] + words[-1][0]).upper()



class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    founded = models.CharField(max_length=50, blank=True, null=True)
    leader = models.CharField(max_length=100, blank=True)

    preview_image = models.ImageField(
        upload_to='organizations/',
        blank=True,
        null=True
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PrayerRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'), ('acknowledged', 'Acknowledged'), ('praying', 'Praying'), ('resolved', 'Resolved')
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Prayer Request'
        verbose_name_plural = 'Prayer Requests'

    def __str__(self):
        return f"Prayer Request from {self.name} — {self.submitted_at.strftime('%b %d, %Y')}"


class Query(models.Model):
    TYPE_CHOICES = [
        ('General Query', 'General Query'),
        ('Sacrament Enquiry', 'Sacrament Enquiry (Baptism, Marriage, etc.)'),
        ('Pastoral Counselling', 'Pastoral Counselling'),
        ('Membership / Transfer', 'Membership / Transfer'),
        ('Donation Enquiry', 'Donation Enquiry'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'), ('in_progress', 'In Progress'), ('resolved', 'Resolved')
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    query_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='General Query')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)
    admin_response = models.TextField(blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'

    def __str__(self):
        return f"{self.query_type} from {self.name} — {self.submitted_at.strftime('%b %d, %Y')}"


class Donation(models.Model):
    GATEWAY_CHOICES = [
        ('razorpay', 'Razorpay'), ('payu', 'PayU'), ('paytm', 'Paytm'), ('upi', 'UPI Direct')
    ]
    PURPOSE_CHOICES = [
        ('General Church Fund', 'General Church Fund'),
        ('Building Maintenance', 'Building Maintenance'),
        ('Sunday School', 'Sunday School'),
        ('Youth Ministry (OCYM)', 'Youth Ministry (OCYM)'),
        ('Social Service / Charity', 'Social Service / Charity'),
        ('Feast Day Offering', 'Feast Day Offering'),
        ('Priest Support Fund', 'Priest Support Fund'),
        ('Memorial / Thanksgiving', 'Memorial / Thanksgiving'),
    ]
    donor_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=100, choices=PURPOSE_CHOICES, default='General Church Fund')
    gateway = models.CharField(max_length=20, choices=GATEWAY_CHOICES, default='razorpay')
    pan_number = models.CharField(max_length=10, blank=True)
    transaction_id = models.CharField(max_length=200, blank=True)
    is_anonymous = models.BooleanField(default=False)
    donated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-donated_at']
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    def __str__(self):
        return f"{'Anonymous' if self.is_anonymous else self.donor_name} — ₹{self.amount} ({self.purpose})"


class GalleryPhoto(models.Model):
    caption = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200, blank=True)

    image = models.ImageField(upload_to='gallery/')
    redirect_url = models.URLField(
        blank=True,
        help_text="URL to open when the image is clicked"
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']


class SiteContent(models.Model):
    hero_headline = models.CharField(max_length=300, default='Where Faith Meets Fellowship')
    hero_subtext = models.TextField(default='Gathered in the name of Christ, rooted in the ancient Orthodox tradition.')
    church_address = models.CharField(max_length=400, default='Tiruvalla - Vennikulam - Ranni Rd, Kavungumprayar Puramattam, Kerala 689544')
    phone = models.CharField(max_length=30, default='0469 2750591')
    email = models.EmailField(default='info@stthomaskottayam.org')
    youtube_link = models.URLField(blank=True)
    history_summary = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Content'
        verbose_name_plural = 'Site Content'

    def __str__(self):
        return f"Site Content (last updated {self.updated_at.strftime('%b %d, %Y')})"
    
class OrganizationTiming(models.Model):
    name = models.CharField(max_length=200)
    timing = models.CharField(max_length=100)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name



class Priest(models.Model):
    name = models.CharField(max_length=150)
    tenure = models.CharField(max_length=100)
    photo = models.ImageField(
        upload_to='priests/',
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def initials(self):
        words = (
            self.name.replace('Rev.', '')
            .replace('Rev', '')
            .replace('V.', '')
            .replace('Malpan','')
            .split()
        )

        if not words:
            return ''

        if len(words) == 1:
            return words[0][0].upper()

        return (words[0][0] + words[-1][0]).upper()