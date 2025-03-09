from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from ultralytics import YOLO
import cv2
import os
import re




app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root@123'
app.config['MYSQL_DB'] = 'project'
app.secret_key = 'hellothere'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and all(key in request.form for key in ('username', 'name', 'password', 'email', 'address', 'phone')):
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not all(request.form[key] for key in ('username', 'name', 'password', 'email', 'address', 'phone')):
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            cursor.execute('INSERT INTO details VALUES(%s,%s, %s, %s, %s)', (username, name, email, address, phone,))

            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/Login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return redirect('/main')
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)

@app.route('/main')
def mainpage():
    return render_template('index.html')




@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        username = session['username']
        cursor = mysql.connection.cursor()

        # Fetch user details from 'details' table
        cursor.execute("SELECT * FROM details WHERE username = %s", (username,))
        userdetails = cursor.fetchall()

        # Fetch donation details from 'donations' table
        cursor.execute("SELECT * FROM donation WHERE username = %s", (username,))
        donationdetails = cursor.fetchall()

        cursor.close()
        return render_template('profile.html', userdetails=userdetails, donationdetails=donationdetails)
    
    else:
        return redirect('/login')



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

model = YOLO('best.pt')  # Initialize the YOLO model outside of the route handlers

@app.route('/clothes')
def clothes():
    return render_template('clothes.html')

@app.route('/fabric_defect_detection')
def fabric_defect_detection():
    return render_template('upload.html')

@app.route('/clothesform', methods=['GET', 'POST'])
def clothesform():
    if request.method == 'POST':
        username = session.get('username')
        date = request.form['date']
        time = request.form['time']
        donation_type = request.form['donation_type']
        num_clothes = request.form['num_clothes']

        cur = mysql.connection.cursor()
        try:
            # Insert data into 'donation' table
            cur.execute("INSERT INTO donation (username, date, time, donation_type) VALUES (%s, %s, %s, %s)",
                        (username, date, time, donation_type))

            # Insert data into 'donation_clothes' table
            cur.execute("INSERT INTO donation_clothes (username, number_of_clothes) VALUES (%s, %s)",
                        (username, num_clothes))

            mysql.connection.commit()  # Commit the transaction
            cur.close()
            flash('Donation recorded successfully!', 'success')
            return redirect("/main")
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of error
            cur.close()
            flash('An error occurred while recording the donation: ' + str(e), 'error')
    return render_template('clothesform.html')



@app.route('/blood', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        username = session.get('username')  # Use session.get() to avoid KeyError if 'username' is not set
        date = request.form['date']
        time = request.form['time']
        donation_type = request.form['donation_type']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO donation (username, date, time, donation_type) VALUES (%s, %s, %s, %s)", (username, date, time, donation_type))
        mysql.connection.commit()
        cur.close()
        return redirect('/main')
    return render_template('index2.html')





@app.route('/books', methods=['GET', 'POST'])
def donation():
    if request.method == 'POST':
        username = session.get('username')
        date = request.form['date']
        time = request.form['time']
        donation_type = request.form['donation_type']
        num_books = request.form['num_books']

        cur = mysql.connection.cursor()
        try:
            # Insert data into 'donation' table
            cur.execute("INSERT INTO donation (username, date, time, donation_type) VALUES (%s, %s, %s, %s)",
                        (username, date, time, donation_type))

            # Insert data into 'donation_books' table
            cur.execute("INSERT INTO donation_books (username, number_of_books) VALUES (%s, %s)",
                        (username, num_books))

            mysql.connection.commit()  # Commit the transaction
            cur.close()
            flash('Donation recorded successfully!', 'success')
            return redirect("/main")
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of error
            cur.close()
            flash('An error occurred while recording the donation: ' + str(e), 'error')
    return render_template('book.html')
    

@app.route('/money', methods=['GET', 'POST'])
def money():
    if request.method == 'POST':
        username = session.get('username')
        date = request.form['date']
        time = request.form['time']
        donation_type = request.form['donation_type']
        amount = request.form['amount']

        cur = mysql.connection.cursor()
        try:
            # Insert data into 'donation' table
            cur.execute("INSERT INTO donation (username, date, time, donation_type) VALUES (%s, %s, %s, %s)",
                        (username, date, time, donation_type))

            # Insert data into 'donation_books' table
            cur.execute("INSERT INTO donation_money (username, amount) VALUES (%s, %s)",
                        (username, amount))

            mysql.connection.commit()  # Commit the transaction
            cur.close()
            flash('Donation recorded successfully!', 'success')
            return redirect("/main")
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of error
            cur.close()
            flash('An error occurred while recording the donation: ' + str(e), 'error')
    return render_template('money.html')


@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    if request.method == 'POST':
        username = session.get('username')
        date = request.form['date']
        time = request.form['time']
        donation_type = request.form['donation_type']
        volunteer_type = request.form['volunteer_type']

        cur = mysql.connection.cursor()
        try:
            # Insert data into 'donation' table
            cur.execute("INSERT INTO donation (username, date, time, donation_type) VALUES (%s, %s, %s, %s)",
                        (username, date, time, donation_type))

            # Insert data into 'donation_books' table
            cur.execute("INSERT INTO volunteer_type (username, volunteer_type) VALUES (%s, %s)",
                        (username, volunteer_type))

            mysql.connection.commit()  # Commit the transaction
            cur.close()
            flash('Donation recorded successfully!', 'success')
            return redirect("/main")
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of error
            cur.close()
            flash('An error occurred while recording the donation: ' + str(e), 'error')
    return render_template('volunteer.html')




def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Function to detect fabric defects and determine if any defects are detected
        def detect_fabric_defects(image_path):
            # Read the input image
            image = cv2.imread(image_path)
            if image is None:
                raise FileNotFoundError(f"Image not found: {image_path}")

            # Perform detection with the YOLO model
            results = model.predict(image)  # Apply the model to the image

            # Check if any defects are detected (i.e., if there are any bounding boxes)
            defects_detected = any(results[0].boxes)  # True if there's at least one bounding box

            return defects_detected

        # Detect defects
        defects = detect_fabric_defects(file_path)

        # Print the result
        if defects:
            print("Defects detected.")
            return render_template('defect.html')
        else:
            print("No defects detected.")
            return render_template('nodefect.html')

    return 'File uploaded successfully'



if __name__ == '__main__':
    app.run(debug=True)
