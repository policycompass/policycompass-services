from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, \
    MaxValueValidator
import logging

log = logging.getLogger(__name__)


class Rating(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    votes_counter = models.PositiveIntegerField(default=0)
    score = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def calculate(self):
        """
        Recalculate the totals, and save.
        """
        aggregates = self.rating_votes.aggregate(count=models.Count('score'),
                                                 score=models.Avg('score'))
        score = aggregates.get('score')
        # round score to the nearest 0.5
        score *= 2
        score = round(score)
        score /= 2
        self.votes_counter = aggregates.get('count') or 0
        self.score = score or 0.0
        self.save()


class RatingVote(models.Model):
    rating = models.ForeignKey(Rating, related_name='rating_votes')
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    user_identifier = models.CharField(max_length=1024, validators=[
        RegexValidator("^(/[^/]*)+/?$")])
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("rating", "user_identifier")
