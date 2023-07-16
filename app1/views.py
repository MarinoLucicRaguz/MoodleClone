from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import user_passes_test

from .models import User, Predmeti, Enrollment
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                role_id = user.role_id if hasattr(user, 'role_id') else None
                if role_id == 1: 
                    return redirect('admin_dashboard')
                elif role_id == 2:
                    return redirect('student_dashboard')
                elif role_id == 3:
                    return redirect('professor_dashboard')
        else:
            invalid_login = True
            return render(request, 'login.html', {'form': form, 'invalid_login': invalid_login})
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})

def admin_required(function):
    decorator = user_passes_test(lambda u: u.is_active and u.is_superuser, login_url='login')
    return decorator(function)


@admin_required
def admin_dashboard(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = LoginForm()

    subjects = Predmeti.objects.all()
    

    context = {
        'form': form,
        'subjects': subjects,
    }

    return render(request, 'admin_dashboard.html', context)

def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = SubjectForm()

    context = {
        'form': form,
    }

    return render(request, 'add_subject.html', context)

def list_subjects(request):
    subjects = Predmeti.objects.all()
    context = {
        'subjects': subjects,
    }
    return render(request, 'list_subjects.html', context)

@staff_member_required
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.save()
            return redirect('admin_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})

@admin_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            subject.delete()
            return redirect('list_subjects')
        else:
            form = SubjectForm(request.POST, instance=subject)
            if form.is_valid():
                form.save()
                return redirect('list_subjects')
    else:
        form = SubjectForm(instance=subject)

    context = {
        'form': form,
        'subject': subject,
    }

    return render(request, 'edit_subject.html', context)

def list_students(request):
    students = User.objects.filter(role__name='STUDENT')
    return render(request, 'list_students.html', {'students': students})

def list_professors(request):
    professors = User.objects.filter(role__name='PROFESSOR')
    return render(request, 'list_professors.html', {'professors': professors})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CustomUserChangeForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'edit_user.html', context)

def enrollment_list(request):
    students = User.objects.filter(role__name='STUDENT')
    return render(request, 'enrollment_list.html', {'students': students})

def create_enrollment(request, student_id):
    student = get_object_or_404(User, id=student_id)
    subjects = Predmeti.objects.all()
    enrollments = []

    for subject in subjects:
        enrollment, created = Enrollment.objects.get_or_create(student=student, subject=subject)
        enrollments.append({'subject': subject, 'status': enrollment.status})

    if request.method == 'POST':
        for subject in subjects:
            status = request.POST.get(f'status_{subject.id}')
            enrollment = Enrollment.objects.get(student=student, subject=subject)
            
            if status in ['enrolled', 'not_enrolled']:
                enrollment.status = status
                enrollment.save()
        
        return redirect('list_students')
    
    return render(request, 'create_enrollment.html', {'student': student, 'subjects': subjects, 'enrollments': enrollments})

def enrolled_students(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    enrolled_students = Enrollment.objects.filter(subject_id=subject_id, status='enrolled')

    return render(request, 'enrolled_students.html', {'subject': subject, 'enrolled_students': enrolled_students})

def enrolled_subjects(request, student_id):
    student = get_object_or_404(User, id=student_id)
    enrolled_subjects = Predmeti.objects.filter(enrollment__student=student, enrollment__status='enrolled')
    return render(request, 'enrolled_subjects.html', {'student': student, 'enrolled_subjects': enrolled_subjects})


def class_attendance(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    students = subject.student_set.all()
    context = {
        'subject': subject,
        'students': students,
    }
    return render(request, 'class_attendance.html', context)

@login_required
def professor_dashboard(request):
    professor = Professor.objects.get(username=request.user.username)
    subjects = Predmeti.objects.filter(nositelj=professor)

    context = {
        'professor': professor,
        'subjects': subjects,
    }

    return render(request, 'professor_dashboard.html', context)

def enrolled_students_professor(request, subject_id):
    professor = Professor.objects.get(username=request.user.username)
    subject = get_object_or_404(Predmeti, id=subject_id, nositelj=professor)
    enrolled_students = Enrollment.objects.filter(subject_id=subject_id, status='enrolled')

    context = {
        'subject': subject,
        'enrolled_students': enrolled_students,
    }

    return render(request, 'enrolled_students_professor.html', context)

def update_enrollment_status(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        enrollment.status = status
        enrollment.save()
        return redirect('professor_dashboard')

    return render(request, 'update_enrollment_status.html', {'enrollment': enrollment})

def passed_students_professor(request, subject_id):
    subject = Predmeti.objects.get(id=subject_id)
    passed_students = Enrollment.objects.filter(subject=subject, status='passed')

    context = {
        'subject': subject,
        'passed_students': passed_students,
    }

    return render(request, 'passed_students.html', context)

def failed_students_professor(request, subject_id):
    subject = Predmeti.objects.get(id=subject_id)
    failed_students = Enrollment.objects.filter(subject=subject, status='failed')

    context = {
        'subject': subject,
        'failed_students': failed_students,
    }

    return render(request, 'failed_students.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Student, Predmeti

from django.shortcuts import render, get_object_or_404
from .models import Student, Predmeti

from django.shortcuts import render, get_object_or_404
from .models import Student, Predmeti, Enrollment

def student_dashboard(request):
    student_id = request.user.id
    student = get_object_or_404(Student, id=student_id)

    if student.status == 'red':
        # Redovni student
        completed_semesters = student.enrollment_set.filter(subject__sem_red__in=[1, 2])
    else:
        # Izvanredni student
        completed_semesters = student.enrollment_set.filter(subject__sem_izv__in=[1, 2])

    # Get the subjects from the completed semesters
    subjects = [enrollment.subject for enrollment in completed_semesters]

    # Check if all subjects from the completed semesters are set to "passed"
    all_passed = all(enrollment.status == 'passed' for enrollment in completed_semesters)

    if all_passed:
        if student.status == 'red':
            # Redovni student
            next_semesters = student.enrollment_set.filter(subject__sem_red__in=[3, 4])
        else:
            # Izvanredni student
            next_semesters = student.enrollment_set.filter(subject__sem_izv__in=[3, 4])

        # Get the subjects from the next semesters
        subjects += [enrollment.subject for enrollment in next_semesters]

    enrollments = Enrollment.objects.filter(student=student, subject__in=subjects)

    if request.method == 'POST':
        # Handle form submission
        for enrollment in enrollments:
            status_field_name = f"status_{enrollment.subject.id}"
            status = request.POST.get(status_field_name)
            enrollment.status = status
            enrollment.save()

    context = {
        'student': student,
        'enrollments': enrollments,
    }

    return render(request, 'student_dashboard.html', context)





from django.db.models import Count, Q

from django.db.models import Count, Case, When

from django.db.models import Count

def show_people(request):
    subjects = Predmeti.objects.all()
    subject_data = []

    for subject in subjects:
        total_passed = Enrollment.objects.filter(subject=subject, status='passed').count()
        regular_passed = Enrollment.objects.filter(subject=subject, student__status='red', status='passed').count()
        non_regular_passed = Enrollment.objects.filter(subject=subject, student__status='izv', status='passed').count()

        subject_data.append({
            'subject': subject,
            'total_passed': total_passed,
            'regular_passed': regular_passed,
            'non_regular_passed': non_regular_passed,
        })

    context = {
        'subject_data': subject_data,
    }

    return render(request, 'show_people.html', context)

def show_enrolled_students(request, subject_id):
    subject = Predmeti.objects.get(pk=subject_id)
    
    regular_students = User.objects.filter(enrollment__subject=subject, enrollment__status='passed', enrollment__student__status='red')
    non_regular_students = User.objects.filter(enrollment__subject=subject, enrollment__status='passed', enrollment__student__status='izv')

    context = {
        'subject': subject,
        'regular_students': regular_students,
        'non_regular_students': non_regular_students,
    }

    return render(request, 'show_enrolled_students.html', context)
