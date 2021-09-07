from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.expressions import OrderBy


# INFO  BlogUserManager
class BlogUserManager(BaseUserManager):
    "creates and returns a new user instance"

    def create_user(self, firstname, lastname, email, password):
        user = self.model(firstname=firstname, lastname=lastname,
                          email=self.normalize_email(email))
        user.save(using=self._db)
        user.set_password(password)
        user.save()
        return user

    "Creates and returns  a new user instance with the admin privileges"

    def create_superuser(self, firstname, lastname, email, password):
        user = self.create_user(
            firstname=firstname, lastname=lastname, email=email, password=password)
        user.is_admin = True
        user.save()
        return user


# INFO Custom User Model
class BlogUser(AbstractBaseUser):
    firstname = models.CharField(max_length=35)
    lastname = models.CharField(max_length=35)

    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']
    objects = BlogUserManager()

    class Meta:
        verbose_name = 'Blog user'
        verbose_name_plural = 'Blog users'
        ordering = ['firstname', 'lastname']

    def __str__(self) -> str:
        return self.get_full_name()

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, app=None):
        return True

    def has_perm(self, app_label=None):
        return True

    def get_full_name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)
