import datetime
import os
import psycopg2
import requests

from dotenv import load_dotenv
from flask import Flask, request, render_template, g, \
    flash, redirect, url_for, abort
from psycopg2.extras import NamedTupleCursor

from page_analyzer.parser import page_parser
from page_analyzer.urls import validate, url_normalizer

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')
app.config['DEBUG'] = True if os.getenv('DEBUG') else False


def connect_db():
    """
    Connecting to database
    :return: connection itself
    """
    conn = psycopg2.connect(app.config['DATABASE_URL'])
    return conn


def get_db():
    """
    open database connection
    """
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_db()
    return g.postgres_db


def init_db():
    """
    Creating to database when app starts
    from using the database.sql file
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('database.sql', mode='r') as db_file:
            db.cursor().execute(db_file.read())
        db.commit()


@app.route('/', methods=['GET'])
def homepage():
    """
    Getting our homepage template
    """
    if request.method == 'GET':
        return render_template(
            'home.html'
        )


@app.route('/urls', methods=['GET', 'POST'])
def urls():
    """
    Handling the route urls, in case of GET method, we list
    our data, in case of POST method, we seek to check/add
    new data to database and reroute to url_details
    """
    if request.method == 'GET':
        conn = get_db()

        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                "SELECT * from urls order by id desc"
            )

            available_urls = cursor.fetchall()

            cursor.execute(
                "SELECT DISTINCT on (url_id) * from url_checks "
                "order by url_id desc, id desc"
            )

            checks = cursor.fetchall()

        conn.close()

        return render_template(
            'urls/main.html',
            data=list(zip(available_urls, checks)),
        )

    if request.method == 'POST':
        url: str = request.form.to_dict().get('url')

        errors = validate(url)

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template(
                'home.html',
                url_name=url
            ), 422

        url = url_normalizer(url)
        conn = get_db()

        with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:

            cursor.execute(
                "SELECT * from urls where name=(%s)", (url,)
            )
            fetched_data = cursor.fetchone()
            if fetched_data:
                url_id: int = fetched_data.id
                flash('Страница уже существует', 'info')

            else:
                cursor.execute(
                    "INSERT INTO urls "
                    "(name, created_at) "
                    "VALUES (%s, %s) RETURNING id;",
                    (url, datetime.datetime.now(),)
                )
                url_id: int = cursor.fetchone().id
                flash('Страница успешно добавлена', 'success')

        conn.commit()
        conn.close()

        return redirect(url_for('url_details', id=url_id)), 301


@app.route('/urls/<int:id>', methods=['GET'])
def url_details(id: int):
    """
    Shows details of every created url + shows the made checks
    :param id: url's id
    """
    conn = connect_db()

    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'SELECT * FROM urls where id=%s', (id,)
        )
        url = cursor.fetchone()

        if not url:
            abort(404)

    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'SELECT * from url_checks '
            'where url_id=%s order by id desc', (id,)
        )

        checks = cursor.fetchall()

    conn.close()

    return render_template(
        'urls/details.html',
        url=url,
        checks=checks
    )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def url_checks(id: int):
    """
    Creating url checks on different levels
    :param id: url's id
    """
    conn = connect_db()

    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'SELECT * from urls where id=%s', (id,)
        )
        url = cursor.fetchone()

    try:
        response = requests.get(url.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_details', id=id))

    page_content = response.text
    page_content = page_parser(page_content)

    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            'INSERT INTO url_checks (url_id, status_code, h1,'
            ' title, description, created_at) values '
            '(%s, %s, %s, %s, %s, %s)',
            (id, response.status_code, page_content.get('h1'),
             page_content.get('title'), page_content.get('description'),
             datetime.datetime.now(),)
        )
        flash('Страница успешно проверена', 'success')
    conn.commit()
    conn.close()

    return redirect(url_for('url_details', id=id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('error/500.html'), 500
