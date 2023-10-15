
from flask import Flask, render_template, request
from database.firebase import get_counter, increment_counter

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        if increment_counter(username):
            counter = get_counter(username)
            return render_template('result.html', username=username, counter=counter)
        else:
            return "Errore durante l'incremento del contatore."
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
