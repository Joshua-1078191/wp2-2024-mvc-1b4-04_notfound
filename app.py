from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index-1.html.jinja")

@app.route('/import', methods=['GET', 'POST'])
def import_questions():
    return render_template("questions/import_questions.html.jinja")

@app.route('/index', methods=['GET', 'POST'])
def index_questions_prompt():
    if request.method == 'POST':
        return redirect(url_for('index') + '/1')
    return render_template("questions/index_questions_prompt.html.jinja")

@app.route('/index/<int:prompt_id>', methods=['GET', 'POST'])
def index_questions_taxonomy(prompt_id:int):
    return render_template("questions/index_questions_taxonomy.html.jinja")

@app.route('/prompts/add_prompt', methods=['GET', 'POST'])
def add_prompt():
    return render_template("prompts/add_prompt.html.jinja")

@app.route('/prompts/prompt_details/<int:prompt_id>', methods=['GET', 'POST'])
def prompt_details(prompt_id:int):
    prompts = [{
        prompt_id: 1,
        "prompt_naam" : "Jorik's prompt",
        "redacteur" : "Jorik",
        "creation_date" : "02-02-2002",
        "categorised_questions" : 200,
        "correct_questions" : 180,
        "incorrect_questions" : 20,
    }]
    return render_template("prompts/prompt_details.html.jinja", prompts = prompts)

@app.route('/prompts/prompts_view', methods=['GET', 'POST'])
def prompts_view():
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
    return render_template("prompts/prompts_view.html.jinja", prompts = prompts)

@app.route('/questions/toetsvragen_view/<int:prompt_id>', methods=['GET', 'POST'])
def toetsvragen_view(prompt_id:int):
    questions = [{
        "prompt" : "prompt ....",
        "id" : 1,
        "question_name" : "vraag 1",
        "subject" : "Biologie",
        "school_grade" : "Havo 3",
        "creation_date" : "14-7-2020",
        "answered_correctly" : True,
    }]
    return render_template("prompts/toetsvragen_view.html.jinja", questions = questions)

# @app.route('/index/login', methods=['GET', 'POST'])
# def toetsvragen_view():
#     return render_template("login.html.jinja")

# @app.route('/index/sign_up', methods=['GET', 'POST'])
# def toetsvragen_view():
#     return render_template("sign_up.html.jinja")

# @app.route('/index/vragen', methods=['GET', 'POST'])
# def toetsvragen_view():
#     return render_template("vragen.html.jinja")

if __name__ == '__main__':
    app.run(debug=True)