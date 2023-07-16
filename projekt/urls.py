from django.contrib import admin
from django.urls import path
from app1.views import *

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('add_subject/', add_subject, name='add_subject'),
    path('list_subjects/', list_subjects, name='list_subjects'),
    path('edit_subject/<int:subject_id>/', edit_subject, name='edit_subject'),
    path('create_user/', create_user, name='create_user'),
    path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
    path('students/', list_students, name='list_students'),
    path('professors/', list_professors, name='list_professors'),
    path('class_attendance/<int:subject_id>/', class_attendance, name='class_attendance'),
    path('professor_dashboard/', professor_dashboard, name='professor_dashboard'),
    path('enrollment_list/', enrollment_list, name='enrollment_list'),
    path('create_enrollment/<int:student_id>/', create_enrollment, name='create_enrollment'),
    path('enrolled_subjects/<int:student_id>/', enrolled_subjects, name='enrolled_subjects'),
    path('enrolled_students/<int:subject_id>/', enrolled_students, name='enrolled_students'),
    path('enrolled_students_professor/<int:subject_id>/', enrolled_students_professor, name='enrolled_students_professor'),
    path('update_enrollment_status/<int:enrollment_id>/', update_enrollment_status, name='update_enrollment_status'),
    path('passed_students_professor/<int:subject_id>/', passed_students_professor, name='passed_students_professor'),
    path('failed_students_professor/<int:subject_id>/', failed_students_professor, name='failed_students_professor'),
    path('update_enrollment_status/', update_enrollment_status, name='update_enrollment_status'),
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('show_people/', show_people, name='show_people'),
    path('show_enrolled_students/<int:subject_id>/', show_enrolled_students, name='show_enrolled_students'),

]
