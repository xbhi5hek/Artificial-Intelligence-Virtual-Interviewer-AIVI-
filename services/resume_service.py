import PyPDF2
import os

SKILLS_DB = ["python", "java", "machine learning", "data science", "c", "sql", "react", "flask", "django", "nlp", "aws", "docker"]

def extract_text(path):
    text = ""
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.lower()

def extract_skills(text):
    found = []
    for skill in SKILLS_DB:
        if skill in text:
            found.append(skill)
    return found if found else ["general"]
