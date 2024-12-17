import json
from json import JSONDecodeError

from flask import Flask, render_template, request, redirect, url_for, session, Response, flash
from flask import Flask, render_template, session, redirect, url_for, request, flash
from src.models.user import User
from src.models.question import Question
from src.models.prompts import Prompts
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
            return Response(json.dumps(questions[0], indent = 4), mimetype='application/json')

        flash("No data in JSON")
        return redirect(request.url)

    return render_template("questions/import_questions.html.jinja")

@app.route('/index/<int:question_id>', methods=['GET', 'POST'])
def index_questions_prompt(question_id:int):
    if request.method == 'POST':
        prompt_id = request.form.get('selectedPrompt')
        if prompt_id:
            try:
                prompt_id = int(prompt_id)
                return redirect(f'{request.url}/{prompt_id}')
            except ValueError:
                pass
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

@app.route('/index/<int:question_id>/<int:prompt_id>', methods=['GET', 'POST'])
def index_questions_taxonomy(question_id:int, prompt_id:int):

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

@app.route('/prompts/add_prompt', methods=['GET', 'POST'])
def add_prompt():
    prompts = Prompts(database_path)
    if request.method == 'POST':
        prompt_titel = request.form['prompt-title']
        prompt = request.form['prompt-text']
        prompt_id = prompts.add_prompt(1, prompt_titel, prompt, 100, 80)
        return redirect(url_for(f'prompt_details', prompt_id=prompt_id))
    else:
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

@app.route('/prompts/prompts_view', methods=['GET', 'POST'])
def prompts_view():
    prompt_models = Prompts(database_path)
    prompts = [{
        "id" : 1,
        "prompt" : "prompt ....",
        "name" : "testnaam",
        "categorised_questions" : 100,
        "correct_questions" : "90%",
    },{
        "id" : 2,
        "prompt" : "prompt 2",
        "name" : "testnaam 2",
        "categorised_questions" : 200,
        "correct_questions" : "80%",
    },{
        "id" : 3,
        "prompt" : "prompt 3",
        "name" : "testnaam 3",
        "categorised_questions" : 300,
        "correct_questions" : "70%",
    }
    ]
    return render_template("prompts/prompts_view.html.jinja", prompts = prompt_models.prompt_all_view())

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

@app.route('/redacteurs/lijst_redacteuren', methods=['GET', 'POST'])
def lijst_redacteuren():
    users = Users(database_path)
    return render_template("redacteurs/lijst_redacteuren.html.jinja", editors=users.get_all())

@app.route('/redacteurs/nieuwe_redacteur', methods=['GET', 'POST'])
def nieuwe_redacteuren():
    return render_template("redacteurs/nieuwe_redacteur.html.jinja")

@app.route('/redacteurs/redacteur_wijzigen/<int:id>', methods=['GET', 'POST'])
def redacteur_wijzigen(id):
    users = Users(database_path)
    return render_template("redacteurs/redacteur_wijzigen.html.jinja", editor=users.get(id))

if __name__ == '__main__':
    app.run(debug=True)