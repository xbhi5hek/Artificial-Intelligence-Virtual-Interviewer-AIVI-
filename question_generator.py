from services.ai_service import generate_questions_ai

def generate_questions(resume_text):
    # Use the AI service to generate dynamic questions
    ai_questions = generate_questions_ai(resume_text)
    
    # Always include some general ones if AI fails or returns too few
    if len(ai_questions) < 3:
        ai_questions.extend(["Tell me about yourself.", "Why should we hire you?"])
    
    return ai_questions