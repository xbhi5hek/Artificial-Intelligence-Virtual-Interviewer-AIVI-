def clean_questions(q_list):
    return [q.strip() for q in q_list if q.strip() != ""]