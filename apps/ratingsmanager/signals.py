from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import RatingVote


@receiver(post_delete, sender=RatingVote)
def calculate_ratings(sender, instance, **kwargs):
    instance.rating.calculate()
