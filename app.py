from flask import Flask, render_template, request, redirect, url_for
import time
from datetime import datetime, timedelta
import uuid  # For unique session IDs

app = Flask(__name__)

study_sessions = []

@app.route('/')
def index():
    now = datetime.now()
    today_total = 0
    week_sessions = 0

    for s in study_sessions:
        created = datetime.fromisoformat(s['created_at'])
        minutes = s['total_seconds'] // 60

        if created.date() == now.date():
            today_total += minutes

        if now - created <= timedelta(days=7):
            week_sessions += 1

    return render_template('index.html', sessions=study_sessions,
                           today_total=today_total, week_sessions=week_sessions)

@app.route('/add', methods=['POST'])
def add_session():
    subject = request.form.get('subject')
    minutes = int(request.form.get('minutes', 0))
    if subject and minutes > 0:
        session = {
            'id': str(uuid.uuid4()),  # Use UUID for unique IDs
            'subject': subject,
            'total_seconds': minutes * 60,
            'start_time': int(time.time()),  # Store start timestamp
            'created_at': datetime.now().isoformat()
        }
        study_sessions.append(session)
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete_session(id):
    global study_sessions
    study_sessions = [s for s in study_sessions if s['id'] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

