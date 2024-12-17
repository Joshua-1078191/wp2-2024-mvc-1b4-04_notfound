import json
from json import JSONDecodeError


from flask import Flask, render_template, request, redirect, url_for, session, Response, flash
from src.models.user import User
from src.models.users import Users
from src.models.question import Questions
from src.models.prompts import Prompts
from src.models.taxonomy import Taxonomy
from lib.gpt.bloom_taxonomy import get_bloom_category

app = Flask(__name__)
app.secret_key = "adwdafawaf"
database_path = 'databases/database.db'

def check_login():
    if 'user_id' not in session:
        return redirect('/index/login')
    return None

@app.route('/')
def main():
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
    if request.method == 'POST':
        if 'jsonFile' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['jsonFile']
        if file.filename == '':
            flash("No file selected")
            return redirect(request.url)
        try:
            questions:list[dict[str, object]] = json.load(file.stream)
        except (UnicodeDecodeError, JSONDecodeError):
            flash("Invalid JSON")
            return redirect(request.url)

        if questions:
            Questions.save_many([
                {
                    "questions_id": question.get("question_id"),
                    "question": question.get("question"),
                    "subject": question.get("vak"),
                    "grade": question.get("leerjaar"),
                    "education": question.get("onderwijsniveau"),
                    "answer": question.get("answer"),
                } for question in questions
            ])
            return redirect(url_for('toetsvragen_view'))

        flash("No data in JSON")
        return redirect(request.url)

    return render_template("questions/import_questions.html.jinja")

@app.route('/index/<question_id>', methods=['GET', 'POST'])
def index_questions_prompt(question_id:int|str):
    if request.method == 'POST':
        prompt_id = request.form.get('selectedPrompt')
        if prompt_id:
            return redirect(url_for('index_questions_taxonomy', question_id=prompt_id, prompt_id=prompt_id))
        flash("Invalid prompt")
        return redirect(request.url)

    question = {
        'question': "Welke twee stoffen ontstaan bij Fotosynthese?",
        'answer': "Glucose en zuurstof, per onderdeel 1 punt",
        'subject': "biologie",
        'education': "havo",
        'grade': 3,
    }

    prompts = [
        {
            'id': 0,
            'name': "Één van de prompts"
        },
        {
            'id': 1,
            'name': "Een andere prompt die ook bestaat"
        },
    ]

    return render_template("questions/index_questions_prompt.html.jinja", question=question, prompts=prompts)

@app.route('/index/<question_id>/<int:prompt_id>', methods=['GET', 'POST'])
def index_questions_taxonomy(question_id:int|str, prompt_id:int):

    question = {
        'question': "Welke twee stoffen ontstaan bij Fotosynthese?",
        'answer': "",
        'subject': "biologie",
        'education': "havo",
        'grade': 3,
    }

    prompt = prompt_id # change
    categorie = get_bloom_category(question['question'], prompt, "dry_run")

    question['answer'] = categorie['categorie']

    explanation = categorie['uitleg']

    taxonomies = [
        {
            'name': 'Kennis',
            'id': 0,
        },
        {
            'name': 'Begrijpen',
            'id': 1,
        },
        {
            'name': 'Toepassen',
            'id': 2,
        },
        {
            'name': 'Analyseren',
            'id': 3,
        },
        {
            'name': 'Evalueren',
            'id': 4,
        },
        {
            'name': 'Synthese',
            'id': 5,
        },
    ]

    answer = {
        'selected_taxonomy': 2,
        'explanation': explanation
    }

    return render_template("questions/index_questions_taxonomy.html.jinja", question=question, taxonomies=taxonomies, answer=answer)

@app.route('/prompts/add', methods=['GET', 'POST'])
def add_prompt():
    if result := check_login(): return result

    prompts_model = Prompts(database_path)

    if request.method == 'POST':
        prompt_id = prompts_model.add_prompt(
            user_id=int(request.form['user_id']),
            prompt_name=request.form['prompt_name'],
            prompt=request.form['prompt'],
            questions_count=0,
            questions_correct=0
        )
        if prompt_id:
            flash('Prompt succesvol toegevoegd!', 'success')
            return redirect(url_for('prompts_view'))
        flash('Er is een fout opgetreden bij het toevoegen van de prompt.', 'error')

    users = prompts_model.get_all_users()
    return render_template('prompts/add_prompt.html.jinja', users=users)

@app.route('/prompts/edit/<int:prompt_id>', methods=['GET', 'POST'])
def edit_prompt(prompt_id):
    if result := check_login(): return result

    prompts_model = Prompts(database_path)

    if request.method == 'POST':
        success = prompts_model.edit_prompt(
            prompts_id=prompt_id,
            user_id=int(request.form['user_id']),
            prompt_name=request.form['prompt_name'],
            prompt=request.form['prompt'],
            questions_count=int(request.form['questions_count']),
            questions_correct=int(request.form['questions_correct'])
        )
        if success:
            flash('Prompt succesvol bijgewerkt!', 'success')
            return redirect(url_for('prompts_view'))
        flash('Er is een fout opgetreden bij het bijwerken van de prompt.', 'error')
        return redirect(url_for('prompts_view'))

    prompt = prompts_model.get_prompt(prompt_id)
    if not prompt:
        flash('Prompt niet gevonden.', 'error')
        return redirect(url_for('prompts_view'))

    users = prompts_model.get_all_users()
    return render_template('prompts/edit_prompt.html.jinja', prompt=prompt, users=users)

