from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    """宿舍楼"""
    name = models.CharField("楼名", max_length=50, unique=True)
    address = models.CharField("地址", max_length=200, blank=True)
    floors = models.IntegerField("楼层数", default=6)
    description = models.TextField("描述", blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "宿舍楼"
        verbose_name_plural = "宿舍楼"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Dormitory(models.Model):
    """宿舍房间"""
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name="所属楼栋")
    room_number = models.CharField("房间号", max_length=20)
    floor = models.IntegerField("楼层")
    capacity = models.IntegerField("容量")
    current_count = models.IntegerField("当前人数", default=0)
    is_active = models.BooleanField("是否可用", default=True)
    description = models.TextField("描述", blank=True)

    class Meta:
        verbose_name = "宿舍房间"
        verbose_name_plural = "宿舍房间"
        unique_together = ["building", "room_number"]
        ordering = ["building", "room_number"]

    def __str__(self):
        return f"{self.building.name}-{self.room_number}"

    @property
    def available_beds(self):
        return self.capacity - self.current_count


class Student(models.Model):
    """学生"""
    GENDER_CHOICES = [("男", "男"), ("女", "女")]
    student_id = models.CharField("学号", max_length=20, unique=True)
    name = models.CharField("姓名", max_length=50)
    gender = models.CharField("性别", max_length=2, choices=GENDER_CHOICES)
    phone = models.CharField("电话", max_length=20, blank=True)
    department = models.CharField("院系", max_length=100, blank=True)
    major = models.CharField("专业", max_length=100, blank=True)
    enrollment_year = models.IntegerField("入学年份", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"
        ordering = ["student_id"]

    def __str__(self):
        return f"{self.name}({self.student_id})"


class Assignment(models.Model):
    """住宿分配"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="学生")
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, verbose_name="宿舍")
    check_in_date = models.DateField("入住日期", auto_now_add=True)
    check_out_date = models.DateField("退宿日期", null=True, blank=True)
    is_active = models.BooleanField("是否有效", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "住宿分配"
        verbose_name_plural = "住宿分配"
        ordering = ["-check_in_date"]

    def __str__(self):
        return f"{self.student.name} -> {self.dormitory}"


class Repair(models.Model):
    """报修"""
    STATUS_CHOICES = [
        ("pending", "待处理"),
        ("processing", "处理中"),
        ("completed", "已完成"),
    ]
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, verbose_name="宿舍")
    reporter_name = models.CharField("报修人", max_length=50)
    description = models.TextField("问题描述")
    report_date = models.DateTimeField("报修日期", auto_now_add=True)
    status = models.CharField("状态", max_length=20, choices=STATUS_CHOICES, default="pending")
    handler = models.CharField("处理人", max_length=50, blank=True)
    handle_date = models.DateTimeField("处理日期", null=True, blank=True)
    note = models.TextField("处理备注", blank=True)

    class Meta:
        verbose_name = "报修"
        verbose_name_plural = "报修"
        ordering = ["-report_date"]

    def __str__(self):
        return f"{self.dormitory} - {self.get_status_display()}"
