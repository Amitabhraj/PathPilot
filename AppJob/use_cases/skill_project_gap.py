from django.http import StreamingHttpResponse
from ollama import chat

def analyze_job_stream(request):

    title = request.GET.get("title")
    company = request.GET.get("company")

    def generate():
        response = chat(
            model='llama3.2:3b',
            messages=[
                {
                    'role': 'user',
                    'content': f"""

                You are an expert AI Career Coach and ATS Analyzer.

                Your task is to compare a student's resume with a job description.

                You must:
                1. Identify matching skills
                2. Identify missing skills
                3. Identify missing technologies
                4. Identify missing projects
                5. Suggest EXACT projects student should build
                6. Suggest learning roadmap
                7. Estimate realistic time required
                8. Give ATS match percentage

                IMPORTANT RULES:
                - Keep response concise
                - Be practical
                - Return beautiful readable text
                - No markdown
                - No JSON
                - Make response structured

                STUDENT SKILLS:
                {(request.user.current_skills_projects).split("--------------")[0]}

                STUDENT PROJECTS:
                {(request.user.current_skills_projects).split("--------------")[1]}

                JOB TITLE:
                {title}

                COMPANY:
                {company}

                """
                }
            ],

            options={
                "temperature": 0,
                "num_predict": 4000,
            },

            stream=True
        )

        for chunk in response:
            content = chunk['message']['content']
            yield content

    return StreamingHttpResponse(
        generate(),
        content_type='text/plain'
    )