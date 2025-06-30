import django.db.models


class Profile(django.db.models.Model):
    user_id = django.db.models.PositiveIntegerField(unique=True)
    username = django.db.models.CharField(unique=True)
    bio = django.db.models.TextField(blank=True)
    avatar_url = django.db.models.URLField(blank=True)

    location = django.db.models.CharField(max_length=100, blank=True)
    birthdate = django.db.models.DateField(null=True, blank=True)

    created_at = django.db.models.DateTimeField(auto_now_add=True)
    updated_at = django.db.models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for User {self.user_id}"
