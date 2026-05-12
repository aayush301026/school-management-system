from django.contrib import admin
from .models import Register, Attendance, Result, Notice, Fees, Timetable

admin.site.register(Register)
admin.site.register(Attendance)
admin.site.register(Result)
admin.site.register(Notice)
admin.site.register(Fees)
admin.site.register(Timetable)