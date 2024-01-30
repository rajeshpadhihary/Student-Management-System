from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import CustomUser, Course, SessionYear
from .forms import AddStudentForm
from django.core.files.storage import FileSystemStorage


# Create your views here.
# def login(request):
#     return render(request,"index.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def DOLOGIN(request):
    if request.method != "POST":
        return redirect("login_page")
    else:
        user = EmailBackEnd.authenticate(
            request,
            username=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return redirect("admin_home")
            elif user.user_type == "2":
                return redirect("staff_home")
            elif user.user_type == "3":
                return redirect("student_home")
        else:
            messages.error(request, "Invalid Data For Login")
            return redirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse(
            "User : " + request.user.email + "usertype : " + request.user.user_type
        )
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return redirect("login_page")


def signup_admin(request):
    return render(request, "signup_admin.html")


def signup_staff(request):
    return render(request, "signup_staff.html")


def signup_student(request):
    courses = Course.objects.all()
    session_year_id = SessionYear.objects.all()
    data = {"courses": courses, "session_year_id": session_year_id}
    return render(request, "signup_student.html", data)


def do_admin_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email, user_type=1
        )
        user.save()
        messages.success(request, "Successfully Created Admin")
        return redirect("login_page")
    except:
        messages.error(request, "Failed to Create Admin")
        return redirect("login_page")


def do_staff_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")

    try:
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=2,
        )
        user.staff.address = address
        user.save()
        messages.success(request, "Successfully Created Staff")
        return redirect("login_page")
    except:
        messages.error(request, "Failed to Create Staff")
        return redirect("login_page")


def do_student_signup(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year_id")
    course_id = request.POST.get("course_id")
    gender = request.POST.get("gender")

    profile_pic = request.FILES.get("profile_pic")
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)

    try:
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=3,
        )
        user.student.address = address
        course_obj = Course.objects.get(id=course_id)
        user.student.course_id = course_obj
        session_year = SessionYear.objects.get(id=session_year_id)
        user.student.session_year_id = session_year
        user.student.gender = gender
        user.student.profile_pic = profile_pic_url
        user.save()
        messages.success(request, "Successfully Created Student")
        return redirect("login_page")
    except:
        messages.error(request, "Failed to create Student")
        return redirect("login_page")
