from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from .models import Register, Attendance, Result, Notice, Fees, Timetable
from datetime import date
from django.shortcuts import render,redirect

def home(request):
    return render(request, 'index.html')


def register_page(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password')

        Register.objects.create(

            name=name,
            email=email,
            phone=phone,
            role=role,
            password=password

        )

        return redirect('/login/')

    return render(request, 'register.html')


def login_page(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Register.objects.filter(

            email=email,
            password=password

        ).first()

        if user:

            request.session['user_id'] = user.id

            if user.role == "Student":

                return redirect('/student-dashboard/')

            else:

                return redirect('/teacher-dashboard/')

    return render(request, 'login.html')


def dashboard(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user_id = request.session.get('user_id')

    user = Register.objects.get(id=user_id)

    context = {

        'user': user

    }

    return render(request, 'dashboard.html', context)


def student_dashboard(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user_id = request.session.get('user_id')

    user = Register.objects.get(id=user_id)

    context = {

        'user': user

    }

    return render(request, 'student_dashboard.html', context)


def teacher_dashboard(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user_id = request.session.get('user_id')

    user = Register.objects.get(id=user_id)

    context = {

        'user': user

    }

    return render(request, 'teacher_dashboard.html', context)

from datetime import date


def mark_attendance(request):

    students = Register.objects.filter(
        role='Student'
    )

    today = date.today()

    message = ""

    if request.method == "POST":

        student_id = request.POST.get('student_id')

        status = request.POST.get('status')

        student = Register.objects.get(
            id=student_id
        )

        already_marked = Attendance.objects.filter(

            student=student,
            date=today

        ).exists()

        if not already_marked:

            Attendance.objects.create(

                student=student,
                status=status

            )

            message = f"{status} marked for {student.name}"

    student_data = []

    for student in students:

        attendance = Attendance.objects.filter(

            student=student,
            date=today

        ).first()

        if attendance:

            current_status = attendance.status

        else:

            current_status = ""

        student_data.append({

            'student':student,
            'status':current_status

        })

    context = {

        'student_data':student_data,
        'message':message

    }

    return render(

        request,
        'mark_attendance.html',
        context

    )

def attendance_records(request):

    records = Attendance.objects.all().order_by('-date')

    context = {

        'records':records

    }

    return render(request,'attendance_records.html',context)

def delete_attendance(request,id):

    record = Attendance.objects.get(id=id)

    record.delete()

    return redirect('attendance_records')

def upload_result(request):

    students = Register.objects.filter(role='Student')

    message = ""

    if request.method == "POST":

        student_id = request.POST.get('student_id')

        subject1 = request.POST.get('subject1')
        subject1_marks = int(request.POST.get('subject1_marks'))

        subject2 = request.POST.get('subject2')
        subject2_marks = int(request.POST.get('subject2_marks'))

        subject3 = request.POST.get('subject3')
        subject3_marks = int(request.POST.get('subject3_marks'))

        subject4 = request.POST.get('subject4')
        subject4_marks = int(request.POST.get('subject4_marks'))

        subject5 = request.POST.get('subject5')
        subject5_marks = int(request.POST.get('subject5_marks'))

        subject6 = request.POST.get('subject6')
        subject6_marks = int(request.POST.get('subject6_marks'))

        total_marks = 600

        obtained_marks = (

            subject1_marks +
            subject2_marks +
            subject3_marks +
            subject4_marks +
            subject5_marks +
            subject6_marks

        )

        percentage = (obtained_marks / total_marks) * 100

        if percentage >= 90:

            grade = "A+"

        elif percentage >= 75:

            grade = "A"

        elif percentage >= 60:

            grade = "B"

        elif percentage >= 40:

            grade = "C"

        else:

            grade = "F"

        student = Register.objects.get(id=student_id)

        Result.objects.create(

            student=student,

            subject1=subject1,
            subject1_marks=subject1_marks,

            subject2=subject2,
            subject2_marks=subject2_marks,

            subject3=subject3,
            subject3_marks=subject3_marks,

            subject4=subject4,
            subject4_marks=subject4_marks,

            subject5=subject5,
            subject5_marks=subject5_marks,

            subject6=subject6,
            subject6_marks=subject6_marks,

            total_marks=total_marks,

            obtained_marks=obtained_marks,

            percentage=percentage,

            grade=grade

        )

        message = "Result Uploaded Successfully"

    context = {

        'students': students,
        'message': message

    }

    return render(request, 'upload_result.html', context)
    
def student_results(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user_id = request.session.get('user_id')

    user = Register.objects.get(id=user_id)

    results = Result.objects.filter(student=user)

    context = {

        'results':results,
        'user':user

    }

    return render(request,'student_results.html',context)

def add_notice(request):

    message = ""

    if request.method == "POST":

        title = request.POST.get('title')

        notice_message = request.POST.get('message')

        Notice.objects.create(

            title=title,
            message=notice_message

        )

        message = "Notice Added Successfully"

    return render(request,'add_notice.html',{'message':message})

def view_notices(request):

    notices = Notice.objects.all().order_by('-id')

    context = {

        'notices':notices

    }

    return render(request,'view_notices.html',context)

def student_profile(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user_id = request.session.get('user_id')

    user = Register.objects.get(id=user_id)

    message = ""

    if request.method == "POST":

        user.name = request.POST.get('name')

        user.phone = request.POST.get('phone')

        user.address = request.POST.get('address')

        if request.FILES.get('profile_image'):

            user.profile_image = request.FILES.get('profile_image')

        user.save()

        message = "Profile Updated Successfully"

    context = {

        'user':user,
        'message':message

    }

    return render(request,'student_profile.html',context)

def add_fees(request):

    students = Register.objects.filter(role='Student')

    message = ""

    if request.method == "POST":

        student_id = request.POST.get('student_id')

        admission_fees = int(request.POST.get('admission_fees'))

        tuition_fees = int(request.POST.get('tuition_fees'))

        exam_fees = int(request.POST.get('exam_fees'))

        dress_fees = int(request.POST.get('dress_fees'))

        book_fees = int(request.POST.get('book_fees'))

        transport_fees = int(request.POST.get('transport_fees'))

        insurance_fees = int(request.POST.get('insurance_fees'))

        paid_fees = int(request.POST.get('paid_fees'))

        total_fees = (

            admission_fees +
            tuition_fees +
            exam_fees +
            dress_fees +
            book_fees +
            transport_fees +
            insurance_fees

        )

        remaining_fees = total_fees - paid_fees

        if remaining_fees <= 0:

            status = "Paid"

            remaining_fees = 0

        else:

            status = "Pending"

        student = Register.objects.get(id=student_id)

        Fees.objects.create(

            student=student,

            admission_fees=admission_fees,

            tuition_fees=tuition_fees,

            exam_fees=exam_fees,

            dress_fees=dress_fees,

            book_fees=book_fees,

            transport_fees=transport_fees,

            insurance_fees=insurance_fees,

            total_fees=total_fees,

            paid_fees=paid_fees,

            remaining_fees=remaining_fees,

            status=status

        )

        message = "Fees Added Successfully"

    context = {

        'students':students,
        'message':message

    }

    return render(request,'add_fees.html',context)

def student_fees(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user_id = request.session.get('user_id')

    user = Register.objects.get(id=user_id)

    fees = Fees.objects.filter(student=user)

    context = {

        'fees':fees

    }

    return render(request,'student_fees.html',context)
def update_fees(request,id):

    fee = Fees.objects.get(id=id)

    message = ''

    if request.method == "POST":

        new_paid_amount = int(request.POST.get('new_paid_amount'))

        fee.paid_fees += new_paid_amount

        fee.remaining_fees = fee.total_fees - fee.paid_fees

        if fee.remaining_fees <= 0:

            fee.status = "Paid"

            fee.remaining_fees = 0

        else:

            fee.status = "Pending"

        fee.save()

        message = "Fees Updated Successfully"

    context = {

        'fee':fee,
        'message':message

    }

    return render(request,'update_fees.html',context)

def delete_fees(request,id):

    fee = Fees.objects.get(id=id)

    fee.delete()

    return redirect('manage_fees')

    
def manage_fees(request):

    fees = Fees.objects.all()

    return render(request,'manage_fees.html',{'fees':fees})

def add_timetable(request):

    message = ""

    if request.method == "POST":

        day = request.POST.get('day')

        period1 = request.POST.get('period1')

        period2 = request.POST.get('period2')

        period3 = request.POST.get('period3')

        period4 = request.POST.get('period4')

        period5 = request.POST.get('period5')

        period6 = request.POST.get('period6')

        Timetable.objects.create(

            day=day,

            period1=period1,

            period2=period2,

            period3=period3,

            period4=period4,

            period5=period5,

            period6=period6

        )

        message = "Timetable Added Successfully"

    return render(request,'add_timetable.html',{'message':message})

def view_timetable(request):

    timetable = Timetable.objects.all()

    return render(request,'view_timetable.html',{'timetable':timetable})

def analytics_dashboard(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user = Register.objects.get(

        id=request.session.get('user_id')

    )

    if user.role != "Teacher":

        return redirect('/login/')

    total_students = Register.objects.filter(
        role='Student'
    ).count()

    total_teachers = Register.objects.filter(
        role='Teacher'
    ).count()

    total_results = Result.objects.count()

    topper = Result.objects.order_by(
        '-percentage'
    ).first()

    average_percentage = 0

    results = Result.objects.all()

    if results.exists():

        total_percentage = 0

        for result in results:

            total_percentage += result.percentage

        average_percentage = total_percentage / results.count()

    pass_students = Result.objects.filter(
        percentage__gte=40
    ).count()

    fail_students = Result.objects.filter(
        percentage__lt=40
    ).count()

    context = {

        'total_students':total_students,

        'total_teachers':total_teachers,

        'total_results':total_results,

        'topper':topper,

        'average_percentage':round(average_percentage,2),

        'pass_students':pass_students,

        'fail_students':fail_students

    }

    return render(request,'analytics_dashboard.html',context)

def download_result_pdf(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user = Register.objects.get(

        id=request.session.get('user_id')

    )

    if user.role != "Student":

        return redirect('/login/')

    result = Result.objects.filter(
        student=user
    ).first()

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        'attachment; filename="result.pdf"'
    )

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold",20)

    p.drawString(180,800,"School Result Report")

    p.setFont("Helvetica",14)

    p.drawString(50,750,f"Student Name: {user.name}")

    p.drawString(50,720,f"Email: {user.email}")

    p.drawString(50,690,"Subjects & Marks")

    y = 650

    subjects = [

        (result.subject1,result.subject1_marks),

        (result.subject2,result.subject2_marks),

        (result.subject3,result.subject3_marks),

        (result.subject4,result.subject4_marks),

        (result.subject5,result.subject5_marks),

        (result.subject6,result.subject6_marks),

    ]

    for subject,marks in subjects:

        p.drawString(

            80,
            y,
            f"{subject} : {marks}"

        )

        y -= 30

    p.drawString(

        50,
        y-20,
        f"Total Marks: {result.total_marks}"

    )

    p.drawString(

        50,
        y-50,
        f"Obtained Marks: {result.obtained_marks}"

    )

    p.drawString(

        50,
        y-80,
        f"Percentage: {result.percentage}%"

    )

    p.drawString(

        50,
        y-110,
        f"Grade: {result.grade}"

    )

    p.save()

    return response

def student_attendance(request):

    if not request.session.get('user_id'):

        return redirect('/login/')

    user = Register.objects.get(

        id=request.session.get('user_id')

    )

    attendance = Attendance.objects.filter(

        student=user

    ).order_by('-date')

    return render(

        request,
        'student_attendance.html',
        {'attendance':attendance}

    )

def logout_page(request):

    request.session.flush()

    return redirect('/login/')