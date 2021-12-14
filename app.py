import csv
import requests
from faker import Faker
from flask import Flask, url_for, request, render_template


app: Flask = Flask(__name__)


@app.route('/index/')
@app.route('/')
def index():
    names = ['Requirements.txt', '100 Users', 'Hights and Weights', 'Astronauts']
    links = [url_for("reqs"), url_for("gen_usr"), url_for("mean"), url_for("astros")]

    return render_template('index.html', links=links, names=names)


@app.route('/requirements/')
def reqs():
    with open('requirements.txt') as requirements:
        content = requirements.readlines()

    return render_template('requirementstxt.html', content=content, back=url_for('index'))


@app.route('/generate-users/')
def gen_usr():
    amt = request.args.get(key='amt', default='100')
    user = Faker()
    users = list()
    for i in range(int(amt)):
        users.append(f'{user.name()} {user.email()}')

    return render_template('generate-users.html', content=users, back=url_for('index'))


@app.route('/mean/')
def mean():
    hights = list()
    weights = list()
    with open('hw.csv') as fooyle:
        rows = csv.reader(fooyle)
        for row in rows:
            try:
                hights.append(float(row[1]))
                weights.append(float(row[2]))
            except IndexError:
                continue
            except ValueError:
                continue
    avg_h = round(sum(hights) / len(hights) * 2.54, 1)
    avg_w = round(sum(weights) / len(weights) / 2.2046, 2)

    return render_template('mean.html', data=[avg_h, avg_w], back=url_for('index'))


@app.route('/space/')
def astros():
    r = requests.get('http://api.open-notify.org/astros.json')
    number = r.json()["number"]

    return render_template('astronauts.html', number=number, back=url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
