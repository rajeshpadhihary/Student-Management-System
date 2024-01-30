from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from app.models import CustomUser,Staff,Course,Attendance,AttendanceReport,Student,Subject,LeaveReportStudent,FeedbackStudent,SessionYear,NotificationStudent,QuaterlyExam,HalfyearlyExam,AnnualExam

def STUDENT_HOME(request):
    student_id = Student.objects.get(admin = request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id = student_id).count()
    attendance_present = AttendanceReport.objects.filter(student_id = student_id,status = True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id = student_id,status = False).count()
    course = Course.objects.get(id = student_id.course_id.id)
    subjects = Subject.objects.filter(course_id = course).count()
    profile_pic = student_id.profile_pic

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subject.objects.filter(course_id = student_id.course_id)

    for i in subject_data:
        attendance = Attendance.objects.filter(subject_id = i.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in = attendance,status = True,student_id = student_id.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in = attendance,status = False,student_id = student_id.id).count()
        subject_name.append(i.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)


    student = Student.objects.filter(admin = request.user.id)
    student_id_n = 0
    for i in student:
        student_id_n = i.id
    student_notification = NotificationStudent.objects.filter(student_id = student_id_n,notification_status = 0).count()
    data = {
        'profile_pic':profile_pic,
        'attendance_total':attendance_total,
        'attendance_present':attendance_present,
        'attendance_absent':attendance_absent,
        'subjects':subjects,
        'subject_name':subject_name,
        'data_present':data_present,
        'data_absent':data_absent,
        'student_notification':student_notification,
    }
    return render(request,'student_template/student_home.html',data)



def student_view_attendance(request):
    student = Student.objects.get(admin = request.user.id)
    profile_pic = student.profile_pic
    course = student.course_id
    subjects = Subject.objects.filter(course_id = course)
    data = {
        'subjects':subjects,
        'profile_pic':profile_pic
    }
    return render(request,"student_template/student_view_attendance.html",data)

