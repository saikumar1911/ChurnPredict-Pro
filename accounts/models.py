# File: accounts/models.py



# Import section
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Store manager profile keeps track of the user's store and usage stats.
class StoreManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    store_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    total_predictions = models.IntegerField(default=0)
    total_emails_sent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

# Function: __str__
    def __str__(self):
        return f"{self.user.username}'s Profile"

# Automatically create a profile when a new user is created.
@receiver(post_save, sender=User)
# Function: create_user_profile
def create_user_profile(sender, instance, created, **kwargs):
    # If block
    if created:
        StoreManagerProfile.objects.create(user=instance)

# Save the profile after the user is updated.
@receiver(post_save, sender=User)
# Function: save_user_profile
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
