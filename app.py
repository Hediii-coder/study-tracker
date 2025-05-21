from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

study_sessions = []
next_id = 1

@app.route('/')
def index():
    return render_template('index.html', sessions=study_sessions)

@app.route('/add', methods=['POST'])
def add_session():
    global next_id
    subject = request.form.get('subject')
    minutes = int(request.form.get('minutes', 0))
    if subject and minutes > 0:
        session = {
            'id': next_id,
            'subject': subject,
            'total_seconds': minutes * 60,
            'start_time': int(time.time())  # Store start timestamp
        }
        study_sessions.append(session)
        next_id += 1
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_session(id):
    global study_sessions
    study_sessions = [s for s in study_sessions if s['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
