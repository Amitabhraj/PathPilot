from django.shortcuts import render, redirect
from django.contrib import messages
from PathPilot.decorators import login_required
import fitz
import ollama
import json
import re


def extract_resume_text(pdf_file):
    text = ""
    try:
        pdf = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in pdf:
            text += page.get_text()
        pdf.close()
    except Exception as e:
        print("PDF Extraction Error:", e)
    return text


def extract_resume_skills_projects(text):

    prompt = f"""
    You are an AI Resume Analyzer.

    Extract ONLY:
    1. Skills
    2. Projects

    From the resume text below.

    Return response ONLY in valid JSON format.

    Format:
    {{
        "skills": ["skill1", "skill2"],
        "projects": [
            {{
                "title": "Project Name",
                "description": "Short Description"
            }}
        ]
    }}

    Resume Text:
    {text}
    """
    try:
        response = ollama.chat(
            model='llama3.2:3b',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        result = response['message']['content']
        result = re.sub(r"```json|```", "", result).strip()
        parsed_json = json.loads(result)

        return parsed_json

    except Exception as e:
        print("Llama Extraction Error:", e)

        return {
            "skills": [],
            "projects": []
        }



@login_required
def upload_resume(request):
    if request.method == 'POST':
        resume = request.FILES.get('current_resume')

        if not resume:
            messages.error(request, "Please select a file.")
            return redirect('userHome')

        extracted_text = extract_resume_text(resume)

        if not extracted_text.strip():
            messages.error(request, "Unable to extract text from PDF.")
            return redirect('userHome')
        
        extracted_skills_projects = extract_resume_skills_projects(extracted_text)

        if not extracted_skills_projects['skills'] and not extracted_skills_projects['projects']:
            messages.error(request, "Unable to extract skills and projects from resume.")
            return redirect('userHome')

        user = request.user
        user.current_resume = resume
        user.resume_raw_text = extracted_text
        user.current_skills_projects = (
                                    json.dumps(extracted_skills_projects['skills']) +
                                    "--------------" +
                                    json.dumps(extracted_skills_projects['projects'])
                                )
        user.save()

        messages.success(request, "Resume uploaded successfully!")
        return redirect('userHome')

    return render(request, 'dashboard/user-home.html')