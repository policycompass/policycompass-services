from django.db import models


class Feedback(models.Model):
    name = models.CharField(max_length=100, default=" ")
    email = models.CharField(max_length=100, default=" ")
    subject = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000, blank=True, default="")
    message = models.TextField()
    comment = models.TextField(default=" ")
    category_id = models.IntegerField(blank=True, null=True)

    # Auto-Generated Metadata
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class FeedbackCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Feedback Category"
        verbose_name_plural = "Feedback Categories"

    def __str__(self):
        return self.title
