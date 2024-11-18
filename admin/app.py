# admin/app.py

"""from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory

from datetime import datetime, timedelta
import os
import mysql.connector
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, send
from flask_socketio import SocketIO, emit
app = Flask(__name__)
# Route to render the login page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key for session management

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # No password as per your setup
    'database': 'db_alumini'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM tb_adminlog WHERE gmail = %s AND password = %s"
        cursor.execute(query, (email, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if admin:
            # Set session variables or any other way to maintain login state
            session['admin_logged_in'] = True
            session['admin_name'] = admin['name']
            return redirect(url_for('adminhome'))
        else:
            return "Invalid credentials, please try again.", 401

    return render_template('login.html')

@app.route('/adminhome')
def adminhome():
    # Check if the admin is logged in
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    return render_template('adminhome.html')
@app.route('/view_alumni')
def view_alumni():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_alulog")
    alumni = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_alumni.html', alumni=alumni)

@app.route('/delete_alumni/<int:id>', methods=['POST'])
def delete_alumni(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_alulog WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view_alumni'))
"""@app.route('/add_alumni', methods=['GET', 'POST'])
def add_alumni():
    if request.method == 'POST':
        name = request.form.get('name')
        gmail = request.form.get('gmail')
        password = request.form.get('password')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO tb_alulog (name, gmail, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, gmail, password))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('add_alumni'))  # Redirect to the view alumni page after adding

    return render_template('add_alumni.html')
    """
@app.route('/view_student')
def view_student():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, password, col_code, Reg_no, pass_our FROM tb_stusign")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_student.html', students=students)
@app.route('/view_jobpost')
def view_jobpost():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, jobtitle, date, uploadimg, description FROM tb_aluupload")
    jobposts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_jobpost.html', jobposts=jobposts)
@app.route('/delete_jobpost/<int:id>', methods=['POST'])
def delete_jobpost(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tb_aluupload WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('view_jobpost'))
@app.route('/view_chat')
def view_chat():
    return render_template('view_chat.html')

@app.route('/api/chat-messages', methods=['GET'])
def get_chat_messages():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_chats")
    messages = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(messages)

@app.route('/api/delete-message/<int:id>', methods=['DELETE'])
def delete_message(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tb_chats WHERE id = %s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return '', 204
@app.route('/adminhome')
def admin_home():
    return render_template('adminhome.html')
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))






@app.route('/add_alumni')
def add_alumni():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, gmail, col_cod, reg, curjob, passedout_year FROM tb_reqalu")
    requests = cursor.fetchall()
    db.close()
    return render_template('add_alumni.html', requests=requests)

# Route to accept a request
@app.route('/accept_request/<int:req_id>', methods=['POST'])
def accept_request(req_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Fetch the request data
    cursor.execute("SELECT name, gmail, password FROM tb_reqalu WHERE id = %s", (req_id,))
    request_data = cursor.fetchone()
    
    if request_data:
        # Insert into tb_alulog
        cursor.execute(
            "INSERT INTO tb_alulog (name, gmail, password) VALUES (%s, %s, %s)",
            (request_data['name'], request_data['gmail'], request_data['password'])
        )
        
        # Delete the row from tb_reqalu
        cursor.execute("DELETE FROM tb_reqalu WHERE id = %s", (req_id,))
        db.commit()
        flash("Request accepted and added to alumni log.", "success")
    else:
        flash("Request not found.", "error")

    db.close()
    return redirect(url_for('add_alumni'))

# Route to reject a request
@app.route('/reject_request/<int:req_id>', methods=['POST'])
def reject_request(req_id):
    db = get_db_connection()
    cursor = db.cursor()
    
    # Delete the row from tb_reqalu
    cursor.execute("DELETE FROM tb_reqalu WHERE id = %s", (req_id,))
    db.commit()
    flash("Request rejected and removed from requests list.", "info")
    
    db.close()
    return redirect(url_for('add_alumni'))
if __name__ == '__main__':
    app.run(debug=True)
