
"""from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="",  # Your MySQL password
    database="db_alumini"
)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Student Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Clear previous session data
        session.clear()

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_stusign WHERE email = %s AND password = %s", (email, password))
        student = cursor.fetchone()

        if student:
            session['student_id'] = student[0]
            session['student_name'] = student[1]
            flash('Student Login Successful!', 'success')
            return redirect(url_for('student'))
        else:
            flash('Incorrect Email or Password for Student', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')"""

"""# Alumni Login Route
@app.route('/loginalu', methods=['GET', 'POST'])
def loginalu():
    if request.method == 'POST':
        # Clear previous session data
        session.clear()

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_alulog WHERE gmail = %s AND password = %s", (email, password))
        alumni = cursor.fetchone()

        if alumni:
            session['alumni_id'] = alumni[0]
            session['alumni_name'] = alumni[1]
            flash('Alumni Login Successful!', 'success')
            return redirect(url_for('jobpost'))  # Redirect to job post page after successful alumni login
        else:
            flash('Incorrect Email or Password for Alumni', 'danger')
            return redirect(url_for('loginalu'))

    return render_template('loginalu.html')"""
"""@app.route('/loginalu', methods=['GET', 'POST'])
def loginalu():
    if request.method == 'POST':
        # Clear previous session data
        session.clear()

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_alulog WHERE gmail = %s AND password = %s", (email, password))
        alumni = cursor.fetchone()

        if alumni:
            session['alumni_id'] = alumni[0]  # Assuming the first column is the ID
            session['alumni_name'] = alumni[1]  # Assuming the second column is the name
            flash('Alumni Login Successful!', 'success')
            return redirect(url_for('alulog'))  # Redirect to alulog page after successful alumni login
        else:
            flash('Incorrect Email or Password for Alumni', 'danger')
            return redirect(url_for('loginalu'))

    return render_template('loginalu.html')
@app.route('/alulog')
def alulog():
    # Check if the user is logged in
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    alumni_name = session.get('alumni_name')  # Get the alumni name from the session

    return render_template('alulog.html', alumni_name=alumni_name)


@app.route('/jobpost')
def jobpost():
    # Check if the user is logged in
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    return render_template('jobpost.html')  # Ensure this points to your jobpost.html template

# Student Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        col_code = request.form['collegeCode']
        reg_no = request.form['regNo']
        pass_out = request.form['passedOutYear']

        cursor = db.cursor()
        # Check if the email already exists
        cursor.execute("SELECT * FROM tb_stusign WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered. Please use a different email.', 'warning')
            return redirect(url_for('signup'))
        
        # Insert the new user into the database
        cursor.execute("INSERT INTO tb_stusign (name, email, password, col_code, Reg_no, pass_our) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, email, password, col_code, reg_no, pass_out))
        db.commit()
        flash('Sign up successful! You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Student Page Route
@app.route('/student')
def student():
    if 'student_id' in session:
        return render_template('student.html', name=session['student_name'])
    else:
        flash('Please login as a student to access the student page.', 'warning')
        return redirect(url_for('login'))

# Alumni Page Route
@app.route('/alumini')
def alumini():
    if 'alumni_id' in session:
        return render_template('alumini.html', name=session['alumni_name'])
    else:
        flash('Please login as alumni to access the alumni page.', 'warning')
        return redirect(url_for('loginalu'))

# Alumni Dashboard Route
@app.route('/alumni_dashboard')
def alumni_dashboard():
    if 'alumni_id' in session:
        return render_template('alumni_dashboard.html', name=session['alumni_name'])
    else:
        flash('Please login as alumni to access the alumni dashboard.', 'warning')
        return redirect(url_for('loginalu'))

# Logout Route for both Student and Alumni
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

from datetime import datetime, timedelta
import os
import mysql.connector
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, send
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Your MySQL username
    password="",  # Your MySQL password
    database="db_alumini"
)

# Configure the folder for image uploads
app.config['UPLOAD_FOLDER'] = 'uploadimg'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home Route
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/alumini')
def alumini():
    if 'alumni_id' in session:
        return render_template('alumini.html', name=session['alumni_name'])
    else:
        flash('Please login as alumni to access the alumni page.', 'warning')
        return redirect(url_for('loginalu'))

# Student Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_stusign WHERE email = %s AND password = %s", (email, password))
        student = cursor.fetchone()

        if student:
            session['student_id'] = student[0]
            session['student_name'] = student[1]
            flash('Student Login Successful!', 'success')
            return redirect(url_for('stulog'))
        else:
            flash('Incorrect Email or Password for Student', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Alumni Login Route
@app.route('/loginalu', methods=['GET', 'POST'])
def loginalu():
    if request.method == 'POST':
        session.clear()

        email = request.form['email']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_alulog WHERE gmail = %s AND password = %s", (email, password))
        alumni = cursor.fetchone()

        if alumni:
            session['alumni_id'] = alumni[0]  # Assuming the first column is the ID
            session['alumni_name'] = alumni[1] 
            session['gmail'] = email  # Assuming the second column is the name
            flash('Alumni Login Successful!', 'success')
            return redirect(url_for('alulog'))  # Redirect to alulog page after successful alumni login
        else:
            flash('Incorrect Email or Password for Alumni', 'danger')
            return redirect(url_for('loginalu'))

    return render_template('loginalu.html')
@app.route('/jobpost')
def jobpost():
    # Check if the user is logged in
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    return render_template('jobpost.html')  # Ensure this points to your jobpost.html template


@app.route('/alulog')
def alulog():
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    alumni_name = session.get('alumni_name')
    #alumni_email = request.form['email']  # Example to retrieve email from a form
    # Assuming login is successful
    #session['gmail'] = alumni_email
    

    return render_template('alulog.html', alumni_name=alumni_name)

# Alumni Post Upload Route
"""@app.route('/upload_post', methods=['POST'])
def upload_post():
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    if request.method == 'POST':
        # Get form data
        alumni_name = request.form['alumni_name']
        job_title = request.form['job_title']
        description = request.form['description']

        # Check if a file was uploaded
        if 'photo' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['photo']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Insert data into the database
            cursor = db.cursor()
           sql = INSERT INTO tb_aluupload (name, jobtitle, uploadimg, description)
                     VALUES (%s, %s, %s, %s)
            cursor.execute(sql, (alumni_name, job_title, filename, description))
            db.commit()

            flash('Post uploaded successfully!')
            return redirect(url_for('alulog'))

    return render_template('jobpost.html')  # Make sure your template is in templates folder"""