def student_view_attendance_post(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_date_parse = datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date_parse = datetime.strptime(end_date,"%Y-%m-%d").date()

        subject_obj = Subject.objects.get(id = subject_id)
        user_obj = CustomUser.objects.get(id = request.user.id)
        student_obj = Student.objects.get(admin = user_obj)

        attendance = Attendance.objects.filter(attendance_date__range = (start_date_parse,end_date_parse),subject_id = subject_obj)
        attendance_report = AttendanceReport.objects.filter(attendance_id__in = attendance,student_id = student_obj)

        profile_pic = student_obj.profile_pic

        data = {
            'attendance_reports':attendance_report,
            'profile_pic':profile_pic

        }
    return render(request,"student_template/student_attendance_data.html",data)


def student_apply_leave(request):
    student_obj = Student.objects.get(admin = request.user.id)
    profile_pic = student_obj.profile_pic
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    data = {
        'leave_data':leave_data,
        'profile_pic':profile_pic
    }
    return render(request,"student_template/stud_apply_leave.html",data)

def student_apply_leave_save(request):
    if request.method != "POST":
        return redirect(reverse('student_apply_leave'))
    else:
        leave_date_start = request.POST.get('leave_date_start')
        leave_date_end = request.POST.get('leave_date_end')
        leave_dates = str(leave_date_start)+" TO "+str(leave_date_end)
        leave_reason = request.POST.get('leave_reason')
        
        str_d1 = str(leave_date_start)
        str_d2 = str(leave_date_end)

        # convert string to date object
        d1 = datetime.strptime(str_d1, "%Y-%m-%d")
        d2 = datetime.strptime(str_d2, "%Y-%m-%d")

        # difference between dates in timedelta
        days = d2 - d1

        student_obj = Student.objects.get(admin = request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id = student_obj,leave_date = leave_dates,leave_reason = leave_reason,leave_status = 0)
            leave_report.save()
            messages.success(request,f"Successfully Applied For {days.days} days Leave")
            return redirect(reverse('student_apply_leave'))

        except:
            messages.warning(request,"failed to apply for leave")
            return redirect(reverse('student_apply_leave'))
        
def student_feedback(request):
    student_obj = Student.objects.get(admin = request.user.id)
    profile_pic = student_obj.profile_pic
    feedbacks = FeedbackStudent.objects.filter(student_id = student_obj)
    data = {
        'feedback_message' : feedbacks,
        'profile_pic':profile_pic
    }
    return render(request,"student_template/feedback_student.html",data)

def student_feedback_save(request):
    if request.method != "POST":
        return redirect(reverse('student_feedback'))
    else:
        feedback_message = request.POST.get("feedback_message")
        student_obj = Student.objects.get(admin = request.user.id)

        try:
            studentfeedback = FeedbackStudent(student_id = student_obj,feedback = feedback_message,feedback_reply = "")
            studentfeedback.save()
            messages.success(request,f"Successfully Feedback Send")
            return redirect(reverse('student_feedback'))

        except:
            messages.warning(request,"failed to send feedback")
            return redirect(reverse('student_feedback'))
        

def profile_student(request):
    user = CustomUser.objects.get(id = request.user.id)
    student = Student.objects.get(admin = user.id)
    profile_pic = student.profile_pic
    data = {
        'user':user,
        'student':student,
        'profile_pic':profile_pic
    }
    return render(request,"student_template/student_profile.html",data)

def student_profile_edit(request):
    user = CustomUser.objects.get(id = request.user.id)
    student = Student.objects.get(admin = user.id)
    profile_pic = student.profile_pic
    courses = Course.objects.all()
    sessionyear = SessionYear.objects.all()
    data = {
        'user':user,
        'student':student,
        'courses':courses,
        'sessionyears':sessionyear,
        'profile_pic':profile_pic
    }
    return render(request,"student_template/student_profile_edit.html",data)

def student_profile_edit_save(request):
    if request.method != "POST":
        return redirect(reverse('student_profile_edit'))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        addresss = request.POST.get("addresss")
        password = request.POST.get("password")
        profile_image = request.POST.get("profile_image")
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            fs = FileSystemStorage()
            filename = fs.save(profile_image.name,profile_image)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id = request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            if password != None and password != "":
                user.set_password(password)
            user.save()
            student = Student.objects.get(admin = user.id)
            student.address = addresss    
            if profile_pic_url != None:
                student.profile_pic = profile_pic_url
            student.save()
            messages.success(request,"Successfully Edited Profile")
            return redirect('profile_student')
        except:
            messages.error(request,"Failed To Edit Profile")
            return redirect('profile_student')
        

@csrf_exempt
def student_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        student = Student.objects.get(admin = request.user.id)
        student.fcm_token = token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
    

def view_notification_student(request):
    student = Student.objects.filter(admin = request.user.id)
    student_id = Student.objects.get(admin = request.user.id)
    profile_pic = student_id.profile_pic
    student_id_n = 0
    for i in student:
        student_id_n = i.id
    student_notification = NotificationStudent.objects.filter(student_id = student_id_n)
    data = {
        'student_notification':student_notification,
        'profile_pic':profile_pic
    }
    return render(request,"student_template/student_notification.html",data)

def view_notification_seen_student(request,n_id):
    notification = NotificationStudent.objects.get(id = n_id)
    notification.notification_status = 1
    notification.save()
    return redirect(reverse('view_notification_s'))

def view_result(request):
    student_id = Student.objects.get(admin = request.user.id)
    profile_pic = student_id.profile_pic
    stud_id = Student.objects.get(admin = request.user.id)
    quaterly_exam_student_mark = QuaterlyExam.objects.filter(student_id = stud_id)
    halfyerly_exam_student_mark = HalfyearlyExam.objects.filter(student_id = stud_id)
    annual_exam_student_mark = AnnualExam.objects.filter(student_id = stud_id)

    results = False
    if not bool(quaterly_exam_student_mark) and not bool(halfyerly_exam_student_mark) and not bool(annual_exam_student_mark):
        results = True
    data = {
        'quaterly_exam_student_mark':quaterly_exam_student_mark,
        'halfyerly_exam_student_mark':halfyerly_exam_student_mark,
        'annual_exam_student_mark':annual_exam_student_mark,
        'profile_pic':profile_pic,
        'results':results
    }
    return render(request,"student_template/view_result.html",data)