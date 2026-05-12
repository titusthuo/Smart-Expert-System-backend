# core/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from .models import (
    User, Country, County,
    AIChatMessage,
    Therapist, TherapistReview, Specialty,
)

# Optional: cleaner sidebar - remove Groups
admin.site.unregister(Group)


# ====================== USER ADMIN ======================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'phone_number', 'first_name', 'last_name', 'country', 'preview_photo', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'country')
    search_fields = ('email', 'phone_number', 'first_name', 'last_name', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    def preview_photo(self, obj):
        """Display profile picture thumbnail in admin list view"""
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%; object-fit:cover;" />',
                obj.profile_picture.url
            )
        return "(No photo)"
    preview_photo.short_description = "Photo"




# ====================== THERAPIST DIRECTORY ADMIN ======================
@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'county',
        'town',
        'phone',
        'email',
        'license_number',
        'price',
        'availability',
    )
    search_fields = ('name', 'county', 'town', 'phone', 'email', 'license_number')
    list_filter = ('county', 'town', 'specialization')
    filter_horizontal = ('specialization',)


@admin.register(TherapistReview)
class TherapistReviewAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'author', 'rating', 'date')
    search_fields = ('therapist__name', 'author', 'comment')
    list_filter = ('rating', 'date')


# ====================== AI CHAT MESSAGE ADMIN ======================
@admin.register(AIChatMessage)
class AIChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender_display', 'short_text', 'created_at')
    list_filter = ('is_from_user', 'created_at', 'user')
    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'text',
    )
    readonly_fields = ('created_at',)
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def sender_display(self, obj):
        if obj.is_from_user:
            return format_html('<strong style="color:#1976d2;">{}</strong>', 'User')
        return format_html('<strong style="color:#43a047;">{}</strong>', 'AI Assistant')
    sender_display.short_description = "Sender"
    sender_display.admin_order_field = 'is_from_user'

    def short_text(self, obj):
        text = obj.text.strip()
        if len(text) > 80:
            return text[:77] + "..."
        return text
    short_text.short_description = "Message"




# ====================== OTHER SIMPLE ADMINS ======================
@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)
    raw_id_fields = ('country',)
    ordering = ('country__name', 'name')

