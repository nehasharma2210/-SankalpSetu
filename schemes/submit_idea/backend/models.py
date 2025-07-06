
from django.db import models

class Idea(models.Model):
    language = models.CharField(max_length=50)
    idea = models.TextField()

    def __str__(self):
        return self.language