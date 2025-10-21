from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        user = getattr(self, 'user', None)
        if user and hasattr(user, 'username'):
            return str(user.username)
        return str(self.user)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.svg')
    cover_image = models.ImageField(upload_to='cover_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Work(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='works')
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100, blank=True, null=True)
    target_audience = models.CharField(max_length=100, blank=True, null=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, null=True)  # Temporal: permitimos null
    created_at = models.DateTimeField(auto_now_add=True)
    shared_post = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='shares')

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.content and not self.image and not self.shared_post:
            raise ValidationError('La publicación debe tener texto, una imagen o ser un post compartido.')

    def __str__(self):
        return str(self.title)

    @property
    def upvotes(self):
        return self.votes.filter(vote_type=Vote.UPVOTE).count()

    @property
    def downvotes(self):
        return self.votes.filter(vote_type=Vote.DOWNVOTE).count()

    @property
    def score(self):
        return self.upvotes - self.downvotes

class Vote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = (
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.IntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

class WikiPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)