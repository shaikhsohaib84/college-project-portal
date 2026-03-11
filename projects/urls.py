from django.urls import path
from . import views


urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("submit/", views.submit_project, name="submit_project"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("edit/<int:project_id>/", views.edit_project, name="edit_project"),
    path("approve/<int:project_id>/", views.approve_project, name="approve_project"),
    path("reject/<int:project_id>/", views.reject_project, name="reject_project"),
    path("delete/<int:project_id>/", views.delete_project, name="delete_project"),
    path("download/<int:project_id>/", views.download_project_file, name="download_project_file"),
    path("teacher/", views.teacher_dashboard, name="teacher_dashboard"),
]

