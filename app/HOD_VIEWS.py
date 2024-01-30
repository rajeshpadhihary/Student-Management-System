from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import json
from django.urls import reverse
from django.contrib import messages
from . forms import AddStudentForm,EditStudentForm
from app.models import CustomUser,Staff,Course,Subject,Student,SessionYear,FeedbackStudent,FeedbackStaff,LeaveReportStaff,LeaveReportStudent,Attendance,AttendanceReport,QuaterlyExam,HalfyearlyExam,AnnualExam,StudentResult,NotificationStaff,NotificationStudent
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt


def admin_home(request):
    staffs_count = Staff.objects.count()
    students_count = Student.objects.count()
    total_members = staffs_count+students_count
    courses_count = Course.objects.count()
    subjects_count = Subject.objects.count()
    sessionyears = SessionYear.objects.count()

    course_all = Course.objects.all()
    course_name_list = []
    subjects_count_list = []
    students_count_in_course = []
    for course in course_all:
        subjects = Subject.objects.filter(course_id = course.id).count()
        student_in_course = Student.objects.filter(course_id = course.id).count()
        students_count_in_course.append(student_in_course)
        course_name_list.append(course.course_name)
        subjects_count_list.append(subjects)

    subject_all = Subject.objects.all()
    subject_name_list = []
    students_count_in_subjct = []
    for subject in subject_all:
        course = Course.objects.get(id = subject.course_id.id)
        student_count = Student.objects.filter(course_id = course.id).count()
        subject_name_list.append(subject.subject_name)
        students_count_in_subjct.append(student_count)

    staffs = Staff.objects.all()
    staff_name_list = []
    staff_attendance_present = []
    staff_attendance_absent = []
    for staff in staffs:
        subject_ids = Subject.objects.filter(staff_id = staff.admin.id)
        attendance = Attendance.objects.filter(subject_id__in = subject_ids).count()
        leaves = LeaveReportStaff.objects.filter(staff_id = staff.id,leave_status = 1).count()
        staff_name_list.append(staff.admin.username)
        staff_attendance_present.append(attendance)
        staff_attendance_absent.append(leaves)

    students_all = Student.objects.all()
    student_list = []
    student_present_list = []
    student_absent_list = []
    for student in students_all:
        attendance_s = AttendanceReport.objects.filter(student_id = student.id,status = True).count()
        absent_s = AttendanceReport.objects.filter(student_id = student.id,status = False).count()
        student_list.append(student.admin.username)
        student_absent_list.append(absent_s)
        student_present_list.append(attendance_s)

    #Quaterly

    Quater = QuaterlyExam.objects.all()
    quater_total_indivisual_results = []
    quater_total_mark = []
    quaterly_student_names = []
    quaterly_indivisual_ids = []
    for s_id in Quater:
        student_indivisual_id = s_id.student_id.id
        if  student_indivisual_id not in quaterly_indivisual_ids:
            quaterly_indivisual_ids.append(student_indivisual_id)

    for i in range(len(quaterly_indivisual_ids)):
        mark_obj = QuaterlyExam.objects.filter(student_id = quaterly_indivisual_ids[i])

        for i in mark_obj:
            if i.student_id.admin.username not in quaterly_student_names:
                quaterly_student_names.append(i.student_id.admin.username)

        sub_mark = [i.obtained_marks for i in mark_obj]
        total_mark = [i.total_marks for i in mark_obj]
        quater_total_indivisual_results.append(sum(sub_mark))
        quater_total_mark.append(sum(total_mark))


    #Half Yearly
    HalfYearly = HalfyearlyExam.objects.all()
    halfyearly_total_indivisual_results = []
    halfyearly_total_mark = []
    halfyearly_student_names = []
    halfyearly_indivisual_ids = []
    for s_id in HalfYearly:
        student_indivisual_id = s_id.student_id.id
        if  student_indivisual_id not in halfyearly_indivisual_ids:
            halfyearly_indivisual_ids.append(student_indivisual_id)

    for i in range(len(halfyearly_indivisual_ids)):
        mark_obj = HalfyearlyExam.objects.filter(student_id = halfyearly_indivisual_ids[i])

        for i in mark_obj:
            if i.student_id.admin.username not in halfyearly_student_names:
                halfyearly_student_names.append(i.student_id.admin.username)

        sub_mark = [i.obtained_marks for i in mark_obj]
        total_mark = [i.total_marks for i in mark_obj]
        halfyearly_total_indivisual_results.append(sum(sub_mark))
        halfyearly_total_mark.append(sum(total_mark))

    #Annual
    Annual = AnnualExam.objects.all()
    annual_total_indivisual_results = []
    annual_total_mark = []
    annually_student_names = []
    annually_indivisual_ids = []
    for s_id in Annual:
        student_indivisual_id = s_id.student_id.id
        if  student_indivisual_id not in annually_indivisual_ids:
            annually_indivisual_ids.append(student_indivisual_id)

    for i in range(len(annually_indivisual_ids)):
        mark_obj = AnnualExam.objects.filter(student_id = annually_indivisual_ids[i])

        for i in mark_obj:
            if i.student_id.admin.username not in annually_student_names:
                annually_student_names.append(i.student_id.admin.username)

        sub_mark = [i.obtained_marks for i in mark_obj]
        total_mark = [i.total_marks for i in mark_obj]
        annual_total_indivisual_results.append(sum(sub_mark))
        annual_total_mark.append(sum(total_mark))
    
    # print(quter_total_indivisual_results)
    # print(quater_total_mark)
    
    data = {
        'staff':staffs_count,
        'student':students_count,
        'course':courses_count,
        "subject":subjects_count,
        'sessionyear':sessionyears,
        'total_member':total_members,
        'course_name_list':course_name_list,
        'subjects_count_list':subjects_count_list,
        'students_count_in_course':students_count_in_course,
        'subject_name_list':subject_name_list,
        'students_count_in_subjct':students_count_in_subjct,
        'staff_name_list':staff_name_list,
        'staff_attendance_present':staff_attendance_present,
        'staff_attendance_absent':staff_attendance_absent,
        'student_list':student_list,
        'student_present_list':student_present_list,
        'student_absent_list':student_absent_list,
        'quater_total_indivisual_results':quater_total_indivisual_results,
        'quater_total_mark':quater_total_mark,
        'quaterly_student_names':quaterly_student_names,
        'annual_total_indivisual_results':annual_total_indivisual_results,
        'annual_total_mark':annual_total_mark,
        'annually_student_names':annually_student_names,
        'halfyearly_total_indivisual_results':halfyearly_total_indivisual_results,
        'halfyearly_total_mark':halfyearly_total_mark,
        'halfyearly_student_names':halfyearly_student_names
    }

    return render(request,'hod_template/home_content.html',data)

