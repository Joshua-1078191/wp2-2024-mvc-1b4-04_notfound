from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index-1.html")

@app.route('/import')
def import_questions():
    return render_template("questions/import_questions.html")

@app.route('/index')
def index_questions():
    return render_template("questions/index_questions.html")