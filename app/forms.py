from django import forms
from . models import Course,Subject,SessionYear

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off",'placeholder': 'Enter Email'}))
    password = forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control",'placeholder': 'Enter password'}))
    first_name = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter Last Name'}))
    username = forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off",'placeholder': 'Enter Username'}))
    address = forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Enter Address'}))
    course_list = []
    try:
        courses = Course.objects.all()
        for i in courses:
            small_c = (i.id,i.course_name)
            course_list.append(small_c)
    except:
        course_list = []


    session_list = []
    try:
        sessions = SessionYear.objects.all()
        for j in sessions:
            small_s = (j.id,str(j.session_start_year)+" TO "+str(j.session_end_year))
            session_list.append(small_s)
    except:
        session_list = []

    gender_choice = (
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    course = forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    # session_start = forms.DateField(label="Session Start",widget=DateInput(attrs={"class":"form-control"}))
    # session_end = forms.DateField(label="Session End",widget=DateInput(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    course_list = []
    try:
        courses = Course.objects.all()
        for i in courses:
            small_c = (i.id,i.course_name)
            course_list.append(small_c)
    except:
        course_list = []


    session_list = []
    try:
        sessions = SessionYear.objects.all()
        for j in sessions:
            small_s = (j.id,str(j.session_start_year)+" to "+str(j.session_end_year))
            session_list.append(small_s)
    except:
        session_list = []

    gender_choice = (
        ("Male","Male"),
        ("Female","Female"),
        ("Others","Others")
    )
    course = forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    gender = forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
