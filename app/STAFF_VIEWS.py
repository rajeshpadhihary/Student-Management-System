from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.urls import reverse
from django.contrib import messages
from app.models import CustomUser,Staff,Course,Subject,SessionYear,Student,Attendance,AttendanceReport,LeaveReportStaff,FeedbackStaff,StudentResult,QuaterlyExam,HalfyearlyExam,AnnualExam,NotificationStaff
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from datetime import datetime
import json

def STAFF_HOME(request):
    subjects = Subject.objects.filter(staff_id = request.user.id)
    staff = Staff.objects.filter(admin = request.user.id)
    staff_id_n = 0
    for i in staff:
        staff_id_n = i.id
    staff_notification = NotificationStaff.objects.filter(staff_id = staff_id_n)
    
    course_id_list = []
    for subject in subjects:
        course = Course.objects.get(id = subject.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Student.objects.filter(course_id__in = final_course).count()


    attendance_count = Attendance.objects.filter(subject_id__in = subjects).count()
    
    staff = Staff.objects.get(admin = request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id = staff.id,leave_status = 1).count()
    subjects_count = Subject.objects.filter(staff_id = request.user.id).count()

    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance1 = Attendance.objects.filter(subject_id = subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance1)

    attendance_count_total = attendance_count + leave_count

    students_attendance = Student.objects.filter(course_id__in = final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []

    for i in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status = True,student_id = i.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status = False,student_id = i.id).count()
        student_list.append(i.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)


    staff = Staff.objects.filter(admin = request.user.id)
    staff_id_n = 0
    for i in staff:
        staff_id_n = i.id
    staff_notification = NotificationStaff.objects.filter(staff_id = staff_id_n,notification_status = 0).count()
    
    data = {
        'subjects_count' : subjects_count,
        'student_count':students_count,
        'attendance_count':attendance_count,
        'leave_count':leave_count,
        'subject_list':subject_list,
        'attendance_list':attendance_list,
        'attendance_count_total':attendance_count_total,
        'student_list':student_list,
        'student_list_attendance_present':student_list_attendance_present,
        'student_list_attendance_absent':student_list_attendance_absent,
        'staff_notification':staff_notification,
    }

    return render(request,'staff_template/staff_home.html',data)

def staff_take_attendance(request):
    subjects = Subject.objects.filter(staff_id = request.user.id)
    session_years = SessionYear.objects.all()
    
    data = {
        'subjects':subjects,
        'session_years':session_years
    }
    return render(request,"staff_template/staff_take_attendance.html",data)


@csrf_exempt
def get_students(request):
    subject_id=request.POST.get('subject')
    session_year=request.POST.get("session_year")

    subject = Subject.objects.get(id=subject_id)
    session_model = SessionYear.objects.get(id=session_year)
    students = Student.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data = []
    for student in students:
        small_data = {"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(small_data)
    return JsonResponse(json.dumps(list_data),content_type = "application/json",safe=False)


@csrf_exempt
def save_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get('attendance_date')
    session_year_id = request.POST.get('session_year_id')
    subject_id = request.POST.get('subject_id')

    # print(student_ids)
    subject_model = Subject.objects.get(id = subject_id)
    session_model = SessionYear.objects.get(id = session_year_id)

    data = json.loads(student_ids)   
    # print(data[0]["id"])

    try:
        attendance = Attendance(subject_id = subject_model,attendance_date = attendance_date,session_year_id = session_model)
        attendance.save()

        for stud in data:
            student = Student.objects.get(admin = stud["id"])
            attendance_report = AttendanceReport(student_id = student,attendance_id = attendance,status = stud["status"])
            attendance_report.save()
        return HttpResponse("okk")
    except:
        return HttpResponse("error")

def staff_update_attendance(request):
    subjects = Subject.objects.filter(staff_id = request.user.id)
    session_year_id = SessionYear.objects.all()
    data = {
        'subjects':subjects,
        'session_year_id' : session_year_id
    }
    return render(request,"staff_template/staff_update_attendance.html",data)

@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get('subject')
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subject.objects.get(id = subject)
    session_year_obj = SessionYear.objects.get(id = session_year_id)
    attendance = Attendance.objects.filter(subject_id = subject_obj,session_year_id = session_year_obj)
    attendance_id = []
    for i in attendance:
        data = {"id":i.id,"attendance_date":str(i.attendance_date),"session_year_id":i.session_year_id.id}
        attendance_id.append(data)
    
    return JsonResponse(json.dumps(attendance_id),safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")

    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)

    list_data = []
    for student in attendance_data:
        small_data = {"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(small_data)
    return JsonResponse(json.dumps(list_data),content_type = "application/json",safe=False)

@csrf_exempt
def save_update_attendace_date(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    data = json.loads(student_ids)   
    try:
        for stud in data:
            student = Student.objects.get(admin = stud["id"])
            attendance_report = AttendanceReport.objects.get(student_id = student,attendance_id = attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("okk")
    except:
        return HttpResponse("error")

def apply_leave(request):
    staff_obj = Staff.objects.get(admin = request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    data = {
        'leave_data':leave_data,
    }
    return render(request,"staff_template/apply_leave.html",data)

def apply_leave_save(request):
    if request.method != "POST":
        return redirect(reverse('apply_leave'))
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

        staff_obj = Staff.objects.get(admin = request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id = staff_obj,leave_date = leave_dates,leave_reason = leave_reason,leave_status = 0)
            leave_report.save()
            messages.success(request,f"Successfully Applied For {days.days} days Leave")
            return redirect(reverse('apply_leave'))

        except:
            messages.warning(request,"failed to apply for leave")
            return redirect(reverse('apply_leave'))


def staff_feedback(request):
    staff_obj = Staff.objects.get(admin = request.user.id)
    feedbacks = FeedbackStaff.objects.filter(staff_id = staff_obj)
    data = {
        'feedback_message' : feedbacks,
    }
    return render(request,"staff_template/staff_feedback.html",data)

def staff_feedback_save(request):
    if request.method != "POST":
        return redirect(reverse('staff_feedback'))
    else:
        feedback_message = request.POST.get("feedback_message")
        staff_obj = Staff.objects.get(admin = request.user.id)

        try:
            stafffeedback = FeedbackStaff(staff_id = staff_obj,feedback = feedback_message,feedback_reply = "")
            stafffeedback.save()
            messages.success(request,f"Successfully Feedback Send")
            return redirect(reverse('staff_feedback'))

        except:
            messages.warning(request,"failed to send feedback")
            return redirect(reverse('staff_feedback'))


def profile_staff(request):
    user = CustomUser.objects.get(id = request.user.id)
    staff = Staff.objects.get(admin = user.id)
    data = {
        'user':user,
        'staff':staff,
    }
    return render(request,"staff_template/staff_profile.html",data)

def staff_profile_edit(request):
    user = CustomUser.objects.get(id = request.user.id)
    staff = Staff.objects.get(admin = user.id)
    data = {
        'user':user,
        'staff':staff,
    }
    return render(request,"staff_template/staff_profile_edit.html",data)

def staff_profile_edit_save(request):
    if request.method != "POST":
        return redirect(reverse('hod_profile_edit'))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        addresss = request.POST.get("addresss")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(id = request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            if password != None and password != "":
                user.set_password(password)
            user.save()
            staff = Staff.objects.get(admin = user.id)
            staff.address = addresss    
            staff.save()
            messages.success(request,"Successfully Edited Profile")
            return redirect('profile_staff')
        except:
            messages.error(request,"Failed To Edit Profile")
            return redirect('profile_staff')
        
@csrf_exempt
def staff_fcmtoken_save(request):
    token = request.POST.get("token")
    try:
        staff = Staff.objects.get(admin = request.user.id)
        staff.fcm_token = token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
    

def add_result(request):
    subjects = Subject.objects.filter(staff_id = request.user.id)
    session_years = SessionYear.objects.all()
    data = {
        'subjects' : subjects,
        'session_years': session_years
    }
    return render(request,"staff_template/add_result.html",data)

def result_save(request):
    if request.method != "POST":
        return redirect(reverse('add_result'))
    else:
        subject_id = request.POST.get("subject")
        student_id = request.POST.get("student_list")
        subject_marks = request.POST.get("subject_marks")
        out_of = request.POST.get("out_of")
        exam_type = request.POST.get("exam_type")

        student_obj = Student.objects.get(admin = student_id)
        subject_obj = Subject.objects.get(id = subject_id)

        try:
            if exam_type == "quaterly_exam":
                student_in_Quater_result = QuaterlyExam.objects.filter(subject_id = subject_obj,student_id = student_obj).exists()
                if student_in_Quater_result:
                    check_exists = StudentResult.objects.filter(student_id = student_obj,subject_id = subject_obj,exam_type = 1).exists()
                    if check_exists:
                        result = StudentResult.objects.get(subject_id = subject_obj,student_id = student_obj,exam_type = 1)
                        result.subject_exam_marks = subject_marks
                        result.marks_out_of = out_of
                        result.save()
                        messages.success(request,f"Successfully Result Updated")
                    else:
                        result = StudentResult(student_id = student_obj,subject_id = subject_obj,subject_exam_marks = subject_marks,marks_out_of = out_of,exam_type = 1)
                        result.save()
                        messages.success(request,f"Successfully Result Added")
                    result_Add = QuaterlyExam.objects.get(subject_id = subject_obj,student_id = student_obj)
                    result_Add.total_marks = out_of
                    result_Add.obtained_marks = subject_marks
                    result_Add.save()
                else:
                    check_exists = StudentResult.objects.filter(student_id = student_obj,subject_id = subject_obj,exam_type = 1).exists()
                    if check_exists:
                        result = StudentResult.objects.get(subject_id = subject_obj,student_id = student_obj,exam_type = 1)
                        result.subject_exam_marks = subject_marks
                        result.marks_out_of = out_of
                        result.save()
                        messages.success(request,f"Successfully Result Updated")
                    else:
                        result = StudentResult(student_id = student_obj,subject_id = subject_obj,subject_exam_marks = subject_marks,marks_out_of = out_of,exam_type = 1)
                        result.save()
                        messages.success(request,f"Successfully Result Added")
                    
                    result_Add = QuaterlyExam(subject_id = subject_obj,student_id = student_obj,total_marks = out_of,obtained_marks = subject_marks)
                    result_Add.save()
                return redirect(reverse('add_result'))
            
            elif exam_type == "halfyearly_exam":
                student_in_Halfyearly_result = HalfyearlyExam.objects.filter(subject_id = subject_obj,student_id = student_obj).exists()
                if student_in_Halfyearly_result:
                    check_exists = StudentResult.objects.filter(student_id = student_obj,subject_id = subject_obj,exam_type = 2).exists()
                    if check_exists:
                        result = StudentResult.objects.get(subject_id = subject_obj,student_id = student_obj,exam_type = 2)
                        result.subject_exam_marks = subject_marks
                        result.marks_out_of = out_of
                        result.save()
                        messages.success(request,f"Successfully Result Updated")
                    else:
                        result = StudentResult(student_id = student_obj,subject_id = subject_obj,subject_exam_marks = subject_marks,marks_out_of = out_of,exam_type = 2)
                        result.save()
                        messages.success(request,f"Successfully Result Added")
                    result_Add = HalfyearlyExam.objects.get(subject_id = subject_obj,student_id = student_obj)
                    result_Add.total_marks = out_of
                    result_Add.obtained_marks = subject_marks
                    result_Add.save()
                else:
                    check_exists = StudentResult.objects.filter(student_id = student_obj,subject_id = subject_obj,exam_type = 2).exists()
                    if check_exists:
                        result = StudentResult.objects.get(subject_id = subject_obj,student_id = student_obj,exam_type = 2)
                        result.subject_exam_marks = subject_marks
                        result.marks_out_of = out_of
                        result.save()
                        messages.success(request,f"Successfully Result Updated")
                    else:
                        result = StudentResult(student_id = student_obj,subject_id = subject_obj,subject_exam_marks = subject_marks,marks_out_of = out_of,exam_type = 2)
                        result.save()
                        messages.success(request,f"Successfully Result Added")
            
                    result_Add = HalfyearlyExam(subject_id = subject_obj,student_id = student_obj,total_marks = out_of,obtained_marks = subject_marks)
                    result_Add.save()
                return redirect(reverse('add_result'))
            
            elif exam_type == "annual_exam":
                student_in_Annual_result = AnnualExam.objects.filter(subject_id = subject_obj,student_id = student_obj).exists()
                if student_in_Annual_result:
                    check_exists = StudentResult.objects.filter(student_id = student_obj,subject_id = subject_obj,exam_type = 3).exists()
                    if check_exists:
                        result = StudentResult.objects.get(subject_id = subject_obj,student_id = student_obj,exam_type = 3)
                        result.subject_exam_marks = subject_marks
                        result.marks_out_of = out_of
                        result.save()
                        messages.success(request,f"Successfully Result Updated")
                    else:
                        result = StudentResult(student_id = student_obj,subject_id = subject_obj,subject_exam_marks = subject_marks,marks_out_of = out_of,exam_type = 3)
                        result.save()
                        messages.success(request,f"Successfully Result Added")
                    result_Add = AnnualExam.objects.get(subject_id = subject_obj,student_id = student_obj)
                    result_Add.total_marks = out_of
                    result_Add.obtained_marks = subject_marks
                    result_Add.save()
                else:
                    check_exists = StudentResult.objects.filter(student_id = student_obj,subject_id = subject_obj,exam_type = 3).exists()
                    if check_exists:
                        result = StudentResult.objects.get(subject_id = subject_obj,student_id = student_obj,exam_type = 3)
                        result.subject_exam_marks = subject_marks
                        result.marks_out_of = out_of
                        result.save()
                        messages.success(request,f"Successfully Result Updated")
                    else:
                        result = StudentResult(student_id = student_obj,subject_id = subject_obj,subject_exam_marks = subject_marks,marks_out_of = out_of,exam_type = 3)
                        result.save()
                        messages.success(request,f"Successfully Result Added")
                    
                    result_Add = AnnualExam(subject_id = subject_obj,student_id = student_obj,total_marks = out_of,obtained_marks = subject_marks)
                    result_Add.save()
                return redirect(reverse('add_result'))
            else:
                return render(reverse('add_result'))
        except:
            messages.warning(request,"failed to add Result")
            return redirect(reverse('add_result'))

def view_notification(request):
    staff = Staff.objects.filter(admin = request.user.id)
    staff_id_n = 0
    for i in staff:
        staff_id_n = i.id
    staff_notification = NotificationStaff.objects.filter(staff_id = staff_id_n)
    data = {
        'staff_notification':staff_notification
    }
    return render(request,"staff_template/staff_notification.html",data)

def view_notification_seen(request,n_id):
    notification = NotificationStaff.objects.get(id = n_id)
    notification.notification_status = 1
    notification.save()
    return redirect(reverse('view_notification'))