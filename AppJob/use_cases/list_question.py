from django.http import StreamingHttpResponse
from ollama import chat

from AppJob.models import Questions

def analyze_question_stream(request):

    title = request.GET.get("title")
    company = request.GET.get("company")

    def generate():
        dsa_questions = Questions.objects.all().filter(type="DSA").values("title", "url")
        data = list(dsa_questions)

        response = chat(
            model='llama3.2:3b',
            messages=[
                {
                    'role': 'user',
                    'content': f"""

                    You are an expert technical interviewer.

                    Select ONLY the BEST 10 DSA questions relevant for this role.

                    Job Title:
                    {title}

                    Company:
                    {company}

                    Available Questions:
                    {data}

                    STRICT RULES:
                    1. Output ONLY 10 questions
                    2. Start with:
                    Here are the top 10 DSA questions

                    3. Use numbering format
                    4. Each question must contain clickable URL
                    5. Do NOT write explanations
                    6. Do NOT write introductions
                    7. Do NOT write conclusions
                    8. Format exactly like:

                    1. Two Sum
                    https://leetcode.com/abc

                    2. Binary Tree Level Order Traversal
                    https://leetcode.com/xyz

                    """
                }
            ],

            options={
                "temperature": 0,
                "num_predict": 1000,
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
