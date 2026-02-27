from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from .models import Job
# from .models import Requirnment

def job_list(request):
    jobs = Job.objects.all()
    paginator = Paginator(jobs, 5)  # 5 jobs per page
    page_number = request.GET.get('page')
    jobs = paginator.get_page(page_number)

    return render(request, 'jobs/jobs.html', {'jobs': jobs})

def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    # requirment = get_object_or_404(Requirnment)  
    similar_jobs = Job.objects.filter(
        job_type=job.job_type
    ).exclude(id=job.id)[:5]
    return render(request, 'jobs/job_detail.html', {'job': job,'similar_jobs': similar_jobs})