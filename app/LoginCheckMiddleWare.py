from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import render,redirect


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self,request,view_func,view_args,view_kwargs):
        module_name = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if module_name == "app.HOD_VIEWS":
                    pass
                elif module_name == "app.views" or module_name == "django.views.static":
                    pass
                else:
                    return redirect(reverse('admin_home'))
                
            elif user.user_type == "2":
                if module_name == "app.STAFF_VIEWS":
                    pass
                elif module_name == "app.views"  or module_name == "django.views.static":
                    pass
                else:
                    return redirect(reverse('staff_home'))
                
            elif user.user_type == "3":
                if module_name == "app.STUDENT_VIEWS":
                    pass
                elif module_name == "app.views"  or module_name == "django.views.static":
                    pass
                else:
                    return redirect(reverse('student_home'))
                
            else:
                return redirect('login_page')
        else:
            if request.path == reverse("login_page") or request.path == reverse("do_login") or module_name == "django.contrib.auth.views" or module_name == "app.views":
                pass
            else:
                return redirect(reverse('login_page'))