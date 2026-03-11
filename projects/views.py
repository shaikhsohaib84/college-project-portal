from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from django.contrib import messages
from django.http import FileResponse, Http404
from accounts.models import User

@login_required
def project_list(request):
    # Public page → only approved projects
    projects = Project.objects.filter(status="approved")
    return render(request, "projects/project_list.html", {"projects": projects})


@login_required
def student_dashboard(request):
    # Show only projects created by logged-in user
    projects = Project.objects.filter(owner=request.user)
    return render(request, "projects/student_dashboard.html", {"projects": projects})


@login_required
def admin_dashboard(request):
    # Only staff can access this page
    if not request.user.is_staff:
        return redirect("project_list")

    projects = Project.objects.all()
    return render(request, "projects/admin_dashboard.html", {"projects": projects})


@login_required
def approve_project(request, project_id):

    if request.user.role != "teacher" and not request.user.is_superuser:
        return redirect("student_dashboard")

    project = get_object_or_404(Project, id=project_id)

    project.status = "approved"
    project.save()

    return redirect("teacher_dashboard")



@login_required
def reject_project(request, project_id):

    if request.user.role != "teacher" and not request.user.is_superuser:
        return redirect("student_dashboard")

    project = get_object_or_404(Project, id=project_id)

    project.status = "rejected"
    project.save()

    return redirect("teacher_dashboard")

@login_required
def submit_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect("student_dashboard")
    else:
        form = ProjectForm()

    return render(request, "projects/submit_project.html", {"form": form})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Only owner can edit
    if project.owner != request.user:
        return redirect("student_dashboard")

    # Only allow editing if pending
    if project.status != "pending":
        return redirect("student_dashboard")

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request,"project updated succesfully ")
            return redirect("student_dashboard")
    else:
        form = ProjectForm(instance=project)

    return render(request, "projects/edit_project.html", {"form": form})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Only owner can delete
    if project.owner != request.user:
        return redirect("student_dashboard")

    # Only pending projects can be deleted
    if project.status != "pending":
        return redirect("student_dashboard")

    if request.method == "POST":
        project.delete()
        messages.success(request,"project succesfully deleted niggah")
        return redirect("student_dashboard")

    return render(request, "projects/delete_project.html", {"project": project})

@login_required
def download_project_file(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Allow owner OR teacher OR superuser
    if (
        request.user != project.owner
        and request.user.role != "teacher"
        and not request.user.is_superuser
    ):
        raise Http404()

    if not project.file:
        raise Http404("File not found")

    return FileResponse(project.file.open(), as_attachment=True)

@login_required
def teacher_dashboard(request):

    if request.user.role != "teacher" and not request.user.is_superuser:
        return redirect("student_dashboard")

    projects = Project.objects.all().order_by("-id")

    return render(
        request,
        "projects/teacher_dashboard.html",
        {"projects": projects},
    )