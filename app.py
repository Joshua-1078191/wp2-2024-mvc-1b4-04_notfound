import json
from json import JSONDecodeError

from flask import Flask, render_template, request, redirect, url_for, session, Response, flash
from src.models.users import Users
from src.models.prompts import Prompts
from lib.gpt.bloom_taxonomy import get_bloom_category

app = Flask(__name__)
app.secret_key = "adwdafawaf"
database_path = 'databases/database.db'

@app.route('/')
def main():
    return render_template("index-1.html.jinja")

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
        prompt_id = prompts.add_prompt(1, prompt, 100, 80)
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

@app.route('/questions/toetsvragen_view/<int:prompt_id>', methods=['GET', 'POST'])
def toetsvragen_view(prompt_id:int):
    questions = [{
        prompt_id: 1,
        "prompt" : "prompt ....",
        "id" : 1,
        "question_name" : "vraag 1",
        "subject" : "Biologie",
        "school_grade" : "Havo 3",
        "creation_date" : "14-7-2020",
        "answered_correctly" : True,
    }]
    if request.method == 'POST':
        keyword = request.form['keyword']
        school_level = request.form['school_level']
        subject = request.form['subject']
    else:
        return render_template("prompts/toetsvragen_view.html.jinja", questions=questions)

# @app.route('/index/login', methods=['GET', 'POST'])
# def toetsvragen_view():
#     return render_template("login.html.jinja")

# @app.route('/index/sign_up', methods=['GET', 'POST'])
# def toetsvragen_view():
#     return render_template("sign_up.html.jinja")

# @app.route('/index/vragen', methods=['GET', 'POST'])
# def toetsvragen_view():
#     return render_template("vragen.html.jinja")

@app.route('/lijst_redacteuren', methods=['GET', 'POST'])
def lijst_redacteuren():
    users = Users(database_path)
    return render_template("lijst_redacteuren.html.jinja", editors=users.get_all())

@app.route('/nieuwe_redacteur', methods=['GET', 'POST'])
def nieuwe_redacteuren():
    return render_template("nieuwe_redacteur.html.jinja")

@app.route('/redacteur_wijzigen/<int:id>', methods=['GET', 'POST'])
def redacteur_wijzigen(id):
    users = Users(database_path)
    return render_template("redacteur_wijzigen.html.jinja", editor=users.get(id))

if __name__ == '__main__':
    app.run(debug=True)