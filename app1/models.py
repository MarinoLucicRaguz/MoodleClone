from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            roles = ['ADMIN', 'STUDENT', 'PROFESSOR']
            for role in roles:
                Role.objects.create(name=role)

        super().save(*args, **kwargs)

class User(AbstractUser):
    objects = UserManager()
    STATUS = (
        ('none', 'None'),
        ('izv', 'izvanredni student'),
        ('red', 'redovni student')
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.role_id:
                self.role = Role.objects.get(name='ADMIN')
            if not self.is_superuser:
                self.password = make_password(self.password)
        return super().save(*args, **kwargs)

    
class Professor(User):

    class Meta:
        proxy = True

    def __str__(self):
        return self.username

class Student(User):

    class Meta:
        proxy = True

    def __str__(self):
        return self.username

class Predmeti(models.Model):
    IZBORNI_CHOICES = (
        ('True', 'Da'),
        ('False', 'Ne'),
    )
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)   
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI_CHOICES)
    nositelj = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE,
        limit_choices_to={'role__name': 'PROFESSOR'},
        default=None,
        null=True,
        blank=True
    )

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('not_enrolled', 'Not enrolled'),
        ('enrolled', 'Enrolled'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_enrolled')

    def __str__(self):
        return f"Enrollment: Student {self.student.username}, Subject {self.subject.name}, Status {self.get_status_display()}"
    
    from django.core.exceptions import ValidationError

    def clean(self):
        # Perform additional validation
        if self.student.status == 'red' and self.subject.sem_red == 3:
            # Regular student trying to enroll in third-year subject
            passed_first_year = Enrollment.objects.filter(
                student=self.student,
                subject__sem_red__in=[1, 2],
                status='passed'
            ).count()
            if passed_first_year != 2:
                raise ValidationError('Regular students must pass all first-year semesters.')

        if self.student.status == 'izv' and self.subject.sem_red == 4:
            # Non-regular student trying to enroll in fourth-year subject
            passed_second_and_third_year = Enrollment.objects.filter(
                student=self.student,
                subject__sem_red__in=[2, 3],
                status='passed'
            ).count()
            if passed_second_and_third_year != 4:
                raise ValidationError('Non-regular students must pass all second-year and third-year semesters.')
