from django.urls import path
from AppJob.use_cases import list_job
from AppJob.use_cases.list_question import analyze_question_stream
from AppJob.use_cases.skill_project_gap import analyze_job_stream

urlpatterns = [
    path('job_list/', list_job.job_list, name='JobListing'),
    path('analyze-job-stream/',analyze_job_stream,name='analyze_job_stream' ),
    path('analyze-question-stream/',analyze_question_stream,name='analyze_question_stream' ),
]


