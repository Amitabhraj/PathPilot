import fitz
import os


def extract_resume_text(folder_path):

    resumes = []

    for filename in os.listdir(folder_path):

        if filename.endswith(".pdf"):

            file_path = os.path.join(
                folder_path,
                filename
            )

            try:

                doc = fitz.open(file_path)

                text = ""

                for page in doc:

                    text += page.get_text()

                resumes.append({
                    "filename": filename,
                    "content": text
                })

            except Exception as e:

                print(f"Error reading {filename}: {e}")

    return resumes