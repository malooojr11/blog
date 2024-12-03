# Flask Blog Application

A lightweight and extensible blog application built with Flask, featuring user authentication, post management, and a clean code structure using blueprints. This project provides essential features for a blog platform, such as user registration, login/logout, creating, updating, and deleting blog posts.

---

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Routes Overview](#routes-overview)
- [Project Structure](#project-structure)


---

## Features

### User Authentication:
- **Register**
- **Login/Logout**

### Blog Management:
- View all posts
- Create, edit, and delete blog posts (only for the post's author)
- Dashboard for users to manage their content
- Secure password storage using `werkzeug.security`

### Organized Structure:
- Clean and modular design using Flask Blueprints

---



## Getting Started
- Prerequisites
- Python 3.8+
- Flask 2.0+
- SQLite (built-in with Python)

## Setup Instructions
- Clone the repository:

`git clone https://github.com/malooojr11/blog.git
cd blog`

- Create and activate a virtual environment:

`python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate`

- Install dependencies:

`pip install flask`

- Set up the database:
Create an SQLite database named blogsite.db and initialize it with the required tables:

`sqlite3 blogsite.db < schema.sql`

- Run the application:

`python app.py`


## Usage
- Register a new user:
Visit [/auth/register](url).

- Login with your credentials:
Visit[ /auth/login](url).

### Manage your posts:
- Access your dashboard at [/auth/dashboard](url).
- Create posts at [/posts/create](url).
- View posts on the homepage[ /](url).
- Edit or delete posts via respective routes.
- The application will be available at [http://127.0.0.1:5000](url).

# Routes Overview
### Authentication (`auth.py`)

| Route               | Method    | Description             |
|---------------------|-----------|-------------------------|
| `/auth/register`    | GET/POST  | User registration       |
| `/auth/login`       | GET/POST  | User login              |
| `/auth/logout`      | GET       | Logs out the user       |
| `/auth/dashboard`   | GET       | Dashboard to manage posts |

### Blog Management (`blog.py`)

| Route               | Method    | Description             |
|---------------------|-----------|-------------------------|
| `/`                 | GET       | Homepage displaying posts |
| `/posts/create`     | GET/POST  | Create a new blog post  |
| `/posts/<id>`       | GET       | View a specific post    |
| `/posts/<id>/update`| GET/POST  | Edit an existing post   |
| `/posts/<id>/delete`| POST      | Delete a specific post  |

## Project Structure
```plaintext
.
├── app.py               # Main application entry point
├── auth.py              # User authentication blueprint
├── blog.py              # Blog posts blueprint
├── templates/           # HTML templates for rendering views
│   ├── auth/
│   ├── blog/
│   └── base.html
├── static/              # Static files (CSS, JS, images)
├── blogsite.db          # SQLite database file
└── README.md            # Project documentation
