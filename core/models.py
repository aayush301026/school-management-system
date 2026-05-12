from django.db import models

class Register(models.Model):

    ROLE_CHOICES = (

        ('Student','Student'),
        ('Teacher','Teacher'),

    )

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    password = models.CharField(max_length=100)

    address = models.TextField(null=True, blank=True)

    profile_image = models.ImageField(upload_to='profiles/',null=True,blank=True)

    def __str__(self):

        return self.name



class Attendance(models.Model):

    student = models.ForeignKey(Register,on_delete=models.CASCADE)

    status = models.CharField(max_length=20)

    date = models.DateField(auto_now_add=True)

    def __str__(self):

     return self.name
    
class Result(models.Model):

    student = models.ForeignKey(Register,on_delete=models.CASCADE)

    subject1 = models.CharField(max_length=100)
    subject1_marks = models.IntegerField()

    subject2 = models.CharField(max_length=100)
    subject2_marks = models.IntegerField()

    subject3 = models.CharField(max_length=100)
    subject3_marks = models.IntegerField()

    subject4 = models.CharField(max_length=100)
    subject4_marks = models.IntegerField()

    subject5 = models.CharField(max_length=100)
    subject5_marks = models.IntegerField()

    subject6 = models.CharField(max_length=100)
    subject6_marks = models.IntegerField()

    total_marks = models.IntegerField()

    obtained_marks = models.IntegerField()

    percentage = models.FloatField()

    grade = models.CharField(max_length=5)

    def __str__(self):

        return self.student.name
    
class Notice(models.Model):

    title = models.CharField(max_length=200)

    message = models.TextField()

    date = models.DateField(auto_now_add=True)

    def __str__(self):

        return self.title
    
class Fees(models.Model):

    student = models.ForeignKey(Register,on_delete=models.CASCADE)

    admission_fees = models.IntegerField()

    tuition_fees = models.IntegerField()

    exam_fees = models.IntegerField()

    dress_fees = models.IntegerField()

    book_fees = models.IntegerField()

    transport_fees = models.IntegerField()

    insurance_fees = models.IntegerField()

    total_fees = models.IntegerField()

    paid_fees = models.IntegerField()

    remaining_fees = models.IntegerField()

    status = models.CharField(max_length=20)

    def __str__(self):

        return self.student.name
    
class Timetable(models.Model):

    day = models.CharField(max_length=20)

    period1 = models.CharField(max_length=100)

    period2 = models.CharField(max_length=100)

    period3 = models.CharField(max_length=100)

    period4 = models.CharField(max_length=100)

    period5 = models.CharField(max_length=100)

    period6 = models.CharField(max_length=100)

    def __str__(self):

        return self.day