@app.route('/upload_post', methods=['POST'])
def upload_post():
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    if request.method == 'POST':
        # Get form data
        alumni_name = request.form['alumni_name']
        alumni_email = request.form['alumni_email']  # Added email
        job_title = request.form['job_title']
        post_date = request.form['post_date']  # Added date
        description = request.form['description']

        # Check if a file was uploaded
        if 'photo' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['photo']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Create upload folder if it doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Insert data into the database, including email and date
            cursor = db.cursor()
            sql = """INSERT INTO tb_aluupload (name, email, jobtitle, date, uploadimg, description)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (alumni_name, alumni_email, job_title, post_date, filename, description))
            db.commit()

            flash('Post uploaded successfully!', 'success')
            return redirect(url_for('alulog'))

    return render_template('jobpost.html')

# Student Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        col_code = request.form['collegeCode']
        reg_no = request.form['regNo']
        pass_out = request.form['passedOutYear']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM tb_stusign WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already registered.', 'warning')
            return redirect(url_for('signup'))

        cursor.execute("INSERT INTO tb_stusign (name, email, password, col_code, Reg_no, pass_our) VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, email, password, col_code, reg_no, pass_out))
        db.commit()
        flash('Sign up successful! You can now login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Student Page Route
"""@app.route('/student')
def student():
    if 'student_id' in session:
        return render_template('student.html', name=session['student_name'])
    else:
        flash('Please login as a student.', 'warning')
        return redirect(url_for('login'))"""
@app.route('/student')
def student():
    # Render student page without checking login status
    return render_template('student.html')
# View Uploaded Posts Route
 # Pass uploads to the template
"""@app.route('/view_uploads')
def view_uploads():
    # Check if the user is logged in
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    cursor = db.cursor()
    cursor.execute("SELECT * FROM tb_aluupload")  # Fetch all uploaded posts
    #cursor.execute("SELECT * FROM tb_aluupload WHERE email = %s", (alumni_email,))
    uploads = cursor.fetchall()  # Get all the results

    return render_template('view_uploads.html', uploads=uploads) """

@app.route('/view_uploads')
def view_uploads():
    # Check if the user is logged in
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))

    # Retrieve the email of the logged-in alumni from the session
    alumni_email = session.get('gmail')  # Retrieve the email stored in the session

    cursor = db.cursor()
    try:
        # Fetch only the uploads for the logged-in alumni
        cursor.execute("SELECT * FROM tb_aluupload WHERE email = %s", (alumni_email,))  # Filter by email
        uploads = cursor.fetchall()  # Get the results
    except Exception as e:
        flash('An error occurred while fetching uploads: ' + str(e), 'danger')
        uploads = []  # Ensure uploads is empty on error
    finally:
        cursor.close()  # Close cursor

    return render_template('view_uploads.html', uploads=uploads)

@app.route('/uploadimg/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploadimg', filename)

@app.route('/delete_post/<int:post_id>/<image>', methods=['POST'])
def delete_post(post_id, image):
    try:
        # Use the global 'db' connection instead of a new one
        cursor = db.cursor()

        # Delete post from database
        cursor.execute("DELETE FROM tb_aluupload WHERE id = %s", (post_id,))
        db.commit()
        cursor.close()

        # Remove image from the filesystem
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
        if os.path.exists(image_path):
            os.remove(image_path)
            flash('Post and image deleted successfully!', 'success')
        else:
            flash('Post deleted, but image file not found.', 'warning')

    except Exception as e:
        flash(f'An error occurred: {e}', 'danger')

    return redirect(url_for('view_uploads'))

# Alumni Dashboard Route
@app.route('/alumni_dashboard')
def alumni_dashboard():
    if 'alumni_id' in session:
        return render_template('alumni_dashboard.html', name=session['alumni_name'])
    else:
        flash('Please login as alumni.', 'warning')
        return redirect(url_for('loginalu'))
@app.route('/stulog')
def stulog():
    if 'student_id' in session:
        return render_template('stulog.html', name=session['student_name'])
    else:
        flash('Please login as a student.', 'warning')
        return redirect(url_for('login'))
@app.route('/recpost')
def recpost():
    cursor = db.cursor()  # Assuming `db` is your database connection object
    query = "SELECT name, jobtitle, date, uploadimg, description FROM tb_aluupload"
    cursor.execute(query)
    posts = cursor.fetchall()  # Fetch all the results from the table
    return render_template('recpost.html', posts=posts)

@app.route('/logout')
def logout():
    # Clear the session or any login-related data
    session.clear()  # This clears all session data
    # Redirect to the index page
    return redirect(url_for('index'))
"""@app.route('/chat')
def chat():
    if 'alumni_id' not in session:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('loginalu'))
    
    return render_template('chat.html')  # Make sure this template exists
