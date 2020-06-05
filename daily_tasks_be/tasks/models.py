from django.db import models
from authentication.models import User

# Create your models here.


class Tasks(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_on = models.DateField(auto_now=True)
    task_date = models.DateField(null=True)
    completed_date = models.DateField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                              null=True)

    def __str__(self):
        return self.title