@app.route('/prompts/delete/<int:prompt_id>', methods=['POST'])
def delete_prompt(prompt_id):
    if result := check_login(): return result

    prompts_model = Prompts(database_path)
    if prompts_model.delete_prompt(prompt_id):
        flash('Prompt succesvol verwijderd!', 'success')
    else:
        flash('Er is een fout opgetreden bij het verwijderen van de prompt.', 'error')
    return redirect(url_for('prompts_view'))

@app.route('/prompts')
def prompts_view():
    if result := check_login(): return result
    prompts_model = Prompts(database_path)
    prompts = prompts_model.prompt_all_view()
    return render_template('prompts/prompts_view.html.jinja', prompts=prompts)

@app.route('/toetsvragen_view')
def toetsvragen_view():
    if result := check_login(): return result
    questions_model = Questions(database_path)
    questions = questions_model.questions_all_view()

    taxonomy_model = Taxonomy(database_path)
    taxonomies = taxonomy_model.get_all_taxonomies()
    return render_template('prompts/toetsvragen_view.html.jinja', questions=questions, taxonomies=taxonomies)

@app.route('/toetsvragen/add', methods=['GET', 'POST'])
def add_question():
    if result := check_login(): return result
    if request.method == 'POST':
        questions_model = Questions(database_path)
        question_id = questions_model.add_question(
            question=request.form['question'],
            subject=request.form['subject'],
            grade=request.form['grade'],
            education=request.form['education'],
            prompts_id=request.form['prompts_id'],
            answer=request.form['answer'],
            taxonomy_id=request.form['taxonomy_id']
        )
        if question_id:
            flash('Vraag succesvol toegevoegd!', 'success')
            return redirect(url_for('toetsvragen_view'))
        flash('Er is een fout opgetreden bij het toevoegen van de vraag.', 'error')

    prompts_model = Prompts(database_path)
    prompts = prompts_model.prompt_all_view()

    taxonomy_model = Taxonomy(database_path)
    taxonomies = taxonomy_model.get_all_taxonomies()
    return render_template('prompts/add_question.html.jinja', prompts=prompts, taxonomies=taxonomies)

@app.route('/toetsvragen/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if result := check_login(): return result

    questions_model = Questions(database_path)

    if request.method == 'POST':
        success = questions_model.edit_question(
            questions_id=question_id,
            question=request.form['question'],
            subject=request.form['subject'],
            grade=request.form['grade'],
            education=request.form['education'],
            prompts_id=request.form['prompts_id'],
            answer=request.form['answer'],
            taxonomy_id=request.form['taxonomy_id']
        )
        if success:
            flash('Vraag succesvol bijgewerkt!', 'success')
            return redirect(url_for('toetsvragen_view'))
        flash('Er is een fout opgetreden bij het bijwerken van de vraag.', 'error')
        return redirect(url_for('toetsvragen_view'))

    question = questions_model.get_question(question_id)
    if not question:
        flash('Vraag niet gevonden.', 'error')
        return redirect(url_for('toetsvragen_view'))

    prompts_model = Prompts(database_path)
    prompts = prompts_model.prompt_all_view()
    taxonomies = Questions.get_all_taxonomies()

    return render_template('prompts/edit_question.html.jinja',
                         question=question,
                         prompts=prompts,
                         taxonomies=taxonomies)

@app.route('/toetsvragen/delete/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    if result := check_login(): return result
    questions_model = Questions(database_path)
    if questions_model.delete_question(question_id):
        flash('Vraag succesvol verwijderd!', 'success')
    else:
        flash('Er is een fout opgetreden bij het verwijderen van de vraag.', 'error')
    return redirect(url_for('toetsvragen_view'))

@app.route('/redacteurs/lijst_redacteuren', methods=['GET', 'POST'])
def lijst_redacteuren():
    if result := check_login(): return result
    users = Users(database_path)
    return render_template("redacteurs/lijst_redacteuren.html.jinja", editors=users.get_all())

@app.route('/redacteurs/nieuwe_redacteur', methods=['GET', 'POST'])
def nieuwe_redacteuren():
    if result := check_login(): return result
    return render_template("redacteurs/nieuwe_redacteur.html.jinja")

@app.route('/redacteurs/redacteur_wijzigen/<int:id>', methods=['GET', 'POST'])
def redacteur_wijzigen(id):
    if result := check_login(): return result
    users = Users(database_path)
    return render_template("redacteurs/redacteur_wijzigen.html.jinja", editor=users.get(id))

if __name__ == '__main__':
    app.run(debug=True)