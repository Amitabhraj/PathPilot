import faiss
import pickle
import numpy as np
import json
import os

from groq import Groq
from dotenv import load_dotenv

from .embedding_model import create_embedding
from .extract_text import extract_resume_text

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(
    BASE_DIR,
    "vector_store",
    "resume_index.faiss"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "vector_store",
    "resume_data.pkl"
)

print("Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

print("Loading resume database...")

with open(DATA_PATH, "rb") as f:

    resumes = pickle.load(f)


def analyze_resume_pipeline(uploaded_resume_path):

    print("Extracting uploaded resume text...")

    extracted_resumes = extract_resume_text(
        os.path.dirname(uploaded_resume_path)
    )

    if len(extracted_resumes) == 0:

        return {
            "error": "Could not extract resume text"
        }

    extracted_resume = extracted_resumes[0]["content"]

    print("Creating embedding...")

    query_embedding = create_embedding(extracted_resume)

    query_embedding = np.array(
        [query_embedding]
    ).astype('float32')

    print("Searching similar resumes...")

    D, I = index.search(query_embedding, k=3)

    retrieved_resumes = []

    for idx in I[0]:

        retrieved_resumes.append(resumes[idx])

    context = ""

    for resume in retrieved_resumes:

        context += f"""

        FILE:
        {resume['filename']}

        RESUME CONTENT:
        {resume['content']}

        """

    prompt = f"""

You are an ATS Resume Analyzer.

Below are resumes of selected candidates from top companies.

{context}

Now analyze this student resume:

{extracted_resume}

Analyze and return ONLY VALID JSON.

Required Format:

{{
    "ATS_score": number,
    "missing_skills": [],
    "missing_projects": [],
    "ats_improvements": [],
    "resume_weaknesses": [],
    "learning_roadmap": [],
    "important_technologies_to_learn": []
}}

"""

    print("Sending request to Groq...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    result = response.choices[0].message.content

    cleaned_result = (
        result
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    print("Parsing JSON response...")

    parsed_json = json.loads(cleaned_result)

    return parsed_json