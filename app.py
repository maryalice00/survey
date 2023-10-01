from flask import Flask, render_template, request, redirect, flash, session, url_for
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/questions/<int:qid>', methods=['GET', 'POST'])
def question_page(qid):
    if qid != len(session.get('responses', [])):
        flash('You are trying to access an invalid question.')
        return redirect(f'/questions/{len(session["responses"])}')

    if qid >= len(satisfaction_survey.questions):
        return redirect('/thank_you')

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question=question, qid=qid)

@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['choice']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank_you')

    return redirect(f'/questions/{len(responses)}')

@app.route('/thank_you')
def thank_you():
    return render_template('thanks.html')

@app.route('/initialize', methods=['POST'])
def initialize_survey():
    session['responses'] = []
    return redirect('/questions/0')

if __name__ == "__main__":
    app.run(debug=True)
