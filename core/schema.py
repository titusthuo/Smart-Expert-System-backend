import logging

import graphene

logger = logging.getLogger(__name__)
from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import get_token
from datetime import timedelta
from django.contrib.auth import authenticate
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from graphene_file_upload.scalars import Upload

from .models import (
    User, Country, County,
    AIChatMessage, Therapist, TherapistReview,
    Specialty, PasswordReset, SecurityQuestion, PasswordResetOTP,
)


class CoordsType(graphene.ObjectType):
    lat = graphene.Float()
    lng = graphene.Float()

class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = ("id", "name", "code")


class CountyType(DjangoObjectType):
    class Meta:
        model = County
        fields = ("id", "name", "country")


class TherapistReviewType(DjangoObjectType):
    class Meta:
        model = TherapistReview
        fields = ("id", "author", "rating", "date", "comment")


class TherapistType(DjangoObjectType):
    photo_url = graphene.String()
    coords = graphene.Field(CoordsType)
    specialization = graphene.List(graphene.String)
    license_number = graphene.String()

    rating = graphene.Float()
    reviews = graphene.Int()

    reviews_list = graphene.List(TherapistReviewType)

    full_bio = graphene.String()

    class Meta:
        model = Therapist
        fields = (
            "id",
            "name",
            "location",
            "county",
            "town",
            "phone",
            "whatsapp",
            "email",
            "bio",
            "price",
            "availability",
            "experience",
            "qualifications",
        )

    def resolve_photo_url(self, info):
        if self.photo:
            return info.context.build_absolute_uri(self.photo.url)
        return None

    def resolve_coords(self, info):
        if self.lat is None or self.lng is None:
            return None
        return CoordsType(lat=self.lat, lng=self.lng)

    def resolve_specialization(self, info):
        return list(self.specialization.values_list('name', flat=True))

    def resolve_license_number(self, info):
        return self.license_number

    def resolve_full_bio(self, info):
        return self.full_bio

    def resolve_reviews(self, info):
        if hasattr(self, '_review_count'):
            return self._review_count
        return self.reviews.count()

    def resolve_rating(self, info):
        if hasattr(self, '_avg_rating'):
            return float(self._avg_rating) if self._avg_rating is not None else 0.0
        agg = self.reviews.aggregate(avg=models.Avg('rating'))
        avg = agg.get('avg')
        return float(avg) if avg is not None else 0.0

    def resolve_reviews_list(self, info):
        return self.reviews.all()


class UserType(DjangoObjectType):
    name = graphene.String()
    phone = graphene.String()
    country = graphene.String()
    profile_picture_url = graphene.String()

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "first_name", "last_name", "is_active")

    def resolve_name(self, info):
        full = f"{(self.first_name or '').strip()} {(self.last_name or '').strip()}".strip()
        return full or self.username

    def resolve_phone(self, info):
        return self.phone_number

    def resolve_country(self, info):
        
        if self.country:
            return self.country.name
        return None
    
    def resolve_profile_picture_url(self, info):
        if self.profile_picture:
            return info.context.build_absolute_uri(self.profile_picture.url)
        return None


class AIChatMessageType(DjangoObjectType):
    class Meta:
        model = AIChatMessage
        fields = ("id", "text", "is_from_user", "created_at", "user")


