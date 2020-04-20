"""This file will store the different web adresses you have, and works as a directory too look up the different parts
 of the application. This calls the @app.route function in flask, and checks for the input navigation keyword. Remember
 that if you dont place any redirection to a HTML file, the HTML file will not rendered*

 *There are ways of linking HTML files directly in text on other HTML files, but this is not recomended practice in
 flask """

from flask import render_template, request, jsonify
from app import app, db
from app.models import ViewPoint

UPLOAD_FOLDER = ''


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/finish', methods=['POST'])
def finish():
    lat = request.form['lat']
    long = request.form['long']
    title = request.form['title']

    vp = ViewPoint(title=title, lat=lat, long=long)

    db.session.add(vp)
    db.session.commit()

    return "Done"


@app.route('/<title>', methods=['DELETE', 'GET'])
def delete(title):
    vp = db.session.query(ViewPoint).filter(ViewPoint.title == title).first()
    db.session.delete(vp)
    db.session.commit()
    return "Deleted"


@app.route('/postjson', methods=['POST'])
def post():
    data = request.get_json()

    print(type(data))
    print(data)

    title = data["title"]
    lat = float(data["latitude"])
    long = float(data["longitude"])

    spot = ViewPoint(title=title, lat=lat, long=long)

    db.session.add(spot)
    db.session.commit()

    return jsonify({'completed': True})


@app.route('/viewPoints', methods=['GET'])
def upload_image():
    viewPoints = ViewPoint.query.all()

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), viewPoints))})


@app.route('/get', methods=['GET'])
def get():
    vp = ViewPoint.query.filter_by(title='Nidarosdomen').first()

    return jsonify(title=vp.title,
                   lat=vp.lat,
                   long=vp.long,
                   )


