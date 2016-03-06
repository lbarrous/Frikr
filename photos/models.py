# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from photos.settings import LICENSES
from photos.validators import badwords_detector

PUBLIC = 'PUB'
PRIVATE = 'PRI'

VISIBILITY = (
    (PUBLIC, 'Pública'),
    (PRIVATE, 'Privada')
)

class Photo(models.Model):
    name = models.CharField(max_length=150)
    url = models.URLField()
    description = models.TextField(blank=True, null=True, default="", validators=[badwords_detector])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    license = models.CharField(max_length=3, choices=LICENSES)
    owner = models.ForeignKey(User)
    visibility = models.CharField(max_length=3, choices=VISIBILITY, default=PUBLIC)

    def __unicode__(self): #Metodo con 0 parametros --> Aunque aparezca self, este no cuenta nunca
        return self.name
