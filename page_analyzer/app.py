from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():  # put application's code here
    if request.method == 'GET':
        return render_template(
            'home.html',
        )


if __name__ == '__main__':
    app.run()
