"""
Definition of models.
"""

from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from app.choices import *
# Create your models here.

class Section(models.Model):
    name = models.CharField(max_length=65)
    section_slug = models.CharField(max_length=65)
    section_head = models.ForeignKey(User, models.PROTECT, blank=False, null=False)

    def __str__(self):
        return self.name

class App(models.Model):
    name = models.CharField(max_length=65)
    favicon = models.CharField(max_length=65, default='wpforms')
    section = models.ForeignKey(Section, models.PROTECT, blank=False, null=False)

    def __str__(self):
        return '%s -> %s' % (self.section, self.name)

class MenuTemplate(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return '%s' % (self.name)

class Menu(models.Model):
    name = models.CharField(max_length=65)
    url = models.CharField(max_length=255)
    app = models.ForeignKey(App, models.CASCADE, blank=False, null=False)
    menu_templates = models.ManyToManyField(MenuTemplate)
    sort_order = models.IntegerField()

    def __str__(self):
        return '%s -> %s' % (self.app,self.name)

    class Meta:
        ordering = ('sort_order',)

class UserProfile(models.Model):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    salutation = models.CharField(max_length=12, choices=SALUTATION_CHOICES)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    menu_template = models.ForeignKey(MenuTemplate, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return "UserProfile of %s %s %s" % (self.salutation,self.user.first_name,self.user.last_name)

class Program(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=65)
    location = models.CharField(max_length=65)
    course_approval_authority = models.CharField(max_length=65)
    type = models.CharField(max_length=65, choices=PROGRAMTYPE_CHOICE)

class AdmissionBatch(models.Model):
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, blank=True, null=True)
    admission_year = models.IntegerField()
    session = models.CharField(max_length=4, choices=(('Jan', 'Jan'), ('June', 'June')))
    enrollment_prefix = models.CharField(max_length=30)

    def __str__(self):
        return "%s (%s), %s, %s %d" % (
            self.program.name, self.program.department, self.program.location, self.session, self.admission_year)

class Student(models.Model):
    first_name = models.CharField(max_length=65)
    middle_name = models.CharField(max_length=65, blank=True, null=True)
    last_name = models.CharField(max_length=65, blank=True, null=True)
    current_batch = models.ForeignKey(AdmissionBatch, on_delete=models.CASCADE, verbose_name='Batch')
    current_roll_no = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name='Your Gender')
    category = models.CharField(max_length=8, choices=ADM_CATEGORY_CHOICES, default='GEN', verbose_name='Your Category')
    admission_category = models.CharField(max_length=8, choices=ADM_CATEGORY_CHOICES, default='GEN',
                                          verbose_name='Admission Category')
    admission_channel = models.CharField(max_length=25)
    sponsored = models.BooleanField(choices=BOOL_CHOICES, default=False, editable=False)
    email = models.EmailField(max_length=50)
    ldap_id = models.CharField(max_length=65)
    phone_regex = RegexValidator(regex=r'^\+91-\d{10}$', \
                                 message="Phone number must be entered in the format: '+91-9830098300'. +91 is the country code of India.")
    phone_number = models.CharField(validators=[phone_regex], default='+91-', max_length=16,
                                    verbose_name='Mobile Number')
    aadhar_regex = RegexValidator(regex=r'^\d{4}\s\d{4}\s\d{4}$', \
                                  message="Aadhar number must be entered in the format: '1111 1111 1111'.")
    aadhar_number = models.CharField(validators=[aadhar_regex], max_length=14, blank=True, null=True)
    phone_activated = models.BooleanField(choices=BOOL_CHOICES, default=False, editable=False)
    activated = models.BooleanField(choices=BOOL_CHOICES, default=False, editable=False)
    created_on = models.DateTimeField(editable=False, blank=True, null=True)
    activated_on = models.DateTimeField(blank=True, null=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    user = models.OneToOneField(User, null = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Faculty(models.Model):
    first_name = models.CharField(max_length = 65)
    middle_name = models.CharField(max_length = 65, blank = True, null = True)
    last_name = models.CharField(max_length = 65, blank = True, null = True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, default = 'M', verbose_name = 'Your Gender')
    designation = models.CharField(max_length = 30, choices = DESIG_CHOICES, default = 'Prof', verbose_name = 'Your Designation')
    email = models.EmailField(max_length = 50)
    ldap_id = models.CharField(max_length = 65)
    phone_regex = RegexValidator(regex = r'^\+91-\d{10}$', \
                                 message = "Phone number must be entered in the format: '+91-9830098300'. +91 is the country code of India.")
    phone_number = models.CharField(validators = [phone_regex], default = '+91-', max_length = 16,
                                    verbose_name = 'Mobile Number')
    aadhar_regex = RegexValidator(regex = r'^\d{4}\s\d{4}\s\d{4}$', \
                                  message = "Aadhar number must be entered in the format: '1111 1111 1111'.")
    aadhar_number = models.CharField(validators = [aadhar_regex], max_length = 14, blank = True, null = True)
    phone_activated = models.BooleanField(choices = BOOL_CHOICES, default = False, editable = False)
    activate = models.BooleanField(choices = BOOL_CHOICES, default = False, editable = False)
    created_on = models.DateTimeField(editable = False, blank = True, null = True)
    activated_on = models.DateTimeField(blank = True, null = True, editable = False)

    last_updated = models.DateTimeField(auto_now=True, editable=False)
    user = models.OneToOneField(User, null = True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class State(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'indian_state'

class CommunicationAddress(models.Model):
    type = models.CharField(editable=False,choices=ADDRESS_TYPE, max_length=20)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150, blank=True, null=True, default='')
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length = 20)
    district = models.CharField(max_length=150, choices=DISTRICTS_CHOICE)  # other for foreign referee
    state = models.ForeignKey(State,on_delete=None)
    country = models.CharField(max_length=150)
    referee = models.ForeignKey('Referee', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True,editable=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ("type", "referee")
        db_table = 'app_address'

    def __str__(self):
        return '%s,\n%s,\n%s,%s,\n%s - %s' % (self.address_line1, self.address_line2, self.city, self.district, self.state, self.pincode)

class Referee(models.Model):
    class Meta:
        verbose_name = 'Referee'
        verbose_name_plural = 'Referees'

    user = models.OneToOneField(User, null = True)
    type = models.CharField(max_length = 1, choices = REFEREE_TYPES)
    university = models.CharField(max_length = 100)
    designation = models.CharField(max_length = 30, choices = DESIG_CHOICES, default = 'Prof', verbose_name = 'Your Designation')
    website = models.CharField(max_length = 150)    # use URL validator in django forms / model

class Approver(models.Model):
    faculty = models.OneToOneField(
            Faculty,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            editable=False
        )
    active = models.BooleanField(default = False)

class StatusType(models.Model):
    class Meta:
        verbose_name = 'Status Type'
        verbose_name_plural = 'Status Types'

    id = models.PositiveIntegerField(primary_key = True)
    status_message = models.CharField(max_length = 50, null = False)
    
    def __str__(self):
        return self.status_message

class ThesisLog(models.Model):
    thesis = models.ForeignKey('Thesis')
    status_type = models.ForeignKey(StatusType)
    date = models.DateTimeField(auto_now = True)

class Thesis(models.Model):
    class Meta:
        verbose_name = 'Thesis'
        verbose_name_plural = 'Thesis'

    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    title = models.CharField(max_length = 150, null = False)
    abstract = models.TextField(max_length = 500, null = True, blank = True)
    synopsis = models.FileField(upload_to = 'Synopsis', null = True, blank = True)
    thesis = models.FileField(upload_to = 'Thesis', null = True, blank = True)
    status = models.ForeignKey(StatusType, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class ThesisGuide(models.Model):
    class Meta:
        verbose_name = 'Thesis Guide'
        verbose_name_plural = 'Thesis Guides'

    thesis = models.ForeignKey(Thesis, on_delete = models.CASCADE)
    guide = models.ForeignKey(Faculty, on_delete = models.CASCADE)
    type = models.CharField(max_length = 1, choices = GUIDE_TYPES)

    def __str__(self):
        return self.guide.first_name + ' ' + self.guide.last_name

class ThesisGuideApproval(models.Model):
    class Meta:
        verbose_name = 'Thesis Guide Approval'
        verbose_name_plural = 'Thesis Guide Approvals'

    thesis = models.ForeignKey(Thesis, on_delete = models.CASCADE)
    guide = models.ForeignKey(Faculty, on_delete = models.CASCADE)
    type = models.CharField(max_length = 1, choices = GUIDE_APPROVAL_TYPES)

    def __str__(self):
        return self.thesis.title

class IEEEKeyword(models.Model):
    class Meta:
        verbose_name = 'IEEE Keyword'
        verbose_name_plural = 'IEEE Keywords'

    keyword = models.CharField(max_length = 100, null = False)
    parent = models.ForeignKey('self', on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.keyword

class ThesisKeyword(models.Model):
    class Meta:
        verbose_name = 'Thesis Keyword'
        verbose_name_plural = 'Thesis Keywords'
        unique_together = (('thesis', 'keyword'),)
    thesis = models.ForeignKey(Thesis, on_delete = models.CASCADE)
    keyword = models.ForeignKey(IEEEKeyword, on_delete = models.CASCADE)

    def __str__(self):
        return 'Keyword ' + self.keyword.keyword + ' ' + ' for ' + self.thesis.title

class PanelMember(models.Model):
    class Meta:
        verbose_name = 'Panel Member'
        verbose_name_plural = 'Panel Members'

    thesis = models.ForeignKey(Thesis, on_delete = models.CASCADE)
    referee = models.ForeignKey(Referee, on_delete = models.CASCADE)
    status = models.CharField(max_length = 1, choices = PANEL_MEMBER_STATUS_TYPES)
    priority = models.PositiveIntegerField(default = 0)
    added_by = models.ForeignKey(Faculty, on_delete = models.CASCADE)
    created_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.referee.user.first_name

class Notification(models.Model):
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    sender = models.ForeignKey(User, null = True, related_name = 'sender', on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, null = True, related_name = 'receiver', on_delete = models.CASCADE)
    message = models.TextField(max_length = 200, null = False)
    link = models.CharField(max_length = 200, null = True)
    status = models.CharField(max_length = 1, choices = NOTIFICATION_STATUS_TYPES)
    date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.receiver.first_name + ' notification'