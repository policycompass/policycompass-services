from django.db import models


class Feedback(models.Model):
    name = models.CharField(max_length=100, default=" ")
    email = models.CharField(max_length=100, default=" ")
    subject = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000, blank=True, default="")
    message = models.TextField()
    comment = models.TextField(default=" ")

    def __str__(self):
        return self.subject
