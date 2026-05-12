from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import random


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    def __str__(self):
        return self.email or self.phone_number or str(self.id)
    
    def save(self, *args, **kwargs):
        try:
            old = User.objects.get(pk=self.pk)
            if old.profile_picture and old.profile_picture != self.profile_picture:
                old.profile_picture.delete(save=False)
        except User.DoesNotExist:
            pass
        super().save(*args, **kwargs)


class County(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='counties')

    class Meta:
        verbose_name_plural = "Counties"
        unique_together = ('name', 'country')
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user}"


class AIChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_chat_messages')
    text = models.TextField()
    is_from_user = models.BooleanField(default=True, help_text="True if message is from the user, False if from AI")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        sender = 'User' if self.is_from_user else 'AI'
        return f"{sender} to {self.user} at {self.created_at}"


class Therapist(models.Model):
    """Dedicated therapist directory model for the mobile app."""

    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='therapists/', null=True, blank=True)

    location = models.CharField(max_length=255)
    county = models.CharField(max_length=120, null=True, blank=True)
    town = models.CharField(max_length=120)

    phone = models.CharField(max_length=30)
    whatsapp = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    specialization = models.ManyToManyField(Specialty, blank=True, related_name='therapists')

    bio = models.TextField()
    full_bio = models.TextField(blank=True)
    qualifications = models.JSONField(default=list, blank=True)
    experience = models.CharField(max_length=255, blank=True)

    license_number = models.CharField(max_length=80, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    availability = models.CharField(max_length=120, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PasswordReset(models.Model):
    """Store password reset tokens with expiry"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    token = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['token', 'is_used']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Reset for {self.user.email or self.user.username} - {self.token}"

    def is_valid(self):
        """Check if token is still valid (not used and not expired)"""
        from django.utils import timezone
        return not self.is_used and timezone.now() < self.expires_at


class TherapistReview(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=120)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.author} ({self.rating})"


class SecurityQuestion(models.Model):
    """Store user's security question and answer for password recovery"""
    QUESTIONS = [
        ('mother_maiden', "What is your mother's maiden name?"),
        ('first_pet', "What was the name of your first pet?"),
        ('primary_school', "What primary school did you attend?"),
        ('childhood_city', "What city did you grow up in?"),
        ('first_car', "What was your first car?"),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_question')
    question = models.CharField(max_length=50, choices=QUESTIONS)
    answer = models.CharField(max_length=255)

    def set_answer(self, raw_answer):
        """Hash and store the answer (case-insensitive)"""
        from django.contrib.auth.hashers import make_password
        self.answer = make_password(raw_answer.lower().strip())

    def check_answer(self, raw_answer):
        """Check if answer matches (case-insensitive)"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_answer.lower().strip(), self.answer)

    def __str__(self):
        return f"{self.user.username} - {self.get_question_display()}"


class PasswordResetOTP(models.Model):
    """Store OTP codes for password reset"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        """Check if OTP is still valid (10 minutes expiry)"""
        expiry = self.created_at + timezone.timedelta(minutes=10)
        return timezone.now() < expiry and not self.is_used

    @staticmethod
    def generate_otp():
        """Generate 6-digit OTP"""
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.user.username} - {self.otp}"