"""This file will store the different web adresses you have, and works as a directory too look up the different parts
 of the application. This calls the @app.route function in flask, and checks for the input navigation keyword. Remember
 that if you dont place any redirection to a HTML file, the HTML file will not rendered*

 *There are ways of linking HTML files directly in text on other HTML files, but this is not recomended practice in
 flask """

from flask import render_template, request, jsonify
from app import app, db
from app.models import ViewPoint
from geopy.distance import vincenty


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


@app.route('/delete', methods=['DELETE', 'GET'])
def delete():
    vp = db.session.query(ViewPoint).filter(ViewPoint.title == "StuatilHaneberg").first()
    if type(vp) is ViewPoint:
        db.session.delete(vp)
        db.session.commit()
        return "Deleted"
    return "Could not find the view point in the database"


@app.route('/changeRating', methods=['GET'])
def changeRating():
    data = request.get_json()

    id = data["id"]
    rating = int(data['rating'])

    vp = db.session.query(ViewPoint).filter(ViewPoint.ID == id).first()

    if type(vp) is ViewPoint:
        numberOfRatings = vp.numberOfRatings + 1
        newRating = (vp.rating + rating)/numberOfRatings
        vp.numberOfRatings = numberOfRatings
        vp.rating = newRating
        db.session.commit()
        return jsonify({'rating': newRating})

    return jsonify({'completed': False})


@app.route('/postjson', methods=['POST'])
def post():
    """
    Function for inserting a new view point to the database
    :return: A json object telling the front-end that it was a sucsess
    """

    data = request.get_json()

    try:
        title = data["title"]
        lat = float(data["latitude"])
        long = float(data["longitude"])

        if data['image']:
            image = data["image"]
            print(len(image))
        else:
            image = None

        spot = ViewPoint(title=title, lat=lat, long=long, image=image)

        db.session.add(spot)
        db.session.commit()
        print("veiw point added to database")

        return jsonify({'completed': True})

    except:
        return jsonify({'completed': False})


@app.route('/viewPoints', methods=['GET'])
def upload_image():
    """
    Function for getting all view points in the database
    :return: a json object with all the view points
    """
    viewPoints = ViewPoint.query.all()

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), viewPoints))})


@app.route('/getViewPoint', methods=['POST'])
def getViewPoint():

    data = request.get_json()
    title = data["title"]
    vp = db.session.query(ViewPoint).filter(ViewPoint.title == title).first()

    if type(vp) is ViewPoint:
        return jsonify({"image": vp.image})

    return jsonify({"completed": False})


@app.route('/filterViewPoints', methods=['GET'])
def filterViewPionts():
    """
    Function for getting all view points within a custom radius from yourself
    :return: a json object with all the view points within the distance
    """
    data = request.get_json()

    radius = float(data["radius"])
    lat = float(data["latitude"])
    long = float(data["longitude"])

    currentCoordinate = (lat, long)
    viewPoints = ViewPoint.query.all()
    validViewPoints = []

    for vp in viewPoints:
        coordinateVP = (vp.lat, vp.long)

        if vincenty(currentCoordinate, coordinateVP).m <= radius:
            validViewPoints.append(vp)

    if len(validViewPoints) == 0:
        return jsonify({'completed': False})

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), validViewPoints))})


@app.route('/clusterViewPoints', methods=['GET'])
def clusterViewPoints():
    """
    Function that gets several View Points that are close to each other
    :return: a json object containing the view points that are close to each other
    """

    data = request.get_json()

    radius = float(data["radius"])
    lat = float(data["latitude"])
    long = float(data["longitude"])
    distance = float(data["distance"])

    currentCoordinate = (lat, long)
    viewPoints = ViewPoint.query.all()

    validViewPoints = []

    for vp in viewPoints:
        coordinateVP = (vp.lat, vp.long)

        if vincenty(currentCoordinate, coordinateVP).m <= radius + distance:
            validViewPoints.append(vp)

    if len(validViewPoints) == 0:
        return jsonify({'completed': False})

    bestSpot = None
    neighbours = []

    for spot in validViewPoints:
        closeSpots = []
        coordinateSpot = (spot.lat, spot.long)
        for n in validViewPoints:

            coordinateN = (n.lat, n.long)
            if spot.ID != n.ID and vincenty(coordinateSpot, coordinateN).m < distance:
                closeSpots.append(n)
        if len(closeSpots) >= len(neighbours):
            neighbours = closeSpots
            bestSpot = spot
    neighbours.append(bestSpot)

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), neighbours))})


@app.route('/distance', methods=['GET'])
def dist():
    viewPoints = ViewPoint.query.all()

    for vp in viewPoints:
        cooVP = (vp.lat, vp.long)
        for s in viewPoints:
            cooS = (s.lat, s.long)
            if s!=vp:
                print(vp.title)
                print(s.title)
                print(vincenty(cooS, cooVP).m)
                print("----------------------")

    return "hello"

