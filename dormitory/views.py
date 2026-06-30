from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Building, Dormitory, Student, Assignment, Repair

# ========== 首页 Dashboard ==========
@login_required
def index(request):
    context = {
        "building_count": Building.objects.count(),
        "dormitory_count": Dormitory.objects.count(),
        "student_count": Student.objects.count(),
        "active_assignments": Assignment.objects.filter(is_active=True).count(),
        "pending_repairs": Repair.objects.filter(status="pending").count(),
        "recent_repairs": Repair.objects.order_by("-report_date")[:5],
    }
    return render(request, "dormitory/index.html", context)


# ========== 宿舍楼 CRUD ==========
@login_required
def building_list(request):
    buildings = Building.objects.all()
    return render(request, "dormitory/building_list.html", {"buildings": buildings})

@login_required
def building_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address", "")
        floors = request.POST.get("floors", 6)
        description = request.POST.get("description", "")
        Building.objects.create(name=name, address=address, floors=floors, description=description)
        messages.success(request, "宿舍楼添加成功")
        return redirect("building_list")
    return render(request, "dormitory/building_form.html", {"is_edit": False})

@login_required
def building_edit(request, pk):
    building = get_object_or_404(Building, pk=pk)
    if request.method == "POST":
        building.name = request.POST.get("name")
        building.address = request.POST.get("address", "")
        building.floors = request.POST.get("floors", 6)
        building.description = request.POST.get("description", "")
        building.save()
        messages.success(request, "宿舍楼修改成功")
        return redirect("building_list")
    return render(request, "dormitory/building_form.html", {"building": building, "is_edit": True})

@login_required
def building_delete(request, pk):
    building = get_object_or_404(Building, pk=pk)
    building.delete()
    messages.success(request, "宿舍楼删除成功")
    return redirect("building_list")


# ========== 宿舍房间 CRUD ==========
@login_required
def dormitory_list(request):
    dormitories = Dormitory.objects.select_related("building").all()
    return render(request, "dormitory/dormitory_list.html", {"dormitories": dormitories})

@login_required
def dormitory_create(request):
    buildings = Building.objects.all()
    if request.method == "POST":
        building_id = request.POST.get("building")
        room_number = request.POST.get("room_number")
        floor = request.POST.get("floor")
        capacity = request.POST.get("capacity")
        current_count = request.POST.get("current_count", 0)
        description = request.POST.get("description", "")
        Dormitory.objects.create(
            building_id=building_id, room_number=room_number,
            floor=floor, capacity=capacity,
            current_count=current_count, description=description
        )
        messages.success(request, "宿舍房间添加成功")
        return redirect("dormitory_list")
    return render(request, "dormitory/dormitory_form.html", {"buildings": buildings, "is_edit": False})

@login_required
def dormitory_edit(request, pk):
    dorm = get_object_or_404(Dormitory, pk=pk)
    buildings = Building.objects.all()
    if request.method == "POST":
        dorm.building_id = request.POST.get("building")
        dorm.room_number = request.POST.get("room_number")
        dorm.floor = request.POST.get("floor")
        dorm.capacity = request.POST.get("capacity")
        dorm.current_count = request.POST.get("current_count", 0)
        dorm.is_active = request.POST.get("is_active") == "on"
        dorm.description = request.POST.get("description", "")
        dorm.save()
        messages.success(request, "宿舍房间修改成功")
        return redirect("dormitory_list")
    return render(request, "dormitory/dormitory_form.html", {"dorm": dorm, "buildings": buildings, "is_edit": True})

@login_required
def dormitory_delete(request, pk):
    dorm = get_object_or_404(Dormitory, pk=pk)
    dorm.delete()
    messages.success(request, "宿舍房间删除成功")
    return redirect("dormitory_list")


# ========== 学生 CRUD ==========
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "dormitory/student_list.html", {"students": students})

