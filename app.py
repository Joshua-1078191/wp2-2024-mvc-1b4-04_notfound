from flask import Flask, render_template, session, redirect, url_for, request, flash
from src.models.user import User
from src.models.question import Question
from src.models.prompts import Prompts

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

@app.route('/prompts/prompt_details/<int:prompt_id>', methods=['GET', 'POST'])
def prompt_details(prompt_id:int):
    prompt_model = Prompts(database_path)
    prompts = [{
        prompt_id: 1,
        "prompt_naam" : "Jorik's prompt",
        "redacteur" : "Jorik",
        "creation_date" : "02-02-2002",
        "categorised_questions" : 200,
        "correct_questions" : 180,
        "incorrect_questions" : 20,
    }]
    return render_template("prompts/prompt_details.html.jinja", prompts = prompt_model.get_one_prompt(prompt_id))

@app.route('/index/prompts_view', methods=['GET', 'POST'])
def prompts_view():
    if result := check_login(): return result
    return render_template("prompts/prompts_view.html.jinja")

@app.route('/index/toetsvragen_view')
def toetsvragen_view():
    if result := check_login(): return result
    questions = Question.get_all_questions()
    return render_template('prompts/toetsvragen_view.html.jinja', questions=questions)

@app.route('/toetsvragen/add', methods=['GET', 'POST'])
def add_question():
    if result := check_login(): return result
    if request.method == 'POST':
        question = Question(
            question=request.form['question'],
            subject=request.form['subject'],
            grade=request.form['grade'],
            education=request.form['education'],
            prompts_id=request.form['prompts_id'],
            answer=request.form['answer'],
            taxonomy_id=request.form['taxonomy_id']
        )
        if question.save():
            flash('Vraag succesvol toegevoegd!', 'success')
            return redirect(url_for('toetsvragen_view'))
        flash('Er is een fout opgetreden bij het toevoegen van de vraag.', 'error')
    
    taxonomies = Question.get_all_taxonomies()
    prompts = Question.get_all_prompts()
    return render_template('prompts/add_question.html.jinja', 
                         question=None, 
                         taxonomies=taxonomies,
                         prompts=prompts)

@app.route('/toetsvragen/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if result := check_login(): return result
    question = Question.get_by_id(question_id)
    if not question:
        flash('Vraag niet gevonden.', 'error')
        return redirect(url_for('toetsvragen_view'))

    if request.method == 'POST':
        question.question = request.form['question']
        question.subject = request.form['subject']
        question.grade = request.form['grade']
        question.education = request.form['education']
        question.prompts_id = request.form['prompts_id']
        question.answer = request.form['answer']
        question.taxonomy_id = request.form['taxonomy_id']

        if question.save():
            flash('Vraag succesvol bijgewerkt!', 'success')
            return redirect(url_for('toetsvragen_view'))
        flash('Er is een fout opgetreden bij het bijwerken van de vraag.', 'error')

    taxonomies = Question.get_all_taxonomies()
    prompts = Question.get_all_prompts()
    return render_template('prompts/edit_question.html.jinja', 
                         question=question,
                         taxonomies=taxonomies,
                         prompts=prompts)

@app.route('/toetsvragen/delete/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if result := check_login(): return result
    if Question.delete(question_id):
        flash('Vraag succesvol verwijderd!', 'success')
    else:
        flash('Er is een fout opgetreden bij het verwijderen van de vraag.', 'error')
    return redirect(url_for('toetsvragen_view'))

if __name__ == '__main__':
    app.run(debug=True)