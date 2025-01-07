from django.shortcuts import render, get_object_or_404
from .models import Attendance, Employee
from datetime import datetime


def mark_attendance(request, emp_id):
    employee = get_object_or_404(Employee, emp_id=emp_id)
    today = datetime.today().date()
    now = datetime.now().time()

    attendance, created = Attendance.objects.get_or_create(employee=employee, date=today)

    if not attendance.check_in:
        attendance.check_in = now
        message = f"{employee.name}'s Check-in recorded at {now}."
    elif not attendance.check_out:
        attendance.check_out = now
        message = f"{employee.name}'s Check-out recorded at {now}."
    else:
        message = f"Attendance for {employee.name} is already marked for today."

    attendance.save()
    return render(request, 'attendance/mark.html', {'message': message})


def daily_report(request):
    today = datetime.today().date()
    attendance_records = Attendance.objects.filter(date=today)
    return render(request, 'attendance/daily_report.html', {'attendance_records': attendance_records})


from django.http import HttpResponse
from reportlab.pdfgen import canvas


def export_daily_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="daily_report.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Daily Attendance Report")
    p.drawString(100, 780, f"Date: {datetime.today().date()}")

    y = 750
    p.drawString(50, y, "Employee Name")
    p.drawString(200, y, "Check-in")
    p.drawString(300, y, "Check-out")
    p.drawString(400, y, "Hours")
    p.drawString(500, y, "Status")

    y -= 20
    attendance_records = Attendance.objects.filter(date=datetime.today().date())
    for record in attendance_records:
        p.drawString(50, y, record.employee.name)
        p.drawString(200, y, str(record.check_in or "-"))
        p.drawString(300, y, str(record.check_out or "-"))
        p.drawString(400, y, str(record.total_hours or "0.0"))
        p.drawString(500, y, record.status)
        y -= 20

    p.save()
    return response