class SignIn(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(root, info, username, password):
        user = authenticate(username=username, password=password)
        if not user:
            try:
                user_by_email = User.objects.get(email__iexact=username)
                user = authenticate(username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass
        if not user:
            try:
                user_by_phone = User.objects.get(phone_number=username)
                user = authenticate(username=user_by_phone.username, password=password)
            except User.DoesNotExist:
                pass
        if not user:
            return SignIn(success=False, error="Invalid credentials", token=None, user=None)
        token = get_token(user)
        return SignIn(success=True, token=token, user=user, error=None)


class SignUp(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        country = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)
    success = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(root, info, first_name, last_name, username, email, country, password):
        if User.objects.filter(username__iexact=username).exists():
            return SignUp(success=False, error="Username already taken")
        if User.objects.filter(email__iexact=email).exists():
            return SignUp(success=False, error="Email already registered")

        try:
            from django.contrib.auth.password_validation import validate_password
            validate_password(password)
        except ValidationError as e:
            return SignUp(success=False, error=" ".join(e.messages))

        username = username.lower().strip()
        email = email.lower().strip()
        first_name = first_name.strip()
        last_name = last_name.strip()
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        country_name = (country or "").strip()
        if country_name:
            resolved_country, _ = Country.objects.get_or_create(name=country_name)
            user.country = resolved_country
            user.save()

        token = get_token(user)
        return SignUp(success=True, error=None, token=token, user=user)


class UploadProfilePicture(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, file):
        user = info.context.user
        if not file:
            return UploadProfilePicture(success=False, error="No file provided", user=None)
        user.profile_picture = file
        user.save()
        return UploadProfilePicture(success=True, error=None, user=user)


class RemoveProfilePicture(graphene.Mutation):
    success = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info):
        user = info.context.user
        if user.profile_picture:
            user.profile_picture.delete(save=False)
            user.profile_picture = None
            user.save()
        return RemoveProfilePicture(success=True, error=None, user=user)


class UpdateProfile(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        phone = graphene.String()

    success = graphene.Boolean()
    error = graphene.String()
    user = graphene.Field(UserType)

    @staticmethod
    @login_required
    def mutate(root, info, name=None, email=None, phone=None):
        user = info.context.user
        
        try:
            # Update name (split into first_name and last_name)
            if name is not None:
                name_parts = name.strip().split(None, 1)
                user.first_name = name_parts[0] if len(name_parts) > 0 else ""
                user.last_name = name_parts[1] if len(name_parts) > 1 else ""
            
            # Update email
            if email is not None:
                email = email.strip()
                if email:
                    # Check if email is already taken by another user
                    if User.objects.filter(email=email).exclude(id=user.id).exists():
                        return UpdateProfile(success=False, error="Email already in use", user=None)
                    user.email = email
                else:
                    user.email = None
            
            # Update phone
            if phone is not None:
                phone = phone.strip()
                if phone:
                    # Check if phone is already taken by another user
                    if User.objects.filter(phone_number=phone).exclude(id=user.id).exists():
                        return UpdateProfile(success=False, error="Phone number already in use", user=None)
                    user.phone_number = phone
                else:
                    user.phone_number = None
            
            user.save()
            return UpdateProfile(success=True, error=None, user=user)
            
        except Exception as e:
            logger.exception("UpdateProfile failed for user %s", info.context.user)
            return UpdateProfile(success=False, error="An unexpected error occurred.", user=None)


class SendAIChatMessage(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)
        is_from_user = graphene.Boolean(default_value=True)

    message = graphene.Field(AIChatMessageType)
    success = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    @login_required
    def mutate(root, info, text, is_from_user=True):
        user = info.context.user
        if not user.is_authenticated:
            return SendAIChatMessage(success=False, error="Authentication required")
        
        text = text.strip()
        if not text:
            return SendAIChatMessage(success=False, error="Message text cannot be empty")
        
        message = AIChatMessage.objects.create(
            user=user,
            text=text,
            is_from_user=is_from_user,
        )
        return SendAIChatMessage(message=message, success=True, error=None)


class ForgotPassword(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, email):
        email = email.lower().strip()
        
        # Always return success to prevent email enumeration attacks
        success_message = "If an account with this email exists, a password reset link has been sent."
        
        try:
            user = User.objects.get(email__iexact=email)
            
            # Invalidate any existing reset tokens for this user
            PasswordReset.objects.filter(user=user, is_used=False).update(is_used=True)
            
            # Create new reset token
            reset_token = uuid.uuid4()
            expires_at = timezone.now() + timedelta(minutes=30)  # 30 minute expiry
            
            PasswordReset.objects.create(
                user=user,
                token=reset_token,
                expires_at=expires_at
            )
            
            # Send email with reset link
            from django.core.mail import send_mail
            from django.conf import settings as django_settings
            frontend_url = getattr(django_settings, 'FRONTEND_URL', 'http://localhost:8081')
            reset_link = f"{frontend_url}/reset-password/{reset_token}"
            
            try:
                send_mail(
                    subject='Password Reset Request - Smart Expert Mental Health Support',
                    message=f'''
Hello,

You requested a password reset for your Smart Expert Mental Health Support account.

Click the link below to reset your password:
{reset_link}

This link will expire in 30 minutes.

If you didn't request this password reset, please ignore this email.

Best regards,
Smart Expert Mental Health Support Team
                    '''.strip(),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@smarthealth.com'),
                    recipient_list=[email],
                    fail_silently=False,
                )
                logger.info("Password reset email sent to %s", email)
            except Exception as e:
                logger.error("Failed to send email to %s: %s", email, e)
                # Still continue - token is created, user can get link from console if needed
            
        except User.DoesNotExist:
            # Don't reveal that email doesn't exist
            pass
        
        return ForgotPassword(
            success=True, 
            message=success_message,
            error=None
        )




class ResetPassword(graphene.Mutation):
    class Arguments:
        token = graphene.String(required=True)
        new_password = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, token, new_password):
        try:
            reset_obj = PasswordReset.objects.get(token=token, is_used=False)
            
            if not reset_obj.is_valid():
                return ResetPassword(
                    success=False,
                    error="Invalid or expired reset token"
                )
            
            # Validate password
            if len(new_password) < 8:
                return ResetPassword(
                    success=False,
                    error="Password must be at least 8 characters long"
                )
            
            # Reject if new password is the same as current password
            user = reset_obj.user
            if user.check_password(new_password):
                return ResetPassword(
                    success=False,
                    error="New password must be different from your current password."
                )
            
            # Update user password
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_obj.is_used = True
            reset_obj.save()
            
            # Invalidate all other reset tokens for this user
            PasswordReset.objects.filter(user=user, is_used=False).update(is_used=True)
            
            return ResetPassword(
                success=True,
                message="Password has been reset successfully. You can now sign in with your new password.",
                error=None
            )
            
        except PasswordReset.DoesNotExist:
            return ResetPassword(
                success=False,
                error="Invalid reset token"
            )




class SetupSecurityQuestion(graphene.Mutation):
    class Arguments:
        question = graphene.String(required=True)
        answer = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, question, answer):
        user = info.context.user
        
        if not user.is_authenticated:
            return SetupSecurityQuestion(
                success=False,
                error="Authentication required"
            )
        
        if not question or not answer:
            return SetupSecurityQuestion(
                success=False,
                error="Question and answer are required"
            )
        
        try:
            sq, created = SecurityQuestion.objects.get_or_create(user=user)
            sq.question = question
            sq.set_answer(answer)
            sq.save()
            
            return SetupSecurityQuestion(
                success=True,
                message="Security question saved successfully",
                error=None
            )
        except Exception as e:
            logger.exception("SetupSecurityQuestion failed for user %s", info.context.user)
            return SetupSecurityQuestion(
                success=False,
                error="An unexpected error occurred."
            )


class GetSecurityQuestion(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    question = graphene.String()
    question_key = graphene.String()

    @staticmethod
    def mutate(root, info, username):
        try:
            user = User.objects.get(username=username)
            sq = user.security_question
            
            return GetSecurityQuestion(
                success=True,
                question=sq.get_question_display(),
                question_key=sq.question,
                error=None
            )
        except (User.DoesNotExist, SecurityQuestion.DoesNotExist):
            return GetSecurityQuestion(
                success=False,
                error="User not found or no security question set",
                question=None,
                question_key=None
            )


class VerifySecurityAnswer(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        answer = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    message = graphene.String()
    otp = graphene.String()

    @staticmethod
    def mutate(root, info, username, answer):
        try:
            user = User.objects.get(username=username)
            sq = user.security_question
            
            if not sq.check_answer(answer):
                return VerifySecurityAnswer(
                    success=False,
                    error="Incorrect answer. Try again.",
                    message=None,
                    otp=None
                )
            
            # Correct answer - generate OTP
            PasswordResetOTP.objects.filter(user=user, is_used=False).delete()
            otp = PasswordResetOTP.generate_otp()
            PasswordResetOTP.objects.create(user=user, otp=otp)
            
            return VerifySecurityAnswer(
                success=True,
                message="Answer correct! Use the OTP below to reset your password.",
                otp=otp,
                error=None
            )
            
        except (User.DoesNotExist, SecurityQuestion.DoesNotExist):
            return VerifySecurityAnswer(
                success=False,
                error="User not found or no security question set",
                message=None,
                otp=None
            )


class ResetPasswordWithOTP(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        otp = graphene.String(required=True)
        new_password = graphene.String(required=True)

    success = graphene.Boolean()
    error = graphene.String()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, username, otp, new_password):
        if len(new_password) < 8:
            return ResetPasswordWithOTP(
                success=False,
                error="Password must be at least 8 characters long"
            )
        
        try:
            user = User.objects.get(username=username)
            otp_record = PasswordResetOTP.objects.filter(
                user=user, otp=otp, is_used=False
            ).latest('created_at')
            
            if not otp_record.is_valid():
                return ResetPasswordWithOTP(
                    success=False,
                    error="OTP has expired. Please start over."
                )
            
            # Reject if new password is the same as current password
            if user.check_password(new_password):
                return ResetPasswordWithOTP(
                    success=False,
                    error="New password must be different from your current password."
                )
            
            # Reset password
            user.set_password(new_password)
            user.save()
            
            # Mark OTP as used
            otp_record.is_used = True
            otp_record.save()
            
            return ResetPasswordWithOTP(
                success=True,
                message="Password reset successful! Please log in.",
                error=None
            )
            
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return ResetPasswordWithOTP(
                success=False,
                error="Invalid OTP or user."
            )


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Smart Expert System for Mental Health Backend API is LIVE!")
    me = graphene.Field(UserType)
    therapists = graphene.List(TherapistType)
    therapist = graphene.Field(TherapistType, id=graphene.Int(required=True))
    ai_chat_messages = graphene.List(AIChatMessageType)

    def resolve_me(self, info):
        return info.context.user if info.context.user.is_authenticated else None

    def resolve_therapists(self, info):
        return (
            Therapist.objects
            .prefetch_related('specialization', 'reviews')
            .annotate(
                _review_count=models.Count('reviews'),
                _avg_rating=models.Avg('reviews__rating'),
            )
        )

    def resolve_therapist(self, info, id):
        try:
            return (
                Therapist.objects
                .prefetch_related('specialization', 'reviews')
                .annotate(
                    _review_count=models.Count('reviews'),
                    _avg_rating=models.Avg('reviews__rating'),
                )
                .get(pk=id)
            )
        except Therapist.DoesNotExist:
            return None

    def resolve_ai_chat_messages(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return AIChatMessage.objects.none()
        return AIChatMessage.objects.filter(user=user).order_by("created_at")


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    sign_in = SignIn.Field()
    sign_up = SignUp.Field()
    update_profile = UpdateProfile.Field()
    upload_profile_picture = UploadProfilePicture.Field()
    remove_profile_picture = RemoveProfilePicture.Field()
    send_ai_chat_message = SendAIChatMessage.Field()
    forgot_password = ForgotPassword.Field()
    reset_password = ResetPassword.Field()
    # Security Question & OTP System
    setup_security_question = SetupSecurityQuestion.Field()
    get_security_question = GetSecurityQuestion.Field()
    verify_security_answer = VerifySecurityAnswer.Field()
    reset_password_with_otp = ResetPasswordWithOTP.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)