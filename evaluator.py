from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def evaluate_answers(questions, answers):
    score = 0
    feedback = []

    for q, a in zip(questions, answers):
        documents = [q, a]

        tfidf = TfidfVectorizer().fit_transform(documents)
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

        if similarity > 0.5:
            score += 2
            feedback.append("Good answer")
        elif similarity > 0.2:
            score += 1
            feedback.append("Average answer")
        else:
            feedback.append("Improve this answer")

    return score, feedback