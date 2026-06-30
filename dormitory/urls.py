from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # 宿舍楼
    path("buildings/", views.building_list, name="building_list"),
    path("buildings/create/", views.building_create, name="building_create"),
    path("buildings/<int:pk>/edit/", views.building_edit, name="building_edit"),
    path("buildings/<int:pk>/delete/", views.building_delete, name="building_delete"),
    # 宿舍房间
    path("dormitories/", views.dormitory_list, name="dormitory_list"),
    path("dormitories/create/", views.dormitory_create, name="dormitory_create"),
    path("dormitories/<int:pk>/edit/", views.dormitory_edit, name="dormitory_edit"),
    path("dormitories/<int:pk>/delete/", views.dormitory_delete, name="dormitory_delete"),
    # 学生
    path("students/", views.student_list, name="student_list"),
    path("students/create/", views.student_create, name="student_create"),
    path("students/<int:pk>/edit/", views.student_edit, name="student_edit"),
    path("students/<int:pk>/delete/", views.student_delete, name="student_delete"),
    # 住宿分配
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("assignments/create/", views.assignment_create, name="assignment_create"),
    path("assignments/<int:pk>/checkout/", views.assignment_checkout, name="assignment_checkout"),
    path("assignments/<int:pk>/delete/", views.assignment_delete, name="assignment_delete"),
    # 报修
    path("repairs/", views.repair_list, name="repair_list"),
    path("repairs/create/", views.repair_create, name="repair_create"),
    path("repairs/<int:pk>/edit/", views.repair_edit, name="repair_edit"),
    path("repairs/<int:pk>/delete/", views.repair_delete, name="repair_delete"),
]