@app.route('/chat')
def chat():
    if 'alumni_id' in session:
        user_type = 'alumni'
    elif 'student_id' in session:
        user_type = 'student'
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))  # or any appropriate page

    return render_template('chat.html', user_type=user_type)"""

"""
@app.route('/chat')
def chat():
    if 'alumni_id' in session:
        user_type = 'alumni'
    elif 'student_id' in session:
        user_type = 'student'
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    # Fetch chat history from the database
    cursor = db.cursor()
    cursor.execute("SELECT user_type, message, timestamp FROM tb_chats ORDER BY timestamp ASC")
    chat_history = cursor.fetchall()  # Retrieve all messages

    return render_template('chat.html', user_type=user_type, chat_history=chat_history)

socketio = SocketIO(app)



@socketio.on('send_message')
def handle_message(data):
    user_type = data['user_type']
    message = data['message']
    
    # Insert the message into the database
    cursor = db.cursor()
    cursor.execute("INSERT INTO tb_chats (user_type, message) VALUES (%s, %s)", (user_type, message))
    db.commit()

    # Retrieve the timestamp of the inserted message
    cursor.execute("SELECT timestamp FROM tb_chats WHERE user_type=%s AND message=%s ORDER BY timestamp DESC LIMIT 1", (user_type, message))
    timestamp = cursor.fetchone()[0]
    
    # Format date and time
    formatted_date = timestamp.strftime("%B %d, %Y")
    formatted_time = timestamp.strftime("%I:%M %p")  # 12-hour format with AM/PM

    # Emit the message back to all connected clients with the formatted timestamp
    emit('receive_message', {
        'user_type': user_type,
        'message': message,
        'date': formatted_date,
        'time': formatted_time
    }, broadcast=True)


