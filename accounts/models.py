from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import CASCADE


# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password):
        if not username:
            raise ValueError("Please enter a username")
        if not first_name or first_name == '':
            raise ValueError("Please enter your first name")

        user = self.model(username=username, first_name=first_name, last_name=last_name, password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password):
        user = self.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Account(AbstractBaseUser):
    username = models.CharField(default='', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(default='', max_length=30)
    last_name = models.CharField(default='', max_length=30)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# Create your models here.
class Profile(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    num_of_followers = models.IntegerField(default=0)
    name = models.CharField(default='', max_length=100)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Repository(models.Model):
    name = models.CharField(default='', max_length=100)
    stars = models.IntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
