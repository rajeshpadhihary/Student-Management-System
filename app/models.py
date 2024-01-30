from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class SessionYear(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()


class CustomUser(AbstractUser):
    TYPES = (
        (1,'HOD'),
        (2,'Staff'),
        (3,'Student')
    )
    user_type = models.CharField(default = 1,choices = TYPES,max_length = 10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    fcm_token = models.TextField(default = "")
    objects = models.Manager()


class Course(models.Model):
    id = models.AutoField(primary_key = True)
    course_name = models.CharField(max_length = 300, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()


class Subject(models.Model):
    id = models.AutoField(primary_key = True)
    subject_name = models.CharField(max_length = 300, null = False)
    course_id = models.ForeignKey(Course, on_delete = models.CASCADE,default = 1)
    staff_id = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser,on_delete = models.CASCADE)
    gender = models.CharField(max_length = 200)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Course, on_delete = models.DO_NOTHING)
    session_year_id = models.ForeignKey(SessionYear,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    fcm_token = models.TextField(default = "")
    objects = models.Manager()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject,on_delete = models.DO_NOTHING)
    attendance_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    session_year_id = models.ForeignKey(SessionYear,on_delete = models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete = models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance,on_delete = models.CASCADE)
    status = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()

class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE)
    leave_date = models.CharField(max_length = 200)
    leave_reason = models.TextField()
    leave_status = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff,on_delete = models.CASCADE)
    leave_date = models.CharField(max_length = 200)
    leave_reason = models.TextField()
    leave_status = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class QuaterlyExam(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete = models.CASCADE)
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE)
    total_marks = models.IntegerField(default = 0)
    obtained_marks = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class HalfyearlyExam(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete = models.CASCADE)
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE)
    total_marks = models.IntegerField(default = 0)
    obtained_marks = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class AnnualExam(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete = models.CASCADE)
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE)
    total_marks = models.IntegerField(default = 0)
    obtained_marks = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE)
    subject_id = models.ForeignKey(Subject,on_delete = models.CASCADE)
    EXAM_TYPES = (
        (1,'QUATERLY'),
        (2,'HALFYEARLY'),
        (3,'ANNUAL')
    )
    exam_type = models.CharField(default = 1,choices = EXAM_TYPES,max_length = 10)
    subject_exam_marks = models.FloatField(default = 0)
    marks_out_of = models.FloatField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class FeedbackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class FeedbackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff,on_delete = models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE)
    message = models.TextField()
    notification_status = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

class NotificationStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff,on_delete = models.CASCADE)
    message = models.TextField()
    notification_status = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = models.Manager()

@receiver(post_save,sender = CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin = instance)
        if instance.user_type == 2:
            Staff.objects.create(admin = instance)
        if instance.user_type == 3:
            Student.objects.create(admin = instance,course_id = Course.objects.get(id=1),session_year_id = SessionYear.objects.get(id=1),address = "",profile_pic = "",gender = "")

@receiver(post_save,sender = CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.student.save()
