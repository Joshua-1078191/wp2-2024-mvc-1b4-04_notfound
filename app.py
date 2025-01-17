import difflib
import json
from io import BytesIO
from json import JSONDecodeError

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort
from src.models.users import Users
from src.models.question import Questions
from src.models.prompts import Prompts
from src.models.taxonomy import Taxonomy
from lib.gpt.bloom_taxonomy import get_bloom_category

app = Flask(__name__)
app.secret_key = "adwdafawaf"
database_path = 'databases/database.db'

def check_login(require_admin = False):
    if 'user_id' not in session:
        return redirect('/index/login')
    if require_admin and session.get('is_admin'):
        abort(401)
    return None

@app.route('/')
def main():
    return render_template("homepage.jinja")

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

        users_model = Users(database_path)

        # Try to log in
        user = users_model.login(email, password) #Users.get_by_email(email)

        # If login failed
        if not user:
            flash('Email of wachtwoord is incorrect', 'error')
            return render_template("login.html.jinja")

        session['user_id'] = user['id']
        session['display_name'] = user['name']
        session['is_admin'] = user['isAdmin']
        return redirect('/')

    return render_template("login.html.jinja")


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
            question_model = Questions(database_path)
            question_model.add_questions([
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

@app.route('/export', methods=['GET'])
def export_questions():
    questions_model = Questions(database_path)

    export_all = request.args.get('all', False)
    if export_all:
        questions = questions_model.export_all_questions()
    else:
        questions = questions_model.export_questions()

    if questions and len(questions) > 0:
        converted = [
            {
                "question_id": question.get("questions_id"),
                "question": question.get("question"),
                "answer": question.get("answer"),
                "vak": question.get("subject"),
                "onderwijsniveau": question.get("education"),
                "leerjaar": question.get("grade"),
            } for question in questions]

        return send_file(BytesIO(bytes(json.dumps(converted), 'utf-8')), as_attachment=True, download_name="questions.json")

    flash("Failed to export database")
    return redirect(url_for('toetsvragen_view'))

@app.route('/index/<question_id>', methods=['GET', 'POST'])
def index_questions_prompt(question_id:int|str):

    if request.method == 'POST':
        prompt_id = request.form.get('selectedPrompt')
        if prompt_id:
            return redirect(url_for('index_questions_taxonomy', question_id=question_id, prompt_id=prompt_id))
        flash("Invalid prompt")
        return redirect(request.url)

    question_model = Questions(database_path)
    question = question_model.get_question(question_id)

    prompt_model = Prompts(database_path)
    prompts = prompt_model.get_available_prompts()

    return render_template("questions/index_questions_prompt.html.jinja", question=question, prompts=prompts)

@app.route('/index/<question_id>/<int:prompt_id>', methods=['GET', 'POST'])
def index_questions_taxonomy(question_id:int|str, prompt_id:int):
    question_model = Questions(database_path)
    question = question_model.get_question(question_id)

    if not question:
        flash('Question does not exist', 'error')
        return redirect(url_for('toetsvragen_view'))

    if question['prompts_id']:
        flash('Question already has selection', 'error')
        return redirect(url_for('toetsvragen_view'))

    prompt_model = Prompts(database_path)

    prompt = prompt_model.get_prompt(prompt_id)
    if not prompt:
        flash('Prompt does not exist', 'error')
        return redirect(url_for('toetsvragen_view'))

    if prompt['archived']:
        flash('Prompt is archived', 'error')
        return redirect(url_for('toetsvragen_view'))

    if request.method == 'POST':
        question_model.edit_question(question_id, taxonomy_id=request.form.get('taxonomy'))
        unchanged = request.form.get('autoSuggestion') == request.form.get('taxonomy')
        success = prompt_model.add_prompt_question_result(prompt_id, unchanged)
        flash('', 'success' if success else 'error')
        return redirect(url_for('toetsvragen_view'))

    #question = {
    #    'question': "Welke twee stoffen ontstaan bij Fotosynthese?",
    #    'answer': "",
    #    'subject': "biologie",
    #    'education': "havo",
    #    'grade': 3,
    #}

    if not question:
        return redirect(url_for('toetsvragen_view'))

    try:
        prompt = prompt_model.get_prompt(prompt_id)
        categorie = get_bloom_category(question['question'], prompt['prompt'], "rac_test")

        explanation = categorie['uitleg']

        taxonomy_model = Taxonomy(database_path)
        taxonomies = taxonomy_model.get_all_taxonomies()

        closest_value = difflib.get_close_matches(categorie['niveau'], list(taxonomies.values()))


        closest_key = None
        if closest_value:
            closest_key = next(key for key, value in taxonomies.items() if value == closest_value[0])

        answer = {
            'selected_taxonomy': closest_key,
            'explanation': explanation
        }

        return render_template("questions/index_questions_taxonomy.html.jinja", question=question, taxonomies=taxonomies, answer=answer)

    except Exception as e:
        print(e)
        return redirect(url_for('toetsvragen_view'))

@app.route('/prompts/add', methods=['GET', 'POST'])
def add_prompt():
    if result := check_login(): return result

    prompts_model = Prompts(database_path)

    if request.method == 'POST':
        prompt_id = prompts_model.add_prompt(
            #user_id=int(request.form['user_id']),
            user_id=session['user_id'],
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

        model = prompts_model.get_prompt(prompt_id)
        if session['is_admin'] or session['user_id'] == model['user_id']:
            success = prompts_model.edit_prompt(
                prompts_id=prompt_id,
                user_id=int(request.form.get('user_id')) if session['is_admin'] else None,
                prompt_name=request.form.get('prompt_name'),
                prompt=request.form.get('prompt') if model['questions_count'] == 0 else None,
                questions_count=int(request.form.get('questions_count')),
                questions_correct=int(request.form.get('questions_correct'))
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
    return render_template('prompts/edit_prompt.html.jinja', prompt=prompt, users=users, is_admin=session['is_admin'])

@app.route('/prompts/delete/<int:prompt_id>', methods=['POST'])
def delete_prompt(prompt_id):
    if result := check_login(): return result

    prompts_model = Prompts(database_path)

    if prompts_model.delete_prompt(prompt_id):
        flash('Prompt succesvol verwijderd!', 'success')
    else:
        flash('Er is een fout opgetreden bij het verwijderen van de prompt.', 'error')
    return redirect(url_for('prompts_view'))

@app.route('/prompts/prompt_details/<int:prompt_id>', methods=['GET', 'POST'])
def prompt_details(prompt_id:int):
    prompt_model = Prompts(database_path)
    return render_template("prompts/prompt_details.html.jinja", prompt = prompt_model.get_prompt(prompt_id))

@app.route('/prompts/archive/<int:prompt_id>', methods=['POST'])
def archive_prompt(prompt_id):
    if result := check_login(): return result

    prompts_model = Prompts(database_path)

    prompt = prompts_model.get_prompt(prompt_id)
    set_archived = not bool(prompt['archived'])
    if prompt is not None and prompts_model.edit_prompt(prompt_id, archived=set_archived):
        flash('Prompt succesvol gearchiveerd!' if set_archived else 'Prompt succesvol hersteld!', 'success')
    else:
        flash('Er is een fout opgetreden bij het archiveren van de prompt.', 'error')
    return redirect(url_for('prompts_view'))

@app.route('/prompts/prompts_view', methods=['GET', 'POST'])
@app.route('/prompts')
def prompts_view():
    if result := check_login(): return result
    prompt_models = Prompts(database_path)
    return render_template("prompts/prompts_view.html.jinja", prompts = prompt_models.prompt_all_view())

@app.route('/prompts/copy/<int:prompt_id>', methods=['POST'])
def copy_prompt(prompt_id):
    if result := check_login(): return result

    prompts_model = Prompts(database_path)
    new_prompt_id = prompts_model.copy_prompt(prompt_id)

    if new_prompt_id:
        flash('Prompt successfully copied!', 'success')
    else:
        flash('Failed to copy prompt.', 'error')

    return redirect(url_for('prompts_view'))

@app.route('/toetsvragen_view', methods=['GET', 'POST'])
def toetsvragen_view():
    if result := check_login(): return result
    if request.method == 'GET' or request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        questions_model = Questions(database_path)
        questions = questions_model.get_paginated_questions(page, per_page)

        taxonomy_model = Taxonomy(database_path)
        taxonomies = taxonomy_model.get_all_taxonomies()

        return render_template('prompts/toetsvragen_view.html.jinja',
                               questions=questions,
                               taxonomies=taxonomies,
                               page=page,
                               per_page=per_page)

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
            prompts_id=int(request.form['prompts_id']),
            answer=request.form['answer'],
            taxonomy_id=int(request.form['taxonomy_id'])
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

@app.route('/toetsvragen/edit/<string:question_id>', methods=['GET', 'POST'])
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
            prompts_id=int(request.form['prompts_id']),
            answer=request.form['answer'],
            taxonomy_id=int(request.form['taxonomy_id'])
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
    taxonomy_model = Taxonomy(database_path)
    taxonomies = taxonomy_model.get_all_taxonomies()

    return render_template('prompts/edit_question.html.jinja',
                         question=question,
                         prompts=prompts,
                         taxonomies=taxonomies)

@app.route('/toetsvragen/delete/<string:question_id>', methods=['POST'])
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

    users_model = Users(database_path)

    if request.method == 'POST':
        nieuwe_redacteur_id = users_model.register(
            email=request.form.get('email'),
            password=request.form.get('password'),
            username=request.form.get('name'),
            is_admin=bool(request.form.get('is_admin', False))
        )
        if nieuwe_redacteur_id:
            flash('Redacteur succesvol toegevoegd!', 'success')
            return redirect(url_for('lijst_redacteuren'))

    return render_template("redacteurs/nieuwe_redacteur.html.jinja")

@app.route('/redacteurs/redacteur_wijzigen/<int:id>', methods=['GET', 'POST'])
def redacteur_wijzigen(id):
    if result := check_login(): return result

    users = Users(database_path)
    editor = users.get(id)

    if not editor:
        flash('De opgegeven redacteur bestaat niet.', 'danger')
        return redirect(url_for('lijst_redacteuren'))

    editor_id = editor['id']
    is_admin = session.get('is_admin', False)
    current_user_id = session.get('user_id')

    if editor_id != current_user_id and not is_admin:
        flash('Je kunt alleen je eigen gegevens wijzigen.', 'danger')
        return redirect(url_for('lijst_redacteuren'))

    if request.method == 'POST':
        if 'delete' in request.form and is_admin:
            user_deleted = users.delete(id)
            if user_deleted:
                flash('Redacteur succesvol verwijderd. Vragen beoordeeld door deze redacteur blijven bestaan.', 'success')
            else:
                flash('Redacteur kon niet worden verwijderd.', 'danger')
        else:
            gegevens_wijzigen = users.update(
                target_id=id,
                email=request.form.get('email'),
                password=request.form.get('password'),
                username=request.form.get('name'),
                is_admin=bool(request.form.get('is_admin', False)) if is_admin else editor['isAdmin']
            )
            if gegevens_wijzigen:
                flash('Redacteurs gegevens succesvol gewijzigd!', 'success')

        return redirect(url_for('lijst_redacteuren'))  # Terug naar de lijst van redacteurs

    return render_template("redacteurs/redacteur_wijzigen.html.jinja", editor=editor)


@app.route('/style_guide')
def style_guide():
    return render_template("example/style_guide.html.jinja")
    

if __name__ == '__main__':
    app.run(debug=True)