"""


@app.route('/chat')
def chat():
    if 'alumni_id' in session:
        user_type = 'alumni'
        user_name = session.get('alumni_name')  # Fetch the name of the logged-in alumni
    elif 'student_id' in session:
        user_type = 'student'
        user_name = session.get('student_name')  # Fetch the name of the logged-in student
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

    # Fetch chat history from the database
    cursor = db.cursor()
    cursor.execute("SELECT user_type, message, username, timestamp FROM tb_chats ORDER BY timestamp ASC")
    chat_history = cursor.fetchall()  # Retrieve all messages

    return render_template('chat.html', user_type=user_type, chat_history=chat_history, user_name=user_name)

socketio = SocketIO(app)

@socketio.on('send_message')
def handle_message(data):
    user_type = data['user_type']
    message = data['message']
    username = data['username']
    
    # Insert the message into the database with the username
    cursor = db.cursor()
    cursor.execute("INSERT INTO tb_chats (user_type, message, username) VALUES (%s, %s, %s)", (user_type, message, username))
    db.commit()

    # Retrieve the timestamp of the inserted message
    cursor.execute("SELECT timestamp FROM tb_chats WHERE user_type=%s AND message=%s AND username=%s ORDER BY timestamp DESC LIMIT 1", (user_type, message, username))
    timestamp = cursor.fetchone()[0]
    
    # Format date and time
    formatted_date = timestamp.strftime("%B %d, %Y")
    formatted_time = timestamp.strftime("%I:%M %p")  # 12-hour format with AM/PM

    # Emit the message back to all connected clients with the formatted timestamp and username
    emit('receive_message', {
        'user_type': user_type,
        'username': username,
        'message': message,
        'date': formatted_date,
        'time': formatted_time
    }, broadcast=True)

@app.route('/request', methods=['GET', 'POST'])
def request_form():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        col_code = request.form.get('col_code')
        reg_no = request.form.get('reg_no')
        current_job = request.form.get('current_job')
        pass_out = request.form.get('pass_out')

        # Check if passwords match
        if password != re_password:
            flash("Passwords do not match!", "error")
            return render_template('request.html')  # Re-render the same page without redirecting

        # Insert data into the database
        try:
            cursor = db.cursor()
            insert_query = """
                INSERT INTO tb_reqalu (name, gmail, password, re_pass, col_cod, reg, curjob, passedout_year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (name, gmail, password, re_password, col_code, reg_no, current_job, pass_out))
            db.commit()
            flash("Form submitted successfully!", "success")
        except mysql.connector.Error as err:
            flash(f"Database error: {err}", "error")
        finally:
            cursor.close()

        return render_template('index.html')  # Show success message without redirecting
    
    return render_template('request.html')




def create_chat_table():
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_chats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_type VARCHAR(10),  -- 'Alumni' or 'Student'
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()
    cursor.close()

# Call the create table function
create_chat_table()



if __name__ == '__main__':
    app.run(debug=True)
