from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Student(models.Model):

    SEMESTER = [
        ('SEM_ONE', 'Semester One'),
        ('SEM_TWO', 'Semester Two'),
        ('SEM_THREE', 'Semester Three'),
        ('SEM_FOUR', 'Semester Four'),
        ('SEM_FIVE', 'Semester Five'),
        ('SEM_SIX', 'Semester Six'),
        ('SEM_SEVEN', 'Semester Seven'),
        ('SEM_EIGHT', 'Semester Eight'),
    ]
    full_name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Student Full Name")
    email = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Student Email")
    semester = models.Field(choices=SEMESTER, default='N/A', null=True, blank=True)
    phone_no = models.IntegerField(null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"
        ordering = ['-full_name']

        def __str__(self):
            return self.full_name
        



class Teacher(models.Model):

    
    DEPARTMENT = [
        ('BCE', 'Bachlor in Civil Engineering'),
        ('BEI', 'Bachlor in Electronics Engineering'),
        ('BAR', 'Bachlor in Architecture'),
        ('BCT', 'Bachlor in Computer Engineering'),
        ('CSIT', 'Bachlor in Computer Science Information Technology'),
        ('BCA', 'Bachlor in Compouer Application'),
        ]
    full_name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Teacher Full Name")
    email = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="Teacher Email")
    department = models.Field(choices=DEPARTMENT, default='N/A', null=True, blank=True)
    phone_no = models.IntegerField(null=False, blank=False)
    join_date = models.DateField(default='Join Date')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "teacher"
        verbose_name_plural = "teachers"
        ordering = ['-full_name']

        def __str__(self):
            return self.full_name
    