@login_required
def student_create(request):
    if request.method == "POST":
        Student.objects.create(
            student_id=request.POST.get("student_id"),
            name=request.POST.get("name"),
            gender=request.POST.get("gender"),
            phone=request.POST.get("phone", ""),
            department=request.POST.get("department", ""),
            major=request.POST.get("major", ""),
            enrollment_year=request.POST.get("enrollment_year") or None,
        )
        messages.success(request, "学生添加成功")
        return redirect("student_list")
    return render(request, "dormitory/student_form.html", {"is_edit": False})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.student_id = request.POST.get("student_id")
        student.name = request.POST.get("name")
        student.gender = request.POST.get("gender")
        student.phone = request.POST.get("phone", "")
        student.department = request.POST.get("department", "")
        student.major = request.POST.get("major", "")
        student.enrollment_year = request.POST.get("enrollment_year") or None
        student.save()
        messages.success(request, "学生信息修改成功")
        return redirect("student_list")
    return render(request, "dormitory/student_form.html", {"student": student, "is_edit": True})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    messages.success(request, "学生删除成功")
    return redirect("student_list")


# ========== 住宿分配 CRUD ==========
@login_required
def assignment_list(request):
    assignments = Assignment.objects.select_related("student", "dormitory__building").all()
    return render(request, "dormitory/assignment_list.html", {"assignments": assignments})

@login_required
def assignment_create(request):
    students = Student.objects.all()
    dormitories = Dormitory.objects.select_related("building").filter(is_active=True)
    if request.method == "POST":
        student_id = request.POST.get("student")
        dormitory_id = request.POST.get("dormitory")
        Assignment.objects.create(student_id=student_id, dormitory_id=dormitory_id)
        # 更新宿舍当前人数
        dorm = Dormitory.objects.get(pk=dormitory_id)
        dorm.current_count = Assignment.objects.filter(dormitory=dorm, is_active=True).count()
        dorm.save()
        messages.success(request, "住宿分配成功")
        return redirect("assignment_list")
    return render(request, "dormitory/assignment_form.html", {"students": students, "dormitories": dormitories})

@login_required
def assignment_checkout(request, pk):
    from datetime import date
    assignment = get_object_or_404(Assignment, pk=pk)
    assignment.is_active = False
    assignment.check_out_date = date.today()
    assignment.save()
    dorm = assignment.dormitory
    dorm.current_count = Assignment.objects.filter(dormitory=dorm, is_active=True).count()
    dorm.save()
    messages.success(request, f"{assignment.student.name} 已退宿")
    return redirect("assignment_list")

@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    dorm = assignment.dormitory
    assignment.delete()
    dorm.current_count = Assignment.objects.filter(dormitory=dorm, is_active=True).count()
    dorm.save()
    messages.success(request, "分配记录已删除")
    return redirect("assignment_list")


# ========== 报修 CRUD ==========
@login_required
def repair_list(request):
    repairs = Repair.objects.select_related("dormitory__building").all()
    return render(request, "dormitory/repair_list.html", {"repairs": repairs})

@login_required
def repair_create(request):
    dormitories = Dormitory.objects.select_related("building").filter(is_active=True)
    if request.method == "POST":
        Repair.objects.create(
            dormitory_id=request.POST.get("dormitory"),
            reporter_name=request.POST.get("reporter_name"),
            description=request.POST.get("description"),
        )
        messages.success(request, "报修提交成功")
        return redirect("repair_list")
    return render(request, "dormitory/repair_form.html", {"dormitories": dormitories})

@login_required
def repair_edit(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    if request.method == "POST":
        repair.status = request.POST.get("status")
        repair.handler = request.POST.get("handler", "")
        repair.note = request.POST.get("note", "")
        if repair.status == "completed" and not repair.handle_date:
            from datetime import date
            repair.handle_date = date.today()
        repair.save()
        messages.success(request, "报修信息已更新")
        return redirect("repair_list")
    return render(request, "dormitory/repair_form.html", {"repair": repair, "is_edit": True})

@login_required
def repair_delete(request, pk):
    repair = get_object_or_404(Repair, pk=pk)
    repair.delete()
    messages.success(request, "报修记录已删除")
    return redirect("repair_list")
