from django.db import models
from users.models import User

class UserSpam(models.Model) : 
    spammed_by = models.ManyToManyField(User,related_name='spammed_by', blank=True)

    @property
    def spam_counter(self) : 
        return self.spammed_by.all().count()
