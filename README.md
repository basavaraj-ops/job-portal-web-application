
# 💼 Job Portal Web Application

A dynamic Job Portal Web Application built with Flask and SQLite that connects job seekers with employers.
1. Users can register
2. log in and Register
3. search based on Filters and apply for jobs
4. while Recuriter can post jobs
5. The admin panel(Dashboard) manages both users and job posts and also edit and Delete the users and jobs
6.  Resume upload feature 
7. The user can apply for the job

## 📁 Project Structure

FRONTEND/
│
├── backend/
│   ├── __pycache__/
│   ├── app.py              # Main Flask app
│   ├── database.db         # SQLite database
│   └── database.py         # Database helper functions
│
├── static/
│   ├── images/             # Image assets
│   ├── jobfetch.js         # Job search functionality
│   ├── login-script.js     # Login form validation
│   ├── script.js           # Other JS logic
│   └── style.css           # CSS styling
│
├── templates/
│   ├── adminlogin.html     # Admin login page
│   ├── apply.html          # Job application form
│   ├── index.html          # Landing page
│   ├── indexsearch.html    # Job search results
│   ├── job-post.html       # Employer job post form
│   ├── job.html            # All jobs listing
│   ├── login.html          # User login page
│   ├── manage.html         # Admin dashboard
│   ├── managejobs.html     # Admin job management
│   ├── manageusers.html    # Admin user management
│   └── register.html       # User registration page
│
└── requirements.txt        # Project dependencies
```

## ⚙️ Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Templating**: Jinja2 (Flask templates)

## 🚀 Features

- User Registration and Login
- Job Listing and Search by keyword/location/company
- Apply to Available Jobs
- Employer Dashboard to Post and Manage Jobs
- Admin Panel to Manage Users and Jobs
- Clean and Responsive UI

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <git remote add origin https://github.com/basavaraj-ops/job-portal-web-application.git>
   cd FRONTEND/backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```



## 📝 Future Improvements


- Job filters by type/salary/date
- Password reset and email verification
- JWT-based authentication
- Pagination and performance optimization




