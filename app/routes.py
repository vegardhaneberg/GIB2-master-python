"""This file will store the different web adresses you have, and works as a directory too look up the different parts
 of the application. This calls the @app.route function in flask, and checks for the input navigation keyword. Remember
 that if you dont place any redirection to a HTML file, the HTML file will not rendered*

 *There are ways of linking HTML files directly in text on other HTML files, but this is not recomended practice in
 flask """

from flask import render_template, request, jsonify
from app import app, db
from app.models import ViewPoint, ViewPointInfo
from geopy.distance import vincenty
import base64


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/finish', methods=['POST'])
def finish():
    lat = request.form['lat']
    long = request.form['long']
    title = request.form['title']
    viewPointType = request.form['type']

    vp = ViewPoint(title=title, lat=lat, long=long, type=viewPointType)

    db.session.add(vp)
    db.session.commit()

    return "Done"


@app.route('/deleteAll', methods=['DELETE'])
def deleteAll():
    i = db.session.query(ViewPoint).delete()
    db.session.commit()
    return str(i)

@app.route('/delete', methods=['DELETE', 'GET'])
def delete():
    vp = db.session.query(ViewPoint).filter(ViewPoint.ID == 70).first()
    if type(vp) is ViewPoint:
        db.session.delete(vp)
        db.session.commit()
        return "Deleted"
    return "Could not find the view point in the database"


@app.route('/changeRating', methods=['PUT'])
def changeRating():
    data = request.get_json()

    id = data["id"]
    rating = int(data['rating'])

    vp = db.session.query(ViewPoint).filter(ViewPoint.ID == id).first()

    if type(vp) is ViewPoint:
        numberOfRatings = vp.numberOfRatings + 1
        newRating = (vp.rating * (numberOfRatings-1) + rating)/numberOfRatings
        vp.numberOfRatings = numberOfRatings
        vp.rating = newRating
        db.session.commit()
        vp.rating = int(round(vp.rating, 0))
        return jsonify({
            'rating': vp.rating,
            'numberOfRatings': vp.numberOfRatings
        })

    return jsonify({'completed': False})


@app.route('/postjson', methods=['POST'])
def postjson():
    """
    Function for inserting a new view point to the database
    :return: A json object telling the front-end that it was a sucsess
    """

    data = request.get_json()


    title = data["title"]
    lat = float(data["latitude"])
    long = float(data["longitude"])
    viewPointType = data['type']

    if data['image']:
        image = data["image"]
    else:
        image = None

    spot = ViewPoint(title=title, lat=lat, long=long, image=image, type=viewPointType)

    db.session.add(spot)
    db.session.commit()

    return jsonify({'completed': True})


@app.route('/viewPoints', methods=['GET'])
def upload_image():
    """
    Function for getting all view points in the database
    :return: a json object with all the view points
    """
    viewPoints = ViewPoint.query.all()

    for vp in viewPoints:
        if vp.rating is not None:
            vp.rating = int(round(vp.rating, 0))
        else:
            vp.rating = 0

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), viewPoints))})


@app.route('/getViewPoint', methods=['POST'])
def getViewPoint():

    data = request.get_json()
    id = int(data['id'])
    vp = db.session.query(ViewPoint).filter(ViewPoint.ID == id).first()

    if type(vp) is ViewPoint:
        vp.rating = int(round(vp.rating, 0))
        return jsonify(vp.serialize())

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


@app.route('/clusterViewPoints', methods=['POST'])
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

    type = data['type']

    currentCoordinate = (lat, long)
    viewPoints = ViewPoint.query.all()

    validViewPoints = []

    for vp in viewPoints:
        coordinateVP = (vp.lat, vp.long)
        if type == "Godt og blandet":
            if vincenty(currentCoordinate, coordinateVP).km <= radius + distance:
                validViewPoints.append(vp)
        else:
            if vincenty(currentCoordinate, coordinateVP).km <= radius + distance and type == vp.type:
                validViewPoints.append(vp)

    if len(validViewPoints) == 0:
        return jsonify({'viewPoints': False})

    bestSpot = None
    neighbours = []

    for spot in validViewPoints:
        closeSpots = []
        coordinateSpot = (spot.lat, spot.long)
        for n in validViewPoints:

            coordinateN = (n.lat, n.long)
            if spot.ID != n.ID and vincenty(coordinateSpot, coordinateN).km < distance:
                closeSpots.append(n)
        if len(closeSpots) >= len(neighbours):
            neighbours = closeSpots
            bestSpot = spot
    neighbours.append(bestSpot)

    viewPointsInfo = []

    for v in neighbours:
        info = ViewPointInfo(ID=v.ID, type=v.type, title=v.title, numberOfRatings=v.numberOfRatings, rating=v.rating, lat=v.lat, long=v.long)
        viewPointsInfo.append(info)

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), viewPointsInfo))})


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


@app.route('/getViewPointInfo', methods=['GET'])
def getViewPointInfo():

    viewPoints = ViewPoint.query.all()
    viewPointsInfo = []

    for vp in viewPoints:
        v = ViewPointInfo(ID=vp.ID, type=vp.type, title=vp.title, numberOfRatings=vp.numberOfRatings, rating=vp.rating, lat=vp.lat, long=vp.long)
        viewPointsInfo.append(v)

    viewPointsInfo.sort(key=returnName, reverse=True)

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), viewPointsInfo))})


def returnName(vp):
    return vp.rating


@app.route('/getWalk', methods=['POST'])
def getWalk():
    data = request.get_json()

    radius = float(data["radius"])
    lat = float(data["latitude"])
    long = float(data["longitude"])
    rating = int(data["rating"])

    type = data['type']

    currentCoordinate = (lat, long)
    viewPoints = ViewPoint.query.all()

    walkingPoints = []

    for vp in viewPoints:
        vpCoordinate = (vp.lat, vp.long)
        if type == 'Godt og blandet':
            if vincenty(currentCoordinate, vpCoordinate) <= radius and vp.rating >= rating:
                walkingPoints.append(vp)
        else:
            if vincenty(currentCoordinate, vpCoordinate) <= radius and vp.rating >= rating and type == vp.type:
                walkingPoints.append(vp)

    infoPoints = []

    for v in walkingPoints:
        v = ViewPointInfo(ID=v.ID, type=v.type, title=v.title, numberOfRatings=v.numberOfRatings, rating=v.rating, lat=v.lat, long=v.long)
        infoPoints.append(v)

    if len(infoPoints) == 0:
        return jsonify({"viewPoints": False})

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), infoPoints))})


@app.route('/getType', methods=['POST'])
def getType():
    data = request.get_json()
    viewPointType = data['type']

    viewPoints = ViewPoint.query.all()

    returnViewPoints = []

    for vp in viewPoints:
        if vp.type == viewPointType:
            v = ViewPointInfo(ID=vp.ID, type=vp.viewPointType, title=vp.title, numberOfRatings=vp.numberOfRatings, rating=vp.rating, lat=vp.lat, long=vp.long)
            returnViewPoints.append(v)

    if len(returnViewPoints) == 0:
        return jsonify({'completed': False})

    return jsonify({"viewPoints": list(map(lambda vp: vp.serialize(), returnViewPoints))})
