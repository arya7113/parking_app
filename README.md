# Parking Management System

A Flask-based web application for managing parking spaces, reservations, and user accounts.

## Project Structure

This Flask application follows a clean MVC architecture with clear separation of concerns:

- **`endpoints/`** - Contains all route handlers organized by functionality:
  - `admin/` - Administrative routes and forms
  - `auth/` - Authentication and authorization routes
  - `user/` - User-specific routes and functionality
- **`models/`** - SQLAlchemy database models and data access layer
- **`templates/`** - HTML templates (base.html, home.html, navbar.html)
- **`static/`** - Static assets (CSS, JavaScript, images)
- **`internals/`** - Internal utilities and configuration
- **`dals/`** - Data Access Layer for database operations

The application uses server-side rendering with Flask's templating system and maintains organized hierarchical routing that reflects the parking management workflow.

## Features

- User authentication and authorization
- Parking space management
- Reservation system
- Administrative dashboard
- Responsive web interface

## Requirements

- Python 3.7+
- Flask
- SQLAlchemy
- Other dependencies listed in `requirements.txt`

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd parking_app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```


## Running the Application

1. **Activate your virtual environment** (if not already activated)
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the Flask application**
   ```bash
   python3 server.py
   ```

3. **Access the application**
   
   Open your web browser and navigate to: `http://localhost:5000`

