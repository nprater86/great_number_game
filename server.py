from flask import Flask, render_template, request, redirect, session
import random
app = Flask(__name__)
app.secret_key = 'great_number_game'

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def landing_page():

    number = random.randint(1,100)

    if 'num_guesses' not in session:
        session['num_guesses'] = 5

    if 'number' not in session:
        session['number'] = number

    if 'state' not in session:
        session['state'] = 'first_guess'

    if 'leaderboard' not in session:
        session['leaderboard'] = []

    if 'attempts' not in session:
        session['attempts'] = 0

    print(f"Session number: {session['number']}")
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():

    session['guess'] = request.form['guess']
    print(f"Session guess: {session['guess']}")
    return redirect('/checkWin')

@app.route('/checkWin')
def checkWin():
    if int(session['guess']) == int(session['number']):
        session['attempts'] += 1
        session['state'] = 'win'
    elif int(session['guess']) < int(session['number']):
        session['state'] = 'too_low'
        session['num_guesses'] -= 1
        session['attempts'] += 1
    elif int(session['guess']) > int(session['number']):
        session['state'] = 'too_high'
        session['num_guesses'] -= 1
        session['attempts'] += 1
    if int(session['num_guesses']) == 0:
        session['attempts'] += 1
        session['state'] = 'lose'
    return redirect('/')

@app.route('/add_to_leaderboard', methods=['POST'])
def add_to_leaderboard():
    temp_dict = {}
    temp_dict['name'] = request.form['name']
    temp_dict['attempts'] = session['attempts']
    session['leaderboard'].append(temp_dict)
    session['leaderboard'] = sorted(session['leaderboard'], key = lambda i: i['attempts'])
    return redirect('/leaderboard')

@app.route('/leaderboard')
def display_leaderboard():
    return render_template("leaderboard.html")


@app.route('/reset')
def reset():
    session.pop('num_guesses', None)
    session.pop('number', None)
    session.pop('state', None)
    session.pop('attempts',None)
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)