def ADD_STAFF(request):
    return render(request,'hod_template/add_staff.html')

def ADD_STAFF_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.create_user(username = username,email = email, password = password,first_name = first_name, last_name = last_name, user_type = 2)
            user.staff.address = address
            user.save() 
            messages.success(request,"Successfully Added Staff")
            return redirect('add_staff')
        except:
            messages.error(request,"Failed to Add Staff")
            return redirect('add_staff')
        
def ADD_COURSE(request):
    return render(request,'hod_template/add_course.html')

def ADD_COURSE_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        try:
            course = request.POST.get('course_name')
            course_model = Course(course_name = course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return redirect('add_course')
        except:
            messages.warning(request,"Please fill all fields.")
            return redirect('add_course')
        
def ADD_STUDENT(request):
    form = AddStudentForm()
    context={
        'form':form,
        }
    return render(request,'hod_template/add_student.html',context)

def ADD_STUDENT_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course']
            gender = form.cleaned_data['gender']

            profile_pic = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name,profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username = username,email = email, password = password,first_name = first_name, last_name = last_name, user_type = 3)
                user.student.address = address
                course_obj = Course.objects.get(id = course_id)
                user.student.course_id = course_obj
                session_year = SessionYear.objects.get(id=session_year_id)
                user.student.session_year_id = session_year
                user.student.gender = gender
                user.student.profile_pic = profile_pic_url
                user.save() 
                messages.success(request,"Successfully Added Student")
                return redirect('add_student')
            except:
                messages.error(request,"Failed to Add Student")
                return redirect('add_student')
        else:
            form = AddStudentForm(request.POST)
            return render(request,'hod_template/add_student.html',{'form':form})

        
def ADD_SUBJECT(request):
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type = 2)
    data = {
        "courses" : courses,
        "staffs" : staffs
    }
    return render(request,'hod_template/add_subject.html',data)

def ADD_SUBJECT_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')
        course = Course.objects.get(id = course_id)
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subject(subject_name = subject_name,course_id = course,staff_id = staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return redirect('add_subject')
        except:
            messages.error(request,"Failed To Add Subject")
            return redirect('add_subject')
        
def MANAGE_STAFF(request):
    staffs = Staff.objects.all()
    data={'staffs':staffs}
    return render(request,'hod_template/manage_staff.html',data)

def MANAGE_STUDENT(request):
    students = Student.objects.all()
    data={'students':students}
    return render(request,'hod_template/manage_student.html',data)

def MANAGE_COURSE(request):
    courses = Course.objects.all()
    data={'courses':courses}
    return render(request,'hod_template/manage_course.html',data)

def MANAGE_SUBJECT(request):
    subjects = Subject.objects.all()
    data={'subjects':subjects}
    return render(request,'hod_template/manage_subject.html',data)

def EDIT_STUDENT(request,student_id):
    request.session['student_id'] = student_id
    student = Student.objects.get(admin = student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['gender'].initial = student.gender
    form.fields['session_year_id'].initial = student.session_year_id.id


    data = {
        'form':form,
        'id':student_id,
        'username':student.admin.username,

    }
    return render(request,'hod_template/edit_student.html',data)

def EDIT_STUDENT_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return redirect('manage_student')
        
        form = EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
        # profile_pic = request.FILES.get("profile_pic")
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course']
            gender = form.cleaned_data['gender']

            profile_pic = request.FILES.get('profile_pic')
            if profile_pic:
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name,profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id = student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                student_model = Student.objects.get(admin = student_id)
                course_obj = Course.objects.get(id = course_id)
                student_model.address = address
                student_model.course_id = course_obj
                session_year = SessionYear.objects.get(id=session_year_id)
                student_model.session_year_id = session_year
                student_model.gender = gender
                if profile_pic_url != None:
                    student_model.profile_pic = profile_pic_url
                student_model.save()
                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return redirect('manage_student')
            except:
                messages.error(request,"Failed to Edit Student")
                return redirect('manage_student')
        else:
            form = EditStudentForm(request.POST)
            student = Student.objects.get(admin = student_id)
            return render(request,"hod_template/edit_student.html",{'form':form,'id':student_id,'username':student.admin.username})
        
def DELETE_STUDENT(request,student_id):
    student = Student.objects.get(admin=student_id)
    student.delete()
    user = CustomUser.objects.get(id = student_id)
    user.delete()
    messages.success(request,f"Records Is Successfully Deleted")
    return redirect('manage_student')


def EDIT_STAFF(request,staff_id):
    staff = Staff.objects.get(admin=staff_id)
    data = {
        'staff':staff,
        'id':staff_id
    }
    return render(request,'hod_template/edit_staff.html',data)


def EDIT_STAFF_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get('staff_id')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.get(id = staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            staff_model = Staff.objects.get(admin = staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request,f"Successfully Edited Staff {user.username}")
            return redirect('manage_staff')
        except:
            messages.error(request,"Failed To Edit Staff")
            return redirect('manage_staff')
        
def DELETE_STAFF(request,staff_id):
    staff = Staff.objects.get(admin=staff_id)
    staff.delete()
    user = CustomUser.objects.get(id = staff_id)
    user.delete()
    messages.success(request,f"Records Is Successfully Deleted")
    return redirect('manage_staff')
        
def EDIT_SUBJECT(request,subject_id):
        subject = Subject.objects.get(id=subject_id)
        courses = Course.objects.all()
        staffs = CustomUser.objects.filter(user_type = 2)
        data = {
            "courses" : courses,
            "staffs" : staffs,
            "subject":subject,
            'id':subject_id
        }
        return render(request,'hod_template/edit_subject.html',data)
def EDIT_SUBJECT_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course')
        staff_id = request.POST.get('staff')
        course = Course.objects.get(id = course_id)
        staff = CustomUser.objects.get(id=staff_id)

        try:
            subject = Subject.objects.get(id=subject_id)
            subject.subject_name = subject_name
            subject.course_id = course
            subject.staff_id = staff
            subject.save()
            messages.success(request,"Successfully Edited Subject")
            return redirect('manage_subject')
        except:
            messages.error(request,"Failed To Edit Subject")
            return redirect('manage_subject')

def DELETE_SUBJECT(request,subject_id):
    student = Subject.objects.get(id=subject_id)
    student.delete()
    messages.success(request,f"Records Is Successfully Deleted")
    return redirect('manage_subject')

def EDIT_COURSE(request,course_id):
    course = Course.objects.get(id=course_id)
    data = {
        "course":course,
        'id':course_id
    }
    return render(request,'hod_template/edit_course.html',data)

def EDIT_COURSE_SAVE(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course_name')
        try:
            course_model = Course.objects.get(id = course_id)
            course_model.course_name = course_name
            course_model.save()
            messages.success(request,"Successfully Edited Course")
            return redirect('manage_course')
        except:
            messages.warning(request,"Failed To Edit Course")
            return redirect('manage_course')
        
def DELETE_COURSE(request,course_id):
    course = Course.objects.get(id = course_id)
    course.delete()
    messages.success(request,f"Records Is Successfully Deleted")
    return redirect('manage_course')


def manage_session(request):
    return render(request,'hod_template/manage_session.html')


def add_session_save(request):
    if request.method != 'POST':
        return redirect(reverse('manage_session'))
    else:
        session_start_year = request.POST.get('session_start')
        session_end_year = request.POST.get('session_end')

        try:
            sessionyear = SessionYear(session_start_year = session_start_year,session_end_year = session_end_year)
            sessionyear.save()
            messages.success(request,"Successfully Added Session Year")
            return redirect('manage_session')
        except:
            messages.warning(request,"Failed To Add Session Year")
            return redirect('manage_session')

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email = email).exists()

    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username = username).exists()

    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def staff_feedback(request):
    feedback_messages = FeedbackStaff.objects.all()
    data = {
        'feedback_messagess':feedback_messages
    }
    return render(request,"hod_template/staff_feedback.html",data)

@csrf_exempt
def staff_feedback_replied(request):
    feedback_id = request.POST.get("id")
    feedback_msg = request.POST.get("message")

    try:
        feedback = FeedbackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_msg
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def student_feedback(request):
    feedback_messages = FeedbackStudent.objects.all()
    data = {
        'feedback_messages':feedback_messages
    }
    return render(request,"hod_template/student_feedback.html",data)

@csrf_exempt
def student_feedback_replied(request):
    feedback_id = request.POST.get("id")
    feedback_msg = request.POST.get("message")

    try:
        feedback = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_msg
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
    

def student_leave_view(request):
    leave_obj = LeaveReportStudent.objects.all()
    data = {
        "leave_objs":leave_obj,
    }
    return render(request,"hod_template/student_leave_view.html",data)

def student_leave_approve(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect(reverse('student_leave_view'))

def student_leave_reject(request,leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect(reverse('student_leave_view'))


def staff_leave_view(request):
    leave_obj = LeaveReportStaff.objects.all()
    data = {
        "leave_objs":leave_obj,
    }
    return render(request,"hod_template/staff_leave_view.html",data)

def staff_leave_approve(request,leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect(reverse('staff_leave_view'))

def staff_leave_reject(request,leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect(reverse('staff_leave_view'))


def hod_view_attendance(request):
    subjects = Subject.objects.all()
    session_year_id = SessionYear.objects.all()
    data = {
        'subjects':subjects,
        'session_year_id' : session_year_id
    }
    return render(request,"hod_template/hod_view_attendance.html",data)

@csrf_exempt
def hod_get_attendance_dates(request):
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
def hod_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")

    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)

    list_data = []
    for student in attendance_data:
        small_data = {"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(small_data)
    return JsonResponse(json.dumps(list_data),content_type = "application/json",safe=False)


def profile_hod(request):
    user = CustomUser.objects.get(id = request.user.id)
    data = {
        'user':user
    }
    return render(request,"hod_template/profile_hod.html",data)

def hod_profile_edit(request):
    user = CustomUser.objects.get(id = request.user.id)
    data = {
        'user':user
    }
    return render(request,"hod_template/profile_hod_edit.html",data)

def hod_profile_edit_save(request):
    if request.method != "POST":
        return redirect(reverse('hod_profile_edit'))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(id = request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            if password != None and password != "":
                user.set_password(password)
            user.save()
            messages.success(request,"Successfully Edited Profile")
            return redirect('profile_hod')
        except:
            messages.error(request,"Failed To Edit Profile")
            return redirect('profile_hod')
        
def send_notification_staff(request):
    staff = Staff.objects.all()
    notifications_staff = NotificationStaff.objects.all().order_by('-id')[0:5]
    data = {
        'staffs':staff,
        'notifications_staff':notifications_staff
    }
    return render(request,"hod_template/send_notification_staff.html",data)

def send_notification_staff_save(request):
    if request.method == "POST":
        message = request.POST.get("message")
        staff_id = request.POST.get("staff_id")

        staff_obj = Staff.objects.get(admin = staff_id)

        notification_save = NotificationStaff(staff_id = staff_obj,message = message)
        notification_save.save()
        messages.success(request,"Notification Sent Successfully")
        return redirect(reverse('send_notification_staff'))
    else:
        messages.error(request,"Failed To Send Notification")
        return redirect(reverse('send_notification_staff'))
    

def send_notification_student(request):
    student = Student.objects.all()
    notifications_student = NotificationStudent.objects.all().order_by('-id')[0:5]
    data = {
        'students':student,
        'notifications_student':notifications_student
    }
    return render(request,"hod_template/send_notification_student.html",data)

def send_notification_student_save(request):
    if request.method == "POST":
        message = request.POST.get("message")
        student_id = request.POST.get("student_id")

        student_obj = Student.objects.get(admin = student_id)

        notification_save = NotificationStudent(student_id = student_obj,message = message)
        notification_save.save()
        messages.success(request,"Notification Sent Successfully")
        return redirect(reverse('send_notification_student'))
    else:
        messages.error(request,"Failed To Send Notification")
        return redirect(reverse('send_notification_student'))