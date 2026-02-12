from flask import Flask, render_template, request, redirect, url_for, session, flash
from db_config import get_db_connection
from datetime import date

app = Flask(__name__)
app.secret_key = 'cems_secret_key'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/hello')
def hello():
    return "Hello route works"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/test-db')
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    cursor.close()
    conn.close()
    return str(tables)


# ---------------- ADMIN LOGIN ---------------- #

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admin WHERE Email=%s AND Password=%s",
            (email, password)
        )
        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin:
            session['admin_id'] = admin['AdminID']
            session['admin_name'] = admin['User_name']
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid credentials")

    return render_template('admin_login.html')


@app.route('/events')
def events():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT Event_name, Date, Time, Type, Sponsors
        FROM event
    """)
    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('events.html', events=events)


@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM student WHERE Email=%s AND Password=%s",
            (email, password)
        )
        student = cursor.fetchone()

        cursor.close()
        conn.close()

        if student:
            session['student_id'] = student['StudentID']
            session['student_name'] = student['User_name']
            return redirect(url_for('student_dashboard'))
        else:
            flash("Invalid student credentials")

    return render_template('student_login.html')

       


@app.route('/student-dashboard')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Student details
    cursor.execute(
        "SELECT * FROM student WHERE StudentID = %s",
        (session['student_id'],)
    )
    student = cursor.fetchone()

    # Registered events (IMPORTANT: EventID INCLUDED)
    cursor.execute("""
        SELECT e.EventID, e.Event_name, e.Date, e.Time, e.Type
        FROM event e
        JOIN registration r ON e.EventID = r.EventID
        WHERE r.StudentID = %s
    """, (session['student_id'],))

    registered_events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'student_dashboard.html',
        student=student,
        registered_events=registered_events
    )





@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM admin WHERE AdminID = %s",
        (session['admin_id'],)
    )
    admin = cursor.fetchone()

    cursor.execute("""
        SELECT 
            EventID,
            Event_name,
            Date,
            Time,
            Type,
            Sponsors
        FROM event
        WHERE AdminID = %s
    """, (session['admin_id'],))

    admin_events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_dashboard.html',
        admin=admin,
        admin_events=admin_events
    )




@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['date'],
            request.form['time'],
            request.form['type'],
            request.form['sponsor'],
            session['admin_id']
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO event
            (Event_name, Date, Time, Type, Sponsors, AdminID)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, data)

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('admin_dashboard'))

    return render_template('add_event.html')
@app.route('/student-signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'POST':
        username = request.form['username']
        dept = request.form['dept']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO student (User_name, Dept, Email, Password, Phone_Number)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, dept, email, password, phone))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Account created successfully. Please login.")
        return redirect(url_for('student_login'))

    return render_template('student_signup.html')
@app.route('/admin-signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO admin (User_name, Email, Password)
            VALUES (%s, %s, %s)
        """, (username, email, password))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Admin account created. Please login.")
        return redirect(url_for('admin_login'))

    return render_template('admin_signup.html')

@app.route('/student-events')
def student_events():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get all events
    cursor.execute("SELECT * FROM event")
    events = cursor.fetchall()

    # Get registered event IDs for this student
    cursor.execute(
        "SELECT EventID FROM registration WHERE StudentID = %s",
        (session['student_id'],)
    )
    registered_events = cursor.fetchall()
    registered_event_ids = {r['EventID'] for r in registered_events}

    cursor.close()
    conn.close()

    return render_template(
        'student_events.html',
        events=events,
        registered_event_ids=registered_event_ids
    )


@app.route('/register-event/<int:event_id>')
def register_event(event_id):
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Prevent duplicate registration
    cursor.execute("""
        SELECT * FROM registration
        WHERE StudentID = %s AND EventID = %s
    """, (session['student_id'], event_id))

    already_registered = cursor.fetchone()

    if not already_registered:
        cursor.execute("""
            INSERT INTO registration (Reg_date, Payment_status, StudentID, EventID)
            VALUES (%s, %s, %s, %s)
        """, (date.today(), 'Pending', session['student_id'], event_id))
        conn.commit()
        flash("Registered successfully!")

    cursor.close()
    conn.close()

    return redirect(url_for('student_events'))

@app.route('/give-feedback/<int:event_id>', methods=['GET', 'POST'])
def give_feedback(event_id):
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    if request.method == 'POST':
        rating = request.form['rating']
        comments = request.form['comments']

        conn = get_db_connection()
        cursor = conn.cursor()

        #cursor.execute("""
         #   INSERT INTO feedback (Rating, Comments, EventID,StudentID)
          #  VALUES (%s, %s, %s,%s)
        #""", (rating, comments, event_id,student_id)
        student_id = session['student_id']

        query = """
        INSERT INTO feedback (Rating, Comments, EventID, StudentID)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (rating, comments, event_id, student_id))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Feedback submitted!")
        return redirect(url_for('student_dashboard'))

    return render_template('give_feedback.html')
@app.route('/admin-feedback/<int:event_id>')
def admin_feedback(event_id):
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Event info (only admin's event)
    cursor.execute("""
        SELECT EventID, Event_name
        FROM event
        WHERE EventID = %s AND AdminID = %s
    """, (event_id, session['admin_id']))
    event = cursor.fetchone()

    if not event:
        cursor.close()
        conn.close()
        return "Unauthorized or event not found"

    # Feedback list
    cursor.execute("""
        SELECT f.Rating, f.Comments, s.User_name
        FROM feedback f
        JOIN student s ON f.StudentID = s.StudentID
        WHERE f.EventID = %s
    """, (event_id,))
    feedbacks = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'admin_feedback.html',
        event=event,
        feedbacks=feedbacks
    )

if __name__ == '__main__':
    app.run(debug=True)
