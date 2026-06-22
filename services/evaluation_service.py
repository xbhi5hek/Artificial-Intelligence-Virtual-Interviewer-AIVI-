from services.ai_service import evaluate_interview_ai
import json
import re

def evaluate_answers(questions, answers):
    """
    Evaluates interview answers using AI.
    Returns (score, feedback)
    """
    raw_evaluation = evaluate_interview_ai(questions, answers)
    
    # Try to parse JSON from the AI response
    try:
        # Look for JSON block in case AI adds preamble
        json_match = re.search(r'\{.*\}', raw_evaluation, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            score = data.get('score', 50)
            feedback = data.get('feedback', raw_evaluation)
            return score, feedback
    except Exception:
        pass

    # If parsing fails, try to extract a score manually or return 0
    score_match = re.search(r'score[:\s]+(\d+)', raw_evaluation.lower())
    score = int(score_match.group(1)) if score_match else 0
    
    return score, raw_evaluation