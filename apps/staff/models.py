from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class Staff(models.Model):
  STATUS = [
      ('active', 'Active'),
      ('inactive', 'Inactive')
  ]

  GENDER = [
      ('male', 'Male'),
      ('female', 'Female')
  ]

  current_status = models.CharField(max_length=10, choices=STATUS, default='active')
  registration_number = models.CharField(max_length=200, unique=True)
  surname = models.CharField(max_length=200)
  firstname = models.CharField(max_length=200)
  middle_name = models.CharField(max_length=200, blank=True)
  gender = models.CharField(max_length=10, choices=GENDER, default='male')
  date_of_birth = models.DateField(default=timezone.now)
  date_of_joining = models.DateField(default=timezone.now)

  mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
  mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)
  
  address = models.TextField(blank=True)
  remarks = models.TextField(blank=True)

  def __str__(self):
    return f'{self.firstname} {self.middle_name} {self.surname}'