from datetime import timezone

from django.conf import settings
from django.contrib.auth.models import AbstractUser,UserManager
from django.db import models

from django.utils.translation import gettext_lazy as _

from django.utils import timezone

# Create your models here.
Gender = (
    ('Male','Male'),
    ('Female','Female'),
)
Mail_Choices = (
    ('Activation notification','Activation notification'),
    ('Decline notification','Decline notification'),
)
User_Choices = (
    ('User','User'),
    ('Company','Company'),
)
USER_MODEL = settings.AUTH_USER_MODEL

class MyUserManager(UserManager):


    def _create_user(self, email, password, **extra_fields):
        """
         Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
             raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)



class MyUser(AbstractUser):
    email = models.EmailField(_('Email address'), unique=True)
    first_name = models.CharField(_('First name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last name'), max_length=30, blank=True)

    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=40, choices=Gender,default='Male')
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)

    profile_picture = models.ImageField(
        upload_to='profile_images', null=True, blank=True
    )

    gov_id = models.CharField(
        db_index=True,
        blank=True,
        null=True,
        max_length=30,
        help_text=_("Şəxsiyyət vəsiqəsinin nömrəsi"),
    )
    voen_code = models.CharField(
        _("VÖEN Kod"),
        db_index=True,
        blank=True,
        null=True,
        max_length=30,
        help_text=_("Şəxsi VÖEN"),
    )
    client_code = models.CharField(
        db_index=True, unique=True, blank=True, null=True, max_length=30, editable=False
    )
    user_choices = models.CharField(choices=User_Choices,max_length = 100,default="User")
    social_media = models.CharField(max_length=100, blank=True,null=True)
    mail_choices = models.CharField(choices=Mail_Choices,max_length = 100, null=True, blank=True)
    activation_mail_sent = models.BooleanField(
        _("Activation mail sent"),
        default=False,
        help_text=_("It will change after sending activation mail"),
        db_index=True,
    )
    decline_mail_sent = models.BooleanField(
        _("Decline mail sent"),
        default=False,
        help_text=_("It will change after sending decline mail"),
        db_index=True,
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )
    is_company_active = models.BooleanField(default=False)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    last_activity = models.DateTimeField(_("last activity"), blank=True, null=True)
    username = None
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_full_name(self):
        """
            Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
            Returns the short name for the user.
        """
        return self.first_name
