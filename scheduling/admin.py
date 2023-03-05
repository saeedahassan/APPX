from django.contrib import admin
from .models import Pharmacy, Student, Shift


class SiteAdminArea(admin.AdminSite):
    site_header = 'AAU - Pharmacy Training'
    base_template = 'admin/base.html'
    login_template = 'admin/login.html'

aau_site = SiteAdminArea('AAU College of Pharmacy Faculty')

class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 1

class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name','area')
    inlines = [ShiftInline]

aau_site.register(Pharmacy,PharmacyAdmin)


class ShiftAdmin(admin.ModelAdmin):
    list_display = ('pharmacy', 'start_time', 'end_time', 'capacity','max_capacity')


class StudentAdmin(admin.ModelAdmin):
    list_display= ('id', 'name','assigned_shift') 
       
aau_site.register(Student,StudentAdmin)
