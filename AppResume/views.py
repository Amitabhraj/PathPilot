from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .UseCases.rag.rag_pipeline import (
    analyze_resume_pipeline
)

import os


@csrf_exempt
def analyze_resume(request):

    if request.method != "POST":

        return JsonResponse({
            "success": False,
            "error": "Only POST request allowed"
        })

    try:

        uploaded_file = request.FILES.get("resume")

        if not uploaded_file:

            return JsonResponse({
                "success": False,
                "error": "No resume uploaded"
            })

        upload_folder = "media/temp_resumes"

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(
            upload_folder,
            uploaded_file.name
        )

        with open(file_path, "wb+") as destination:

            for chunk in uploaded_file.chunks():

                destination.write(chunk)

        result = analyze_resume_pipeline(file_path)

        return JsonResponse({
            "success": True,
            "analysis": result
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "error": str(e)
        })