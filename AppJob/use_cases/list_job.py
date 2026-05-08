from jobspy import scrape_jobs
import logging
from django.contrib import messages
from PathPilot.decorators import login_required
from django.shortcuts import render
import ollama
import json
import re

logger = logging.getLogger(__name__)


# =====================================================
# 🤖 Generate Job Roles using AI
# =====================================================
def generate_job_roles(skills_projects_text):

    prompt = f"""
    You are an AI Career Assistant.

    Based on the user's skills and projects,
    suggest ONLY 5 most suitable job roles.

    Return ONLY valid JSON.

    Format:
    {{
        "job_roles": []
    }}

    User Resume Skills & Projects:
    {skills_projects_text}
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

        print("\n========== RAW OLLAMA RESPONSE ==========")
        print(result)
        print("=========================================\n")

        # Remove markdown code block
        result = re.sub(r"```json|```", "", result).strip()

        # Extract JSON safely
        json_match = re.search(r'\{.*\}', result, re.DOTALL)

        if not json_match:

            logger.error("No valid JSON found in response")

            return []

        clean_json = json_match.group()

        parsed_json = json.loads(clean_json)

        job_roles = parsed_json.get("job_roles", [])

        # Ensure list
        if not isinstance(job_roles, list):
            logger.error("job_roles is not a list")
            return []

        # Remove empty values
        job_roles = [
            role.strip()
            for role in job_roles
            if role.strip()
        ]

        return job_roles[:5]

    except Exception as e:

        logger.error(f"Job Role Extraction Error: {e}")

        return []





def fetch_jobs(request, search, location):

    user = request.user

    skills_projects_text = user.current_skills_projects

    # Resume check
    if not skills_projects_text:
        messages.error(
            request,
            "Please upload your resume first."
        )
        return []

    # Generate AI roles
    search_jobs = generate_job_roles(
        skills_projects_text
    )

    all_jobs = []
    try:

        for role in search_jobs:
            jobs_df = scrape_jobs(
                site_name=["linkedin"],
                search_term=role,
                location=location,
                results_wanted=5,
                hours_old=72,
                country_relevant="india",
            )

            # Skip empty dataframe
            if jobs_df.empty:
                print(f"No jobs found for {role}")
                continue

            for _, row in jobs_df.iterrows():
                all_jobs.append({
                    "search_role": role,
                    "title": row.get("title"),
                    "company": row.get("company"),
                    "location": row.get("location"),
                    "job_url": row.get("job_url"),
                    "description": row.get("description"),
                    "salary": row.get("salary"),
                    "date_posted": row.get("date_posted"),
                })

        print(f"\nTOTAL JOBS FETCHED: {len(all_jobs)}")

        return all_jobs

    except Exception as e:

        logger.error(f"Job fetch failed: {e}")

        messages.error(
            request,
            "Unable to fetch jobs currently."
        )

        return []


# =====================================================
# 📄 Job Listing View
# =====================================================
@login_required
def job_list(request):

    search = request.GET.get(
        "search",
        "Software Engineer"
    )

    location = request.GET.get(
        "location",
        "India"
    )

    jobs = fetch_jobs(
        request,
        search,
        location
    )

    context = {
        "jobs": jobs,
        "search": search,
        "location": location,
    }

    return render(
        request,
        "job/job_listing.html",
        context
    )