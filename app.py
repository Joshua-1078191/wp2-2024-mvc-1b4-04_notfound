from flask import Flask, render_template, session, redirect, url_for, request
from lib.controllers.auth_controller import login, sign_up, logout

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
    return login()

@app.route('/index/sign_up', methods=['GET', 'POST'])
def sign_up_route():
    return sign_up()

@app.route('/index/logout')
def logout_route():
    return logout()

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