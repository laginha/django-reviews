import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from reviews.managers import *


class Vote(models.Model):
    """
    A vote for or against a Review.
    
    This let's users rate up or down a review that they found useful.
    
    Usage::
        
        >>> vote = Vote(like=True, user=1, review=1)
        >>> review.votes.add(vote)
    
    """
    like = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('user'), 
        related_name='reviews_votes', blank=True, null=True)
    ip_address = models.IPAddressField(blank=True)
    review = models.ForeignKey('ReviewedItem', verbose_name=_('review'), 
        related_name='reviews_votes')
    date_added = models.DateTimeField(_('date added'), 
        default=datetime.datetime.now, editable=False)
    date_changed = models.DateTimeField(_('date changed'), 
        default=datetime.datetime.now, editable=False)
    
    objects = VoteManager()
    
    class Meta:
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
    
    def save(self, *args, **kwargs):
        self.date_changed = datetime.datetime.now()
        super(Vote, self).save(*args, **kwargs)
    
    def __unicode__(self):
        
        # Get their vote; either up or down.
        if self.like:
            v = "up"
        else:
            v = "down"
        
        # Get the user string
        if self.user != None:
            u = "%s [%s]" % (self.user.username, self.ip_address)
        else:
            u = "[%s]" % self.ip_address
        
        return u"%s voted %s Review #%s" % (u, v, 
            self.review.id)
    

class ReviewedItem(models.Model):
    """
    A generic ReviewedItem of a Django Model.
    """
    content_type = models.ForeignKey(
        ContentType,
        related_name = "reviews",
        editable = False)

    object_id = models.PositiveIntegerField(
        editable = False)

    score = models.IntegerField(
        verbose_name = _('Rating'))

    content = models.TextField(
        verbose_name = _('Review'))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name = 'reviews',
        editable = False)

    date_added = models.DateTimeField(
        auto_now_add = True,
        editable = False)

    date_changed = models.DateTimeField(
        auto_now = True,
        editable = False)
    
    content_object = generic.GenericForeignKey()
    
    objects = ReviewedItemManager()
    
    # TODO: Add flagging of reviews...
    
    class Meta:
        ordering = ('date_added',)
        verbose_name = _('reviewed item')
        verbose_name_plural = _('reviewed items')
        # unique_together = (('content_type', 'object_id', 'key', 'user')) #, 'ip_address'
    
    def save(self, *args, **kwargs):
        self.date_changed = datetime.datetime.now()
        super(ReviewedItem, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return u"Review of %s by %s" % (self.content_object, self.user.username)

