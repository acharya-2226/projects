from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.


SUBJECTS=[
    ('BCT001', 'Math'),
    ('BCT002', 'Science'),
    ('BCT003', 'English'),
    ('BCT004', 'History'),
    ('BCT005', 'Geography'),
    ('BCT006', 'Geography'),
    ]


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
    semester = models.CharField(max_length=20,choices=SEMESTER, default='N/A', null=True, blank=True)
    phone_no = models.IntegerField(null=False,blank=False)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "student"
        verbose_name_plural = "students"
        ordering =['-full_name']

    def __str__(self):
        return self.full_name
        
class Teacher(models.Model):
    DEPARTMENT = {
        ('BCA','Bachelor of Computer Application'),
        ('BCT','Bachelor of Computer Engineering'),
        ('BEI','Bachelor of Electronics and Information'),
        ('BCE','Bachelor of Civil Engineering'),
    }
    full_name = models.CharField(max_length=200, null=False, blank=False, verbose_name="teacher Full Name")
    email = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name="teacher Email")
    department = models.CharField(max_length=20,choices=DEPARTMENT, default='N/A', null=True, blank=True)
    phone_no = models.IntegerField(null=False,blank=False)
    import datetime
    join_data = models.DateField(default=datetime.date.today)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    class Meta:
        verbose_name = "teacher"
        verbose_name_plural = "teachers"
        ordering =['-full_name']

    def __str__(self):
        return self.full_name
    
class Assignment(models.Model):
    title = models.CharField(max_length=100,null=False,verbose_name='Assignment Title')
    import datetime
    start_date = models.DateField(default=datetime.date.today, null=False, blank=False, verbose_name='Start_Date')
    end_date = models.DateField(default=datetime.date.today, null=False, blank=False, verbose_name='End_Date')
    question_file = models.FileField(upload_to='assignments/question/',null=True,blank=True,verbose_name='select_Assignment_file')
    question = models.TextField(null=True,blank=True,verbose_name='Assignment_Question')
    remark = models.CharField(max_length=100,null=False,blank=False,verbose_name='Assignment Details')
    full_mark = models.FloatField(blank=False,null=False)
    teacher =models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name='Uploaded By')
    subject =models.CharField(max_length=20, choices=SUBJECTS, default='N/A', verbose_name='Subject')

    class Meta:
        verbose_name = 'assignment'
        verbose_name_plural = 'assignments'
        ordering =['-title']

    def __str__(self):
        return self.title
    
class Material(models.Model):
    MATERIALS = [
        ('NOTES', 'Notes'),
        ('VIDEO', 'Video'),
        ('PDF', 'PDF'),
        ('PPT', 'PowerPoint'),
        ('AUDIO', 'Audio'),
        ('IMAGE', 'Image'),
        ('OTHER', 'Other'),
    ]

    title = models.CharField(max_length=100,null=False,verbose_name='Material Title')
    category = models.CharField(max_length=20, choices=MATERIALS, null=False, blank=False, default='N\A',verbose_name='category')
    description = models.CharField(max_length=255,null=True,blank=True,verbose_name='Description of Material')
    upload_date = models.DateField(default=datetime.now(), null=False, blank=False, verbose_name='Upload_Date')
    teacher =models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name='Uploaded By')
    subject =models.CharField(max_length=20, choices=SUBJECTS, default='N/A',verbose_name='Subject')
    file = models.FileField(upload_to='material',null=True,blank=True,verbose_name='select_file')
    
    
    class Meta:
        verbose_name = 'material'
        verbose_name_plural = 'materials'
        ordering =['-title']

    def __str__(self):
        return self.title