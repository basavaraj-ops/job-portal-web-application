from flask import Flask, render_template, request, redirect, url_for, flash , jsonify
import sqlite3
import os
from flask import session
from database import db, Job
from flask_sqlalchemy import SQLAlchemy
# Setup base path and DB path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
DB_PATH = os.path.join(BASE_DIR, 'database.db')
# Flask app setup
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
# Database connection helper
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
# Home route
@app.route('/')
def home():
    return render_template('index.html')
# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        
        

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template('register.html')
        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            flash("Email already registered.")
            conn.close()
            return render_template('register.html')
        conn.execute('''
            INSERT INTO users (first_name, last_name, email, password, confirm_password, role)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (first_name, last_name, email, password, confirm_password, role))
        conn.commit()
        conn.close()
        
        session['role'] = role  # Store role in session for redirection
        if role == 'recruiter':
            return redirect(url_for('post-job.html'))
        
        flash("Registration successful. Please login.")
        return redirect(url_for('login'))
    return render_template('register.html')
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if user:
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            
            flash("Login successful.")
            return redirect(url_for('job'))
        else:
            flash("Invalid email or password.")
            return render_template('login.html')
    return render_template('login.html')
# Job page route
@app.route('/job')
def job():
    # Get user info from session
    first_name = session.get('first_name', 'Guest')
    last_name = session.get('last_name', '')
    user_company = session.get('company')
    user_location = session.get('location')
    user_Categories = session.get('Categories')
    # Get filter values from query parameters (or fallback to session)
    company = request.args.get('company', user_company or '').lower()
    location = request.args.get('location', user_location or '').lower()
    Categories = request.args.get('category', user_Categories or '').lower()
    # Pagination settings
    per_page = 10
    page = request.args.get('page', 1, type=int)
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # Build query dynamically
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    if company:
        query += " AND LOWER(company) LIKE ?"
        params.append(f"%{company}%")
    if location:
        query += " AND LOWER(location) LIKE ?"
        params.append(f"%{location}%")
    if Categories:
        query += " AND LOWER(Categories) LIKE ?"
        params.append(f"%{Categories}%")
    # Add pagination to the query
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, (page-1) * per_page])
    # Execute the query
    c.execute(query, params)
    db_jobs = c.fetchall()
    # Get total count of jobs for pagination
    c.execute("SELECT COUNT(*) FROM jobs WHERE 1=1")
    total_jobs = c.fetchone()[0]
    conn.close()
    # Convert to dictionaries
    jobs = []
    for job in db_jobs:
        jobs.append({
            'id': job['id'],  # Including the ID so you can link to specific job pages
            'title': job['title'],
            'company': job['company'],
            'location': job['location'],
            'Categories': job['Categories'],
            'experience': job['experience'],
            'salary': job['salary'],
            'skills': job['skills']
        })
    # Calculate total pages
    total_pages = (total_jobs // per_page) + (1 if total_jobs % per_page > 0 else 0)
    # Pass filter values and pagination details to the template
    return render_template('job.html', 
                           first_name=first_name, 
                           last_name=last_name, 
                           jobs=jobs,
                           company_filter=company,
                           location_filter=location,
                           Categories_filter=Categories,
                           current_page=page,
                           total_pages=total_pages)
   

   
@app.route('/job-post', methods=['GET', 'POST'])
def job_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')  # Optional
        salary = request.form['salary']
        location = request.form['location']
        company = request.form['company']
        experience = request.form['experience']
        skills = request.form['skills']
        vacancy = request.form['vacancy']
        Categories = request.form['Categories']  # ✅ changed variable name for clarity
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO jobs (title, company, location, experience, vacancy, salary, skills, description, Categories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, company, location, experience, vacancy, salary, skills, description, Categories))
        conn.commit()
        conn.close()
        flash("Job posted successfully", "success")
        return redirect(url_for('job_post'))
    return render_template('job-post.html')
    
   
   
   
   

@app.route('/manage-listings')
def manage_listings():
    employer = {"name": "Test Company"}
    return render_template('manage.html', employer=employer, stats={ 'total_views': 0 })

# Admin login page sever and endpoint
# Dummy credentials for demonstration
ADMIN_USERNAME = "jeeva"
ADMIN_PASSWORD = "6363"
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('manageusers'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('adminlogin'))
           
    
    return render_template('adminlogin.html')

@app.route('/manageusers', methods=['GET'])
def manageusers():
    
    
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id,role,  first_name, last_name, email FROM users")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        users.append({
            'id': row[0],
            'role' : row[1],
            'first_name': row[2],
            'last_name': row[3],
            'email': row[4],
            
        })
    conn.close()
    if not session.get('admin_logged_in'):
        flash("Please log in to access this page.", "error")
        return redirect(url_for('adminlogin'))
    
    
    return render_template('manageusers.html', users=users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    # Example logic
    return f"Edit user page for user ID {user_id}"
@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    # Example logic
    return f"Delete user with ID {user_id}"
@app.route('/toggle_status/<int:user_id>', methods=['GET'])
def toggle_status(user_id):
    # Example logic
    return f"Toggling status for user ID {user_id}"




@app.route('/managejobs', methods=['GET'])
def managejobs():
    if not session.get('admin_logged_in'):
        flash("Please log in to access this page.", "error")
        return redirect(url_for('adminlogin'))
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, experience, vacancy, location, skills, salary, category FROM jobs")
    rows = cursor.fetchall()
    jobs = []
    for row in rows:
        jobs.append({
            'id': row[0],
            'title': row[1],
            'company': row[2],
            'experience': row[3],
            'vacancy': row[4],
            'location': row[5],
            'skills': row[6],
            'salary': row[7],
            
        })
    conn.close()
    return render_template('managejobs.html', jobs=jobs)

@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    # Example logic
    return f"Edit job page for job ID {job_id}"

@app.route('/delete_job/<int:job_id>', methods=['GET'])
def delete_job(job_id):
    # Example logic
    return f"Delete job with ID {job_id}"



@app.route('/apply/<int:job_id>', methods=['GET', 'POST'])
def apply(job_id):
    if request.method == 'POST':
        # Process form data
        fullname = request.form['fullname']
        address = request.form['Address']
        phone = request.form['phone']
        email = request.form['email']
        school = request.form.get('school')  # Degree was mistakenly mapped to school
        degree = request.form.get('degree')  # School/Institution field
        year_completed = request.form.get('year_completed')
        certifications = request.form.get('certifications')  # Added this
        company = request.form.get('company')
        position_held = request.form.get('position_held')
        start_date = request.form.get('start_date')  # Added to replace duplicate employment_dates
        end_date = request.form.get('end_date')  # Added to replace duplicate employment_dates
        skills = request.form.get('skills')
        ref_name = request.form.get('ref_name')
        ref_phone = request.form.get('ref_phone')
        
        
 
      

        # You can now store this data into a DB or process it
        flash('Application submitted successfully!', 'success')
        return redirect(url_for('job'))
    # For GET request: fetch job title based on job_id to show in form
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    if job:
        return render_template('apply.html', job_id=job_id, job_title=job['title'])
    else:
        flash('Job not found.', 'Try again')
        return redirect(url_for('job'))



@app.route('/search')
def search():
    # Get user info from session
    first_name = session.get('first_name', 'Guest')
    last_name = session.get('last_name', '')
    user_company = session.get('company')
    user_location = session.get('location')
    user_Categories = session.get('Categories')
    # Get filter values from query parameters (or fallback to session)
    company = request.args.get('company', user_company or '').lower()
    location = request.args.get('location', user_location or '').lower()
    Categories = request.args.get('Categories', user_Categories or '').lower()
    # Pagination settings
    per_page = 10
    page = request.args.get('page', 1, type=int)
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # Build query dynamically
    base_query = "FROM jobs WHERE 1=1"
    filters = []
    params = []
    if company:
        base_query += " AND LOWER(company) LIKE ?"
        params.append(f"%{company}%")
    if location:
        base_query += " AND LOWER(location) LIKE ?"
        params.append(f"%{location}%")
    if Categories:
        base_query += " AND LOWER(category) LIKE ?"
        params.append(f"%{Categories}%")
    # Count total filtered jobs
    count_query = "SELECT COUNT(*) " + base_query
    c.execute(count_query, params)
    total_jobs = c.fetchone()[0]
    # Add pagination
    search_query = "SELECT * " + base_query + " LIMIT ? OFFSET ?"
    paginated_params = params + [per_page, (page - 1) * per_page]
    
    
    print("Executing query:", search_query)
    c.execute(search_query, paginated_params)
    db_jobs = c.fetchall()
    conn.close()
    
    # Convert jobs to dictionaries
    jobs = []
    for job in db_jobs:
        jobs.append({
            'id': job['id'],
            'title': job['title'],
            'company': job['company'],
            'location': job['location'],
            'Categories': job['Categories'],
            'experience': job['experience'],
            'salary': job['salary'],
            'skills': job['skills']
        })
    # Calculate total pages
    total_pages = (total_jobs // per_page) + (1 if total_jobs % per_page > 0 else 0)
    return render_template('indexsearch.html',
                           first_name=first_name,
                           last_name=last_name,
                           jobs=jobs,
                           company_filter=company,
                           location_filter=location,
                           Categories_filter=Categories,
                           current_page=page,
                           total_pages=total_pages)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    
     

