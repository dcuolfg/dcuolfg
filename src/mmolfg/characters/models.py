"""
Models for characters in mmolfg.
"""

import datetime

from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from mmolfg.characters.managers import CharacterManager


class Character(models.Model):
    """Characters used by Players in DCUO."""

    CHARACTER_SERVER_CHOICES = (
        (0, 'USPS3'),
        (1, 'USPC'),
        (2, 'EUPS3'),
        (3, 'EUPC'),
    )

    CHARACTER_ROLE_CHOICES = (
        (0, 'DPS'),
        (1, 'Controller'),
        (2, 'Healer'),
        (3, 'Tank'),
    )

    CHARACTER_POWERSET_CHOICES = (
        (0, 'Fire'),
        (1, 'Ice'),
        (2, 'Gadgets'),
        (3, 'Mental'),
        (4, 'Light'),
        (5, 'Socery'),
        (6, 'Nature'),
        (7, 'Electricity'),
    )

    player = models.ForeignKey(User, related_name='characters')
    name = models.CharField(max_length=75)
    server = models.IntegerField(choices=CHARACTER_SERVER_CHOICES)
    role = models.IntegerField(choices=CHARACTER_ROLE_CHOICES)
    powerset = models.IntegerField(choices=CHARACTER_POWERSET_CHOICES)
    description = models.TextField(blank=True)
    level = models.IntegerField(
        blank=True, null=True, default=1,
        validators=[MinValueValidator(0), MaxValueValidator(30)])
    combat_rating = models.IntegerField(null=True, blank=True, default=0)
    skill_points = models.IntegerField(blank=True, null=True, default=0)

    # The dates make use of auto_now and auto_now_add options, but
    # also include a "default" value.  This is so that Character objects
    # work sanely without having to call save on them.
    date_added = models.DateTimeField(
        auto_now_add=True, auto_now=False, default=datetime.datetime.now)
    date_updated = models.DateTimeField(
        auto_now_add=True, auto_now=True, default=datetime.datetime.now)

    objects = CharacterManager()

    # XXX: Still need the following attributes:
    #
    # >> +1 votes
    # >> images

    class Meta:
        """Metadata for Character model."""
        unique_together = ('server', 'name')
        db_table = 'characters'
        get_latest_by = 'date_added'

    def __unicode__(self):
        """Used to describe each object in admin."""
        return u'%s: %s' % (self.get_server_display(), self.name)

    def get_server_value(self, server_name):
        """Return the server value to store based on server name."""
        server_value = [
            srv[0] for srv in self.CHARACTER_SERVER_CHOICES
            if srv[1] == server_name]
        if len(server_value) == 1:
            return server_value[0]
        return None

    # XXX: Not sure how to model the "looking_for bit yet."
