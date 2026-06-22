import os
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Configure Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(prompt, system_instruction="You are a professional AI interviewer."):
    """
    Get AI response using Gemini as primary and Groq as fallback.
    """
    # Try Gemini first
    try:
        response = gemini_model.generate_content(
            f"{system_instruction}\n\nUser: {prompt}"
        )
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}. Falling back to Groq...")
        
        # Fallback to Groq
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as groq_e:
            return f"Error: Both AI services failed. {groq_e}"

def generate_questions_ai(resume_text):
    prompt = f"Analyze the following resume text and generate 5 VERY BASIC interview questions strictly related to the skills and experience mentioned:\n\n{resume_text}"
    system = """You are a friendly HR interviewer. 
- Ask only BASIC and foundational questions. 
- Do not ask advanced technical or complex architectural questions.
- Every question must be directly related to something mentioned in the resume.
- Return only the questions, one per line. No introduction or numbering."""
    response = get_ai_response(prompt, system)
    # Split by lines and clean up
    questions = [q.strip() for q in response.split('\n') if q.strip()]
    return questions[:7]

def evaluate_interview_ai(questions, answers):
    q_a_pairs = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(questions, answers)])
    prompt = f"Evaluate the following interview responses:\n{q_a_pairs}"
    system = """You are a highly critical Lead Engineer conducting a technical interview. 
Your goal is to identify if the candidate truly knows the subject.
- If an answer is 'I don't know', 'wrong', 'asdf', or irrelevant, score that question as 0.
- Vague or generic answers should receive a maximum of 30/100.
- Only comprehensive, technically accurate answers receive high scores.

REQUIRED RESPONSE FORMAT (JSON ONLY):
{
  "score": <int_0_to_100>,
  "feedback": "<detailed_feedback_string>"
}
Do not include any other text before or after the JSON."""
    
    response = get_ai_response(prompt, system)
    # Try to extract JSON or just return text if it fails
    return response