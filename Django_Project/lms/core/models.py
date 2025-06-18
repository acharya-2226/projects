from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Subject and category choices
SUBJECTS = [
    ('BCT001', 'Math'),
    ('BCT002', 'Science'),
    ('BCT003', 'English'),
    ('BCT004', 'History'),
    ('BCT005', 'Geography'),
    ('BCT006', 'Geography'),
]

MATERIALS = [
    ('NOTES', 'Notes'),
    ('VIDEO', 'Video'),
    ('PDF', 'PDF'),
    ('PPT', 'PowerPoint'),
    ('AUDIO', 'Audio'),
    ('IMAGE', 'Image'),
    ('OTHER', 'Other'),
]


class Student(models.Model):
    SEMESTERS = [
        ('SEM_ONE', 'Semester One'),
        ('SEM_TWO', 'Semester Two'),
        ('SEM_THREE', 'Semester Three'),
        ('SEM_FOUR', 'Semester Four'),
        ('SEM_FIVE', 'Semester Five'),
        ('SEM_SIX', 'Semester Six'),
        ('SEM_SEVEN', 'Semester Seven'),
        ('SEM_EIGHT', 'Semester Eight'),
    ]

    full_name = models.CharField(max_length=200, verbose_name="Full name")
    email = models.EmailField(unique=True, verbose_name="Email")
    semester = models.CharField(max_length=20, choices=SEMESTERS, default='N/A', null=True, blank=True)
    phone_no = models.CharField(max_length=15, verbose_name="Phone number")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"
        ordering = ['-full_name']

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    DEPARTMENTS = [
        ('BCA', 'Bachelor of Computer Application'),
        ('BCT', 'Bachelor of Computer Engineering'),
        ('BEI', 'Bachelor of Electronics and Information'),
        ('BCE', 'Bachelor of Civil Engineering'),
    ]

    full_name = models.CharField(max_length=200, verbose_name="Full name")
    email = models.EmailField(unique=True, verbose_name="Email")
    department = models.CharField(max_length=20, choices=DEPARTMENTS, default='N/A', null=True, blank=True)
    phone_no = models.CharField(max_length=15, verbose_name="Phone number")
    join_date = models.DateField(default=datetime.today, verbose_name="Join date")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "teacher"
        verbose_name_plural = "teachers"
        ordering = ['-full_name']

    def __str__(self):
        return self.full_name


class Assignment(models.Model):
    title = models.CharField(max_length=100, verbose_name='Assignment title')
    start_date = models.DateField(default=datetime.today, verbose_name='Start date')
    end_date = models.DateField(default=datetime.today, verbose_name='End date')
    question_file = models.FileField(upload_to='assignments/question/', null=True, blank=True, verbose_name='Question file')
    question = models.TextField(null=True, blank=True, verbose_name='Question description')
    remark = models.CharField(max_length=100, verbose_name='Remark')
    full_mark = models.FloatField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Uploaded by')
    subject = models.CharField(max_length=20, choices=SUBJECTS, default='N/A', verbose_name='Subject')

    class Meta:
        verbose_name = 'assignment'
        verbose_name_plural = 'assignments'
        ordering = ['-title']

    def __str__(self):
        return f"{self.title} ({self.subject})"


class Material(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    category = models.CharField(max_length=20, choices=MATERIALS, default='N/A', verbose_name='Category')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name='Description')
    upload_date = models.DateField(default=datetime.today, verbose_name='Upload date')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Uploaded by')
    subject = models.CharField(max_length=20, choices=SUBJECTS, default='N/A', verbose_name='Subject')
    file = models.FileField(upload_to='materials/', null=True, blank=True, verbose_name='File upload')

    class Meta:
        verbose_name = 'material'
        verbose_name_plural = 'materials'
        ordering = ['-title']

    def __str__(self):
        return f"{self.title} ({self.subject})"
