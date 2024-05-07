from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from main.forms import JobForm, EmployerUpdateForm, WorkerUpdateForm, CustomUserCreationForm
from main.models import Job


@login_required
def toggle_role(request):
    user = request.user
    user.is_employer = not user.is_employer
    user.save()
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    active_jobs = user.get_active_jobs() if user.is_employer else []
    inactive_jobs = user.get_inactive_jobs() if user.is_employer else []

    if request.method == 'POST':
        if user.is_employer:
            form = EmployerUpdateForm(request.POST, instance=user)
        else:
            form = WorkerUpdateForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        if user.is_employer:
            form = EmployerUpdateForm(instance=user)
        else:
            form = WorkerUpdateForm(instance=user)

    return render(request, 'main/profile.html', {
        'active_jobs': active_jobs,
        'inactive_jobs': inactive_jobs,
        'form': form
    })


def index(request):
    return render(request, 'main/index.html')


@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('jobs')
    else:
        form = JobForm()
    return render(request, 'main/add_job.html', {'form': form})


@login_required
def show_jobs(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        jobs = Job.objects.all()
    return render(request, 'main/show_jobs.html', {'jobs': jobs})
