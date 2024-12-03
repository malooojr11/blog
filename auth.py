from flask import request, redirect, render_template, url_for, flash, session, g, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from blog import get_db, login_required


bp = Blueprint('auth', __name__)


@bp.before_app_request
def load_logged_in_user():
    """
    Runs before every request to load the current user if they're logged in.
    Stores the user ID in g.user and the full user details in g.user_details.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
        g.user_details = None  # No user details if not logged in
    else:
        # Fetch the full user details and store them in g.user_details for template use
        user = get_db().execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        g.user = user['id']  # Store only the user ID in g.user for ID-based operations
        g.user_details = user  # Store the full user details for template access

@bp.route('/dashboard')
@login_required  # Ensure the user is logged in
def dashboard():
    db =get_db()
    user_details = g.user_details  # Get the logged-in user's details from g.user_details
    if user_details is None:
        return redirect(url_for('auth.login'))  # Redirect to login page if no user details found
    
    # Fetch the user's blog posts
    posts = db.execute('SELECT id, title, body, created_at FROM posts WHERE author_id = ?', (user_details['id'],)).fetchall()
    
    return render_template('dashboard.html', user=user_details, posts=posts)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration. 
    - GET: Renders the registration form.
    - POST: Validates the form data and creates a new user in the database.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        # Simple validation of form data
        if not username:
            error = 'Username is not valid'
        if not email:
            error = 'Email is not valid'
        if not password:
            error = 'Password is not valid'

        if error is None:
            db = get_db()
            try:
                # Insert the new user into the users table with a hashed password
                db.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                        (username, generate_password_hash(password), email))
                db.commit()
            except db.IntegrityError:
                # If the username or email already exists, handle the integrity error
                error = f'{username} already exists'
            else:
                # Redirect to login after successful registration
                return redirect(url_for('auth.login'))
            flash(error)
    return render_template('auth/register.html', title='Register')


@bp.route('/login', methods=['POST', 'GET'])
def login():
    """
    Handles user login.
    - GET: Renders the login form.
    - POST: Validates user credentials and creates a session.
    """

    if g.user:
        return redirect(url_for('blog.index'))  # Redirect if already logged in
    
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        error = None
        db = get_db()
        # Fetch the user by email from the database
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if not user:
            error = 'Email not found'
        elif not check_password_hash(user['password'], password):
            # Check if the password hash matches
            error = 'Wrong password'

        if error is None:
            session.clear()  # Clear any existing session
            session['user_id'] = user['id']  # Set user_id in session for tracking logged-in user
            return redirect(url_for('blog.index'))
        
        flash(error)

    return render_template('auth/login.html', title='Login')


@bp.route('/logout')
def logout():
    """
    Logs the user out by clearing the session and redirecting to the blog index.
    """
    session.clear()  # Clear all session data
    return redirect(url_for('blog.index'))

