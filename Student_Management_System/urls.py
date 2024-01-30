"""
URL configuration for Student_Management_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from app import views,HOD_VIEWS,STAFF_VIEWS,STUDENT_VIEWS

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include('django.contrib.auth.urls')),
    path('',views.ShowLoginPage,name='login_page'),
    path('signup_admin/',views.signup_admin,name='signup_admin'),
    path('signup_staff/',views.signup_staff,name='signup_staff'),
    path('signup_student',views.signup_student,name='signup_student'),
    path('do_admin_signup',views.do_admin_signup,name='do_admin_signup'),
    path('do_staff_signup',views.do_staff_signup,name='do_staff_signup'),
    path('do_student_signup',views.do_student_signup,name='do_student_signup'),
    path('get_user_details/',views.GetUserDetails,name='get_user_details'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('dologin/',views.DOLOGIN,name='do_login'),
    path('check_email_exist/',HOD_VIEWS.check_email_exist,name='check_email_exist'),
    path('check_username_exist/',HOD_VIEWS.check_username_exist,name='check_username_exist'),


    # HOD VIEW ROUTES
    path('admin_home/',HOD_VIEWS.admin_home,name='admin_home'),
    path('profile_hod/',HOD_VIEWS.profile_hod,name='profile_hod'),
    path('hod_profile_edit/',HOD_VIEWS.hod_profile_edit,name='hod_profile_edit'),
    path('hod_profile_edit_save/',HOD_VIEWS.hod_profile_edit_save,name='hod_profile_edit_save'),
    path('add_staff/',HOD_VIEWS.ADD_STAFF,name="add_staff"),
    path('add_staff_save/',HOD_VIEWS.ADD_STAFF_SAVE,name="add_staff_save"),
    path('add_course/',HOD_VIEWS.ADD_COURSE,name="add_course"),
    path('add_course_save/',HOD_VIEWS.ADD_COURSE_SAVE,name="add_course_save"),
    path('add_student/',HOD_VIEWS.ADD_STUDENT,name="add_student"),
    path('add_student_save/',HOD_VIEWS.ADD_STUDENT_SAVE,name="add_student_save"),
    path('add_subject/',HOD_VIEWS.ADD_SUBJECT,name="add_subject"),
    path('add_subject_save/',HOD_VIEWS.ADD_SUBJECT_SAVE,name="add_subject_save"),
    path('manage_staff/',HOD_VIEWS.MANAGE_STAFF,name="manage_staff"),
    path('manage_student/',HOD_VIEWS.MANAGE_STUDENT,name="manage_student"),
    path('manage_course/',HOD_VIEWS.MANAGE_COURSE,name="manage_course"),
    path('manage_subject/',HOD_VIEWS.MANAGE_SUBJECT,name="manage_subject"),
    path('manage_session/',HOD_VIEWS.manage_session,name="manage_session"),
    path('add_session_save/',HOD_VIEWS.add_session_save,name="add_session_save"),
    path('edit_student/<str:student_id>',HOD_VIEWS.EDIT_STUDENT,name="edit_student"),
    path('edit_student_save/',HOD_VIEWS.EDIT_STUDENT_SAVE,name="edit_student_save"),
    path('delete_student/<str:student_id>',HOD_VIEWS.DELETE_STUDENT,name='delete_student'),
    path('edit_staff/<str:staff_id>',HOD_VIEWS.EDIT_STAFF,name="edit_staff"),
    path('edit_staff_save/',HOD_VIEWS.EDIT_STAFF_SAVE,name="edit_staff_save"),
    path('delete_staff/<str:staff_id>',HOD_VIEWS.DELETE_STAFF,name='delete_staff'),
    path('edit_subject/<str:subject_id>',HOD_VIEWS.EDIT_SUBJECT,name="edit_subject"),
    path('edit_subject_save/',HOD_VIEWS.EDIT_SUBJECT_SAVE,name="edit_subject_save"),
    path('delete_subject/<str:subject_id>',HOD_VIEWS.DELETE_SUBJECT,name='delete_subject'),
    path('edit_course/<str:course_id>',HOD_VIEWS.EDIT_COURSE,name="edit_course"),
    path('edit_course_save/',HOD_VIEWS.EDIT_COURSE_SAVE,name="edit_course_save"),
    path('delete_course/<str:course_id>',HOD_VIEWS.DELETE_COURSE,name='delete_course'),
    path('staff_feedback/',HOD_VIEWS.staff_feedback,name='staff_feedback'),
    path('staff_feedback_replied/',HOD_VIEWS.staff_feedback_replied,name='staff_feedback_replied'),
    path('student_feedback/',HOD_VIEWS.student_feedback,name='student_feedback'),
    path('student_feedback_replied/',HOD_VIEWS.student_feedback_replied,name='student_feedback_replied'),
    path('student_leave_view/',HOD_VIEWS.student_leave_view,name='student_leave_view'),
    path('student_leave_approve/<str:leave_id>',HOD_VIEWS.student_leave_approve,name='student_leave_approve'),
    path('student_leave_reject/<str:leave_id>',HOD_VIEWS.student_leave_reject,name='student_leave_reject'),
    path('staff_leave_view/',HOD_VIEWS.staff_leave_view,name='staff_leave_view'),
    path('staff_leave_approve/<str:leave_id>',HOD_VIEWS.staff_leave_approve,name='staff_leave_approve'),
    path('staff_leave_reject/<str:leave_id>',HOD_VIEWS.staff_leave_reject,name='staff_leave_reject'),
    path('hod_view_attendance/',HOD_VIEWS.hod_view_attendance,name='hod_view_attendance'),
    path('hod_get_attendance_dates/',HOD_VIEWS.hod_get_attendance_dates,name='hod_get_attendance_dates'),
    path('hod_get_attendance_student/',HOD_VIEWS.hod_get_attendance_student,name='hod_get_attendance_student'),
    path('send_notification_staff/',HOD_VIEWS.send_notification_staff,name='send_notification_staff'),
    path('send_notification_staff_save/',HOD_VIEWS.send_notification_staff_save,name='send_notification_staff_save'),
    path('send_notification_student/',HOD_VIEWS.send_notification_student,name='send_notification_student'),
    path('send_notification_student_save/',HOD_VIEWS.send_notification_student_save,name='send_notification_student_save'),


    # STAFF VIEW ROUTES
    path('staff_home',STAFF_VIEWS.STAFF_HOME,name='staff_home'),
    path('profile_staff/',STAFF_VIEWS.profile_staff,name='profile_staff'),
    path('staff_profile_edit/',STAFF_VIEWS.staff_profile_edit,name='staff_profile_edit'),
    path('staff_profile_edit_save/',STAFF_VIEWS.staff_profile_edit_save,name='staff_profile_edit_save'),
    path('staff_take_attendance/',STAFF_VIEWS.staff_take_attendance,name='staff_take_attendance'),
    path('get_students/',STAFF_VIEWS.get_students,name='get_students'),
    path('save_attendance_data/',STAFF_VIEWS.save_attendance_data,name='save_attendance_data'),
    path('staff_update_attendance/',STAFF_VIEWS.staff_update_attendance,name='staff_update_attendance'),
    path('get_attendance_dates/',STAFF_VIEWS.get_attendance_dates,name='get_attendance_dates'),
    path('get_attendance_student/',STAFF_VIEWS.get_attendance_student,name='get_attendance_student'),
    path('save_update_attendace_date/',STAFF_VIEWS.save_update_attendace_date,name='save_update_attendace_date'),
    path('apply_leave/',STAFF_VIEWS.apply_leave,name='apply_leave'),
    path('apply_leave_save/',STAFF_VIEWS.apply_leave_save,name='apply_leave_save'),
    path('staff_feedback/',STAFF_VIEWS.staff_feedback,name='staff_feedback'),
    path('staff_feedback_save/',STAFF_VIEWS.staff_feedback_save,name='staff_feedback_save'),
    path('staff_fcmtoken_save/',STAFF_VIEWS.staff_fcmtoken_save,name='staff_fcmtoken_save'),
    path('add_result/',STAFF_VIEWS.add_result,name='add_result'),
    path('result_save/',STAFF_VIEWS.result_save,name='result_save'),
    path('view_notification/',STAFF_VIEWS.view_notification,name='view_notification'),
    path('view_notification_seen/<str:n_id>',STAFF_VIEWS.view_notification_seen,name='view_notification_seen'),

    # STUDENT VIEW ROUTES
    path('student_home',STUDENT_VIEWS.STUDENT_HOME,name='student_home'),
    path('profile_student/',STUDENT_VIEWS.profile_student,name='profile_student'),
    path('student_profile_edit/',STUDENT_VIEWS.student_profile_edit,name='student_profile_edit'),
    path('student_profile_edit_save/',STUDENT_VIEWS.student_profile_edit_save,name='student_profile_edit_save'),
    path('student_view_attendance/',STUDENT_VIEWS.student_view_attendance,name='student_view_attendance'),
    path('student_view_attendance_post/',STUDENT_VIEWS.student_view_attendance_post,name='student_view_attendance_post'),
    path('student_apply_leave/',STUDENT_VIEWS.student_apply_leave,name='student_apply_leave'),
    path('student_apply_leave_save/',STUDENT_VIEWS.student_apply_leave_save,name='student_apply_leave_save'),
    path('student_feedback/',STUDENT_VIEWS.student_feedback,name='student_feedback'),
    path('view_result/',STUDENT_VIEWS.view_result,name='view_result'),
    path('student_feedback_save/',STUDENT_VIEWS.student_feedback_save,name='student_feedback_save'),
    path('student_fcmtoken_save/',STUDENT_VIEWS.student_fcmtoken_save,name='student_fcmtoken_save'),
    path('view_notification_student/',STUDENT_VIEWS.view_notification_student,name='view_notification_s'),
    path('view_notification_seen_student/<str:n_id>',STUDENT_VIEWS.view_notification_seen_student,name='view_notification_seen_s'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
