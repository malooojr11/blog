from flask import abort, flash, render_template, request, url_for, redirect, Blueprint, g
import functools
import sqlite3

DATABASE = 'blogstie.db'
bp = Blueprint('blog', __name__, url_prefix='/posts')

def get_db():
    """
    Returns a database connection, ensuring it's stored in the app context (g).
    Enables WAL mode for better concurrency.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Return rows as dictionaries for easier access
        g.db.execute('PRAGMA journal_mode=WAL;')  # Enable WAL for concurrent read/writes
    return g.db


def get_post(post_id, check_author=True):
    """
    Fetches a blog post by ID from the database.
    Optionally checks if the current user is the author (for update/delete operations).
    """
    post = get_db().execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if post is None:
        abort(404, f"Can't find blog with ID: {post_id}")
    
    # If check_author is True, verify the logged-in user is the author of the post
    if check_author and post['author_id'] != g.user:
        abort(403)  # Unauthorized if the current user is not the author
    
    return post


@bp.teardown_app_request
def close_db(error):
    """
    Closes the database connection after the request finishes.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def login_required(func):
    """
    A decorator that ensures a user is logged in before accessing the route.
    Redirects to login page if the user is not authenticated.
    """
    @functools.wraps(func)
    def wrapped_func(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return func(**kwargs)
    return wrapped_func


@bp.route('/')
def index():
    """
    Displays a list of all blog posts on the homepage.
    """
    connection = get_db()
    try:
        posts = connection.execute('SELECT * FROM posts').fetchall()
    finally:
        connection.close()
    return render_template('index.html', posts=posts, title='HomePage')


@bp.route('/<int:post_id>')
def show(post_id):
    """
    Displays a single blog post by its ID.
    """
    post = get_post(post_id, check_author=False)  # No need to check author for viewing
    return render_template('show.html', post=post, title='Blogs')


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """
    Handles the creation of a new blog post.
    - GET: Renders the create form.
    - POST: Inserts a new blog post into the database.
    """
    if request.method == 'POST':
        connection = get_db()
        title = request.form['title']
        body = request.form['body']
        
        # Insert new post into the database
        try:
            connection.execute('INSERT INTO posts (title, body, author_id) VALUES (?, ?, ?)', 
                            (title, body, g.user))  # g.user is the logged-in user's ID
            connection.commit()
        except sqlite3.OperationalError as e:
            print("OperationalError:", e)
            flash('Database error, please try again.')
        return redirect(url_for('blog.index'))
    
    return render_template('create.html', title='Create Blog')


@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    """
    Handles updating an existing blog post.
    - GET: Renders the update form with the current post content.
    - POST: Updates the post in the database.
    """
    post = get_post(post_id,check_author=False)  # Ensure the user is the author

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'

        if error:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE posts SET title = ?, body = ? WHERE id = ?', 
                    (title, body, post_id))
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('create.html', post=post, title='Update Blog')


@bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    """
    Deletes a blog post by ID. Only the author can delete the post.
    """
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    db.close()
    return redirect(url_for('blog.index'))

