# view
from django.db import IntegrityError
from django.shortcuts import render, redirect
from scheduling.models import Pharmacy, Student, Shift
def success(request):
    return render(request, 'scheduling/success.html')

def pharmacy_scheduling(request):
    available_shifts = None
    if request.method == 'POST':
        student_id = request.POST.get('student_id', None)
        preferred_area = request.POST.get('preferred_area', None)
        preferred_start_time = request.POST.get('preferred_start_time', None)
        # Query for available shifts that match preferred area and start time
        available_pharmacy = Pharmacy.objects.get(area = preferred_area)
        available_shifts = Shift.objects.all().filter(pharmacy = available_pharmacy)
        student = Student.objects.get(id = student_id)
        # Try to assign the student to an available shift
        for shift in available_shifts:
            if (shift.capacity < shift.max_capacity):
                try:
                    student.assigned_shift = shift
                    student.save()
                    shift.capacity += 1;
                    shift.save()
                    break
                except IntegrityError:
                    # Shift was already filled by another student
                    continue

        # If no available shift was found, try to assign the student to any shift that matches the preferred start time
        if not student.assigned_shift:
            available_shift = Shift.objects.all().filter(start_time = preferred_start_time)
            ph = Shift.objects.get(start_time = preferred_start_time)
            for shift in available_shifts:
                if (shift.capacity < shift.max_capacity):
                    try:
                        student.assigned_shift = shift
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