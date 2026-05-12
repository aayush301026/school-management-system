from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('register/', views.register_page, name='register'),

    path('login/', views.login_page, name='login'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('logout/', views.logout_page, name='logout'),

    path('mark-attendance/',views.mark_attendance,name='mark_attendance'),

    path('attendance-records/',views.attendance_records,name='attendance_records'),

    path('delete-attendance/<int:id>/',views.delete_attendance,name='delete_attendance'),

    path('upload-result/',views.upload_result,name='upload_result'),

    path('student-results/',views.student_results,name='student_results'),

    path('add-notice/',views.add_notice,name='add_notice'),

    path('view-notices/',views.view_notices,name='view_notices'),

    path('student-profile/',views.student_profile,name='student_profile'),

    path('add-fees/',views.add_fees,name='add_fees'),

    path('student-fees/',views.student_fees,name='student_fees'),

    path('update-fees/<int:id>/',views.update_fees,name='update_fees'),
    
    path('delete-fees/<int:id>/',views.delete_fees,name='delete_fees'),

    path('manage-fees/',views.manage_fees,name='manage_fees'),

    path('add-timetable/',views.add_timetable,name='add_timetable'),

    path('view-timetable/',views.view_timetable,name='view_timetable'),

    path('analytics-dashboard/',views.analytics_dashboard,name='analytics_dashboard'),

    path('download-result-pdf/',views.download_result_pdf,name='download_result_pdf'),

    path('student-attendance/', views.student_attendance, name='student_attendance'),

]