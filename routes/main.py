from flask import Blueprint, render_template, request, redirect, url_for, current_app, Response, jsonify
from flask_login import login_required, current_user
from models import db, Interview, InterviewQuestion
from resume_parser import extract_text, extract_skills
from question_generator import generate_questions
from services.evaluation_service import evaluate_answers
from services.video_service import video_service
from services.voice_service import voice_service
import os
import time

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.dashboard'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    interviews = Interview.query.filter_by(user_id=current_user.id).order_by(Interview.date.desc()).all()
    
    # Calculate average score (excluding None)
    scored_interviews = [i.score for i in interviews if i.score is not None]
    avg_score = sum(scored_interviews) // len(scored_interviews) if scored_interviews else 0
    
    return render_template('dashboard.html', interviews=interviews, avg_score=avg_score)

@main_bp.route('/video_feed')
@login_required
def video_feed():
    video_service.start()
    return Response(video_service.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@main_bp.route('/live_interview/<int:interview_id>')
@login_required
def live_interview(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    questions = [q.question_text for q in interview.questions]
    return render_template('live_interview.html', interview_id=interview_id, questions=questions)

@main_bp.route('/speak_question', methods=['POST'])
@login_required
def speak_question():
    text = request.json.get('text')
    filename = f"q_{int(time.time())}.mp3"
    audio_path = voice_service.speak(text, filename)
    return jsonify({"audio_url": url_for('static', filename='audio/' + filename)})

@main_bp.route('/listen_answer', methods=['POST'])
@login_required
def listen_answer():
    text = voice_service.listen()
    return jsonify({"text": text})

@main_bp.route('/delete_interview/<int:interview_id>', methods=['POST'])
@login_required
def delete_interview(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    if interview.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
    
    # Delete related questions first
    InterviewQuestion.query.filter_by(interview_id=interview.id).delete()
    db.session.delete(interview)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main_bp.route('/report/<int:interview_id>')
@login_required
def view_report(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    if interview.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
    return render_template('report.html', interview=interview)

@main_bp.route('/start')
@login_required
def start_interview():
    return render_template('index.html')

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'resume' not in request.files:
        return redirect(url_for('main.start_interview'))
    
    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('main.start_interview'))

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    text = extract_text(path)
    skills = extract_skills(text)
    questions = generate_questions(text)
    
    # Create new interview record
    new_interview = Interview(user_id=current_user.id, skills=",".join(skills))
    db.session.add(new_interview)
    db.session.commit()
    
    for q_text in questions:
        q = InterviewQuestion(interview_id=new_interview.id, question_text=q_text)
        db.session.add(q)
    db.session.commit()

    mode = request.form.get('mode', 'text')

    if mode == 'live':
        return render_template("live_interview.html", questions=questions, interview_id=new_interview.id)
    else:
        return render_template("interview.html", questions=questions, interview_id=new_interview.id)


@main_bp.route('/submit/<int:interview_id>', methods=['POST'])
@login_required
def submit(interview_id):
    answers = request.form.getlist('answers')
    interview = Interview.query.get_or_404(interview_id)
    questions = [q.question_text for q in interview.questions]
    
    # Update answers in DB
    for i, q in enumerate(interview.questions):
        if i < len(answers):
            q.answer_text = answers[i]
    
    score, feedback = evaluate_answers(questions, answers)
    
    interview.score = score
    interview.feedback = feedback
    db.session.commit()

    return render_template('result.html', score=score, feedback=feedback)
