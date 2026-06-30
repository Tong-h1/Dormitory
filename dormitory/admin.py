from django.contrib import admin
from .models import Building, Dormitory, Student, Assignment, Repair

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "floors", "created_at"]
    search_fields = ["name"]

@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ["building", "room_number", "floor", "capacity", "current_count", "is_active"]
    list_filter = ["building", "is_active"]
    search_fields = ["room_number"]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["student_id", "name", "gender", "department", "enrollment_year"]
    search_fields = ["student_id", "name"]
    list_filter = ["gender", "department"]

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["student", "dormitory", "check_in_date", "is_active"]
    list_filter = ["is_active"]

@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ["dormitory", "reporter_name", "status", "report_date"]
    list_filter = ["status"]
