from tabnanny import verbose

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import Model
from django.template.base import kwarg_re

from django.urls import reverse


class UserManager(BaseUserManager):
    def create_user(self, username, firstname, lastname, password=None):
        if not firstname or not lastname or not username:
            raise ValueError("Users must have a firstname, lastname and username!")

        user = self.model(username=username, firstname=firstname, lastname=lastname)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, firstname, lastname, password):
        user = self.create_user(username, firstname, lastname, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=False, unique=True)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        db_table = "users"

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users',
        blank=True,
    )

    def __str__(self):
        return self.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        verbose_name = 'User\'s posts'
        verbose_name_plural = 'User\'s posts'
        ordering = ['-created_at', 'author']
        db_table = "posts"

    def __str__(self):
        return f'{self.pk}) {self.author}: {self.caption[:10]}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_pk': self.pk})

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE,related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user" ,"post")

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class PostTag(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="post_tags")
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, related_name="post_tags")

    class Meta:
        unique_together = ("tag" ,"post")


def user_directory_path(instance, filename):
    return f'images/{instance.post.author.username}/{filename}'

class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=user_directory_path, blank=False)

    def __str__(self):
        return str(self.image)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"