# Flask Auth Blueprint
A modular, plug-and-play authentication blueprint for Flask apps.

## Features
- **Modular Blueprint:** Easily portable into any Flask application.
- **Robust Forms:** Built with Flask-WTF (validation rules are enforced on both the client-side and server-side).
- **Secure Hashing:** Utilizes Bcrypt for industry-standard password protection.
- **Real-Time Validation (JS):** 
  - Dynamic client-side password matching.
  - Debounced async requests (`fetch`) to check username availability on-the-fly.
- **Decoupled Database (`db.py`):** Utilizes `g.db` context, freeing the blueprint from hardcoded imports.
 
## Usage
### Running Locally
Follow these commands to set up and run the developer environment.
```bash
# install dependencies
pip install flask flask-wtf flask-bcrypt
# initialize database
flask init-db
# run app
flask --app auth run
```

### Using in a New Project
1. **Copy the module:**
   Copy the `auth/` directory into your new project.

2. **Ensure Database Context:**
   The blueprint expects a database connection object to be present on Flask's global context (`g.db`). Ensure your new project initializes dynamic requests with this connection (e.g., using `app.before_request`).

3. **Register the blueprint:**
   Add this to your new project's initialization file:
   ```python
   from flask import Flask
   from auth.blueprints import auth
   
   # initialize the main Flask application
   app = Flask(__name__)
   
   # register blueprint
   app.register_blueprint(auth.bp)
   ```