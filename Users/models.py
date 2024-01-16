from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, mobile, password=None, password2=None):
        """
        Creates and saves a User with the given email, category, first_name,last_name, email, address, country, state, phone, fax and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            first_name = first_name,
            last_name=last_name,
            email=self.normalize_email(email),    
            mobile=mobile,                            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, mobile, password=None):
        """
        Creates and saves a superuser with the given email, category, first_name,last_name, email, address, country, state, phone, fax and password.
        """
        user = self.create_user(
            first_name = first_name,
            last_name=last_name, 
            email=email,
            mobile=mobile,
            password=password,                                 
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True, editable=False)  
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255, blank=False)
    mobile =models.BigIntegerField(blank=True, null=True) 
    address = models.CharField(max_length=500, blank=True, null=True)       
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_login = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "mobile"]

    def __str__(self):        
        return self.first_name+" "+self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
