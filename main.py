from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret123"

# ================= DUMMY DATA =================

EVENTS = [
    {
        "id": 1,
        "name": "Coding Contest",
        "date": "2026-02-10",
        "venue": "Main Hall",
        "category": "Technical",
        "fee": 50
    },
    {
        "id": 2,
        "name": "Poster Presentation",
        "date": "2026-02-12",
        "venue": "Seminar Hall",
        "category": "Non-Technical",
        "fee": 30
    }
]

USERS = []          # user accounts
PARTICIPANTS = []  # event registrations
ADMIN = {
    "username": "admin",
    "password": "admin123"
}

# ================= HELPERS =================

def login_required_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash("Please login first", "warning")
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

def login_required_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'admin' not in session:
            flash("Admin login required", "warning")
            return redirect(url_for('admin_login'))
        return fn(*args, **kwargs)
    return wrapper

# ================= PUBLIC =================

@app.route('/')
def home():
    return render_template('home.html', events_list=EVENTS)

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contactus.html')

# ================= USER AUTH =================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        USERS.append({
            "name": request.form['name'],
            "email": request.form['email'],
            "username": request.form['username'],
            "password": request.form['password']
        })
        flash("Registration successful!", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        for u in USERS:
            if u['username'] == request.form['username'] and u['password'] == request.form['password']:
                session['user'] = u
                return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('user-login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

# ================= USER DASHBOARD =================

@app.route('/dashboard')
@login_required_user
def dashboard():
    return render_template('user-dashboard.html', user=session['user'], events=EVENTS)

@app.route('/event-registration', methods=['GET', 'POST'])
@login_required_user
def event_registration():
    if request.method == 'POST':
        PARTICIPANTS.append({
            "name": session['user']['name'],
            "email": session['user']['email'],
            "phone": request.form['phone'],
            "events": request.form.getlist('events'),
            "payment": request.form['payment']
        })
        flash("Event registered successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('event_registration.html', events=EVENTS)

@app.route('/my-events')
@login_required_user
def my_events():
    user_email = session['user']['email']
    my_list = [p for p in PARTICIPANTS if p['email'] == user_email]
    return render_template('my_events.html', events=my_list)

# ================= ADMIN =================

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN['username'] and request.form['password'] == ADMIN['password']:
            session['admin'] = ADMIN['username']
            return redirect(url_for('admin_dashboard'))
        flash("Invalid admin login", "danger")
    return render_template('admin-login.html')

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin-dashboard')
@login_required_admin
def admin_dashboard():
    return render_template('admin-dashboard.html')

@app.route('/manage-events')
@login_required_admin
def manage_events():
    return render_template('events-management.html', events=EVENTS)

@app.route('/participants')
@login_required_admin
def participants():
    return render_template('participants.html', participants=PARTICIPANTS)

# ================= RUN =================

if __name__ == '__main__':
    app.run(host='0.0.0',debug=True)
