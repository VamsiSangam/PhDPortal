"""
Definition of models.
"""

from django.db import models
from django.forms import ModelForm

# Create your models here.

class User(models.Model):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USER_TYPES = (
        ('S', 'Student'),
        ('G', 'Guide'),
        ('D', 'Director'),
        ('R', 'Referee'),
    )

    username = models.CharField(max_length = 30, primary_key = True)
    email_id = models.CharField(max_length = 30, null = False)
    type = models.CharField(max_length = 1, choices = USER_TYPES)
    first_name = models.CharField(max_length = 50, blank = True)
    last_name = models.CharField(max_length = 50, blank = True)
    address = models.TextField(max_length = 250, blank = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class StatusTypes(models.Model):
    class Meta:
        verbose_name = 'Status Type'
        verbose_name_plural = 'Status Types'

    id = models.PositiveIntegerField(primary_key = True)
    status_message = models.CharField(max_length = 50, null = False)

    def __str__(self):
        return self.status_message

class Thesis(models.Model):
    class Meta:
        verbose_name = 'Thesis'
        verbose_name_plural = 'Thesis'

    username = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 150, null = False)
    abstract = models.TextField(max_length = 500, null = True)
    synopsis = models.FileField(upload_to = 'Synopsis', null = True)
    thesis = models.FileField(upload_to = 'Thesis', null = True)
    status = models.ForeignKey(StatusTypes, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class SynopsisForm(ModelForm):
    class Meta:
        model = Thesis
        fields = ['synopsis']

class ThesisForm(ModelForm):
    class Meta:
        model = Thesis
        fields = ['thesis']

class ThesisGuides(models.Model):
    class Meta:
        verbose_name = 'Thesis Guide'
        verbose_name_plural = 'Thesis Guides'

    GUIDE_TYPES = (
        ('G', 'Guide'),
        ('C', 'Co-Guide'),
    )

    thesis_id = models.ForeignKey(Thesis, on_delete = models.CASCADE)
    guide_username = models.ForeignKey(User, on_delete = models.CASCADE)
    type = models.CharField(max_length = 1, choices = GUIDE_TYPES)

    def __str__(self):
        return self.guide_username.first_name + ' ' + self.guide_username.last_name

class IEEEKeywords(models.Model):
    class Meta:
        verbose_name = 'IEEE Keyword'
        verbose_name_plural = 'IEEE Keywords'

    keyword = models.CharField(max_length = 50, null = False)
    parent_keyword_id = models.ForeignKey('self', on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.keyword

class ThesisKeywords(models.Model):
    class Meta:
        verbose_name = 'Thesis Keyword'
        verbose_name_plural = 'Thesis Keywords'
        unique_together = (('thesis_id', 'keyword_id'),)
    thesis_id = models.ForeignKey(Thesis, on_delete = models.CASCADE)
    keyword_id = models.ForeignKey(IEEEKeywords, on_delete = models.CASCADE)

    def __str__(self):
        return 'Keyword ' + self.keyword_id.keyword + ' ' + ' for ' + self.thesis_id.title

class PanelMembers(models.Model):
    class Meta:
        verbose_name = 'Panel Member'
        verbose_name_plural = 'Panel Members'

    STATUS_TYPES = (
        ('U', 'Not yet decided'),
        ('Y', 'Approved'),
        ('N', 'Declined'),
    )

    thesis_id = models.ForeignKey(Thesis, on_delete = models.CASCADE)
    referee_username = models.ForeignKey(User, on_delete = models.CASCADE)
    priority = models.PositiveIntegerField(null = True)
    status = models.CharField(max_length = 1, choices = STATUS_TYPES)

    def __str__(self):
        return self.refereee_username.first_name

class Notifications(models.Model):
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    STATUS_TYPES = (
        ('R', 'Read'),
        ('U', 'Unread'),
    )

    #username = models.ForeignKey(User, on_delete = models.CASCADE)
    sender = models.ForeignKey(User, null = True, related_name = 'sender', on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, null = True, related_name = 'receiver', on_delete = models.CASCADE)
    message = models.TextField(max_length = 200, null = False)
    link = models.CharField(max_length = 200, null = True)
    status = models.CharField(max_length = 1, choices = STATUS_TYPES)
    date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.receiver.first_name + ' notification'