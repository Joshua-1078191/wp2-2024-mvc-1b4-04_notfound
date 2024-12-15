from flask import Flask, render_template, session, redirect, url_for, request, flash
from src.models.user import User

app = Flask(__name__)
app.secret_key = 'random'

def check_login():
    if 'user_id' not in session:
        return redirect('/index/login')
    return None

@app.route('/')
def main():
    if 'user_id' not in session:
        return redirect('/index/login')
    return render_template("index-1.html.jinja")

@app.route('/index/login', methods=['GET', 'POST'])
def login_route():
    if 'user_id' in session:
        return redirect('/')
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Please enter both email and password', 'error')
            return render_template("login.html.jinja")
        
        # First check if email exists
        user = User.get_by_email(email)
        if not user:
            flash('No account found with this email', 'error')
            return render_template("login.html.jinja")
        
        # Then check if password matches
        user = User.get_by_credentials(email, password)
        if not user:
            flash('Incorrect password', 'error')
            return render_template("login.html.jinja")
        
        session['user_id'] = user.user_id
        session['display_name'] = user.display_name
        session['is_admin'] = user.is_admin
        return redirect('/')
    
    return render_template("login.html.jinja")

@app.route('/index/sign_up', methods=['GET', 'POST'])
def sign_up_route():
    if 'user_id' in session:
        return redirect('/')
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template("sign_up.html.jinja")
        
        # Check if email already exists
        if User.get_by_email(email):
            flash('Email already registered', 'error')
            return render_template("sign_up.html.jinja")
        
        # Create new user
        if User.create_user(email, password):
            flash('Account created successfully! Please log in.', 'success')
            return redirect('/index/login')
        else:
            flash('An error occurred while creating your account', 'error')
            return render_template("sign_up.html.jinja")
    
    return render_template("sign_up.html.jinja")

@app.route('/index/logout')
def logout_route():
    session.clear()
    return redirect('/index/login')

@app.route('/import', methods=['GET', 'POST'])
def import_questions():
    if result := check_login(): return result
    return render_template("questions/import_questions.html.jinja")

@app.route('/index', methods=['GET', 'POST'])
def index_questions_prompt():
    if result := check_login(): return result
    if request.method == 'POST':
        return redirect(url_for('index_questions_taxonomy', prompt_id=1))
    return render_template("questions/index_questions_prompt.html.jinja")

@app.route('/index/<int:prompt_id>', methods=['GET', 'POST'])
def index_questions_taxonomy(prompt_id:int):
    if result := check_login(): return result
    return render_template("questions/index_questions_taxonomy.html.jinja")

@app.route('/index/add_prompt', methods=['GET', 'POST'])
def add_prompt():
    if result := check_login(): return result
    return render_template("prompts/add_prompt.html.jinja")

@app.route('/index/prompt_details', methods=['GET', 'POST'])
def prompt_details():
    if result := check_login(): return result
    return render_template("prompts/prompt_details.html.jinja")

@app.route('/index/prompts_view', methods=['GET', 'POST'])
def prompts_view():
    if result := check_login(): return result
    return render_template("prompts/prompts_view.html.jinja")

@app.route('/index/toetsvragen_view', methods=['GET', 'POST'])
def toetsvragen_view():
    if result := check_login(): return result
    return render_template("prompts/toetsvragen_view.html.jinja")

@app.route('/index/vragen', methods=['GET', 'POST'])
def vragen():
    if result := check_login(): return result
    return render_template("vragen.html.jinja")

if __name__ == '__main__':
    app.run(debug=True)