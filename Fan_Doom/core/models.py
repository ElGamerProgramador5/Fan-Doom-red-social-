from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        user = getattr(self, 'user', None)
        if user and hasattr(user, 'username'):
            return str(user.username)
        return str(self.user)


class Work(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='works')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        author = getattr(self.author, 'user', None)
        if author and hasattr(author, 'username'):
            return f"{self.title} ({str(author.username)})"
        return str(self.title)


# Sistema de seguidores/seguidos
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        follower_username = getattr(self.follower, 'username', None)
        followed_username = getattr(self.followed, 'username', None)
        return f"{str(follower_username)} sigue a {str(followed_username)}"


# Relación de seguimiento de obras
class WorkFollow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_follows')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'work')

    def __str__(self):
        return f"{self.user.username} sigue la obra {self.work.title}"


class Fandom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.name)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/', blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True)  # Temporal: permitimos null
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.content and not self.image:
            raise ValidationError('Debes proporcionar texto, imagen o ambos en el post.')

    def __str__(self):
        return str(self.title)

class WikiPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)