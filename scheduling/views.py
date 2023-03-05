# view
from django.db import IntegrityError
from django.shortcuts import render, redirect
from scheduling.models import Pharmacy, Student, Shift

def fail(request,context):
    return render(request, 'scheduling/fail.html',context)

def success(request):
    return render(request, 'scheduling/success.html')

def pharmacy_scheduling(request):
    if request.method == 'POST':
        available_shifts = None
        student_id = request.POST.get('student_id', None)
        student = Student.objects.get(id = student_id)
        preferred_start_time = request.POST.get('preferred_start_time', None)
        print(student.tries)
        if student.tries != 0:    
            return render(request,'scheduling/fail.html',{'s' : student})    
        # Query for available shifts that match preferred area and start time
        available_shifts = Shift.objects.all().filter(start_time = preferred_start_time)
        student = Student.objects.get(id = student_id)
        # Try to assign the student to an available shift
        for shift in available_shifts:
            if (shift.capacity < shift.max_capacity  and student.tries < 1):
                try:
                    student.assigned_shift = shift
                    student.tries += 1
                    student.save()
                    shift.capacity += 1;
                    shift.save()
                    break
                except IntegrityError:
                    # Shift was already filled by another student
                    continue
        # If no available shift was found, try to assign the student to any shift that matches)
        if not student.assigned_shift and student.tries < 1:
            available_shift = Shift.objects.all().filter(start_time = preferred_start_time)
            ph = Shift.objects.get(start_time = preferred_start_time)
            for shift in available_shifts:
                if (shift.capacity < shift.max_capacity):
                    try:
                        student.assigned_shift = shift
                        student.tries += 1
                        student.save()
                        shift.capacity += 1
                        shift.save()
                        break
                    except IntegrityError:
                        # Shift was already filled by another student
                        continue
        return render(request, 'scheduling/success.html',{'s':student,'ph':shift.pharmacy})
    else:
        pharmacies = Pharmacy.objects.all()
        shifts = Shift.objects.all()
        context = {'pharmacies':pharmacies,'shifts':shifts}
        return render(request, 'scheduling.html',context)   