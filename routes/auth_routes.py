from flask import Blueprint, request, redirect

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    # simple login logic
    return redirect('/')