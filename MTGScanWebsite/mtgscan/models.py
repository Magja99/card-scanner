from django.db import models
import validators
from uuid import UUID, uuid4
import bcrypt as bcrypt
import sqlite3

from django.contrib.auth.models import User


class Card(models.Model):
    name = models.CharField(max_length=200)
    networkName = models.CharField(max_length=200)


class Possesion(models.Model):
    userId = models.ManyToManyField(User)
    cardId = models.ManyToManyField(Card)
