import datetime

from django.conf import settings

from django.db import models
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# from django.contrib.auth.models.CustomUser import USERNAME_FIELD, EMAIL_FIELD, REQUIRED_FIELDS

# from django.contrib.auth.backends import BaseBackend


# class ZUserManager(BaseUserManager):

#     def create_user(self, email, nickname, password=None):
#         """
#         Create and save a User with the given email, nickname and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             user_id_email=self.normalize_email(email),
#             nick_name=nickname
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user


#     def create_superuser(self, email, nickname, password):
#         """
#         Create and save a superuser with the given email, nickname and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.create_user(
#             email,
#             nickname,
#             password=password
#         )

#         user.is_admin = True
#         user.save(using=self._db)
#         return user


# class ZUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#         )
#     nick_name = models.CharField(max_length=72)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     manage = ZUserManager()

#     USERNAME_FIELD = 'email'
#     EMAIL_FIELD = USERNAME_FIELD
#     REQUIRED_FIELDS = ['nick_name']

#     def __str__(self):
#         return self.email


#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin


# class ZAuthBackend(BaseBackend):

#     def authenticate(self, request, username=None, password=None):
#         # Check the username/password and return a user.
#     # def authenticate(self, request, token=None):
#     #     # Check the token and return a user.
#         login_valid = (settings.ADMIN_LOGIN == username)
#         pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
#         if login_valid and pwd_valid:
#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 # Create a new user. There's no need to set a password
#                 # because only the password from settings.py is checked.
#                 user = User(username=username)
#                 user.is_staff = True
#                 user.is_superuser = True
#                 user.save()
#             return user
#         return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None


class ZProfil(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE
    )  # settings.AUTH_USER_MODEL
    site_web = models.URLField(blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/")
    signature = models.TextField(blank=True)
    inscrit_newsletter = models.BooleanField(default=False)

    def __str__(self):
        return "Profil de {0}".format(self.user.username)


class ZContact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class ZAddress(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ZRole(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
