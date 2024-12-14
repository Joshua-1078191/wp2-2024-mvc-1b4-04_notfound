import json
from json import JSONDecodeError

from flask import Flask, render_template, request, redirect, url_for, session, Response, flash
from src.models.users import Users

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

@app.route('/index', methods=['GET', 'POST'])
def index_questions_prompt():
    if request.method == 'POST':
        return redirect(url_for('index') + '/1')
    return render_template("questions/index_questions_prompt.html.jinja")

@app.route('/index/<int:prompt_id>', methods=['GET', 'POST'])
def index_questions_taxonomy(prompt_id:int):
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
        'explanation': "This is because of facts and logic that are very real and stuff."
    }

    return render_template("questions/index_questions_taxonomy.html.jinja", taxonomies=taxonomies, answer=answer)

@app.route('/prompts/add_prompt', methods=['GET', 'POST'])
def add_prompt():
    return render_template("prompts/add_prompt.html.jinja")

@app.route('/prompts/prompt_details/<int:prompt_id>', methods=['GET', 'POST'])
def prompt_details():
    return render_template("prompts/prompt_details.html.jinja")

@app.route('/prompts/prompts_view', methods=['GET', 'POST'])
def prompts_view():
    return render_template("prompts/prompts_view.html.jinja")

@app.route('/questions/toetsvragen_view/<int:prompt_id>', methods=['GET', 'POST'])
def toetsvragen_view():
    return render_template("prompts/toetsvragen_view.html.jinja")

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
    return render_template("redacteur_wijzigen.html.jinja", editor=users.get(id-1))

if __name__ == '__main__':
    app.run(debug=True)