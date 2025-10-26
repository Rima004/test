from django.db import models

from apps.users.models import User


# Create your models here. will have Task model with title, description and status fields(Choices: Open, In Progress, Completed, Canceled, Archived)


from django.db import models


class Task(models.Model):
    STATUS = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Archived', 'Archived'),
    ]

    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=20, choices=STATUS,default='Open')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.status})"
