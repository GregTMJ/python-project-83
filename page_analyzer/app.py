import os

from dotenv import load_dotenv
from flask import Flask, request, render_template

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def homepage():  # put application's code here
    if request.method == 'GET':
        return render_template(
            'home.html',
        )


if __name__ == '__main__':
    app.run(host=os.getenv('HOST'),
            port=os.getenv('PORT'))
