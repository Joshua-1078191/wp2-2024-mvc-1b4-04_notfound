from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def main():
    return ""#render_template("index-1.html")

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

@app.route('/index/lijst_redacteuren', methods=['GET', 'POST'])
def lijst_redacteuren():
    return render_template("lijst_redacteuren.html.jinja")

@app.route('/index/nieuwe_redacteur', methods=['GET', 'POST'])
def nieuwe_redacteuren():
    return render_template("nieuwe_redacteur.html.jinja")

@app.route('/index/redacteur_wijzigen', methods=['GET', 'POST'])
def redacteur_wijzigen():
    return render_template("redacteur_wijzigen.html.jinja")

if __name__ == '__main__':
    app.run(debug=True)