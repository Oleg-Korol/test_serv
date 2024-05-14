from flask import request, jsonify
from srv.models import db, Point
from srv.models import GPS


def post_gps():
    data = request.json
    point_data = data.get('point')
    gps_data = data.get('gps')

    try:
        if 'point_id' in point_data:
            point_id = point_data.get('point_id')
        else:
            alias = point_data.get('alias')
            name = point_data.get('name')

            if name:
                existing_point = db.session.query(Point).filter_by(name=name).first()
            if alias and not existing_point:
                existing_point = db.session.query(Point).filter_by(alias=alias).first()

            if existing_point:
                point_id = existing_point.id
            else:
                new_point = Point(**point_data)
                db.session.add(new_point)
                db.session.flush()
                point_id = new_point.id

        new_gps = GPS(point_id=point_id, **gps_data)
        db.session.add(new_gps)
        db.session.commit()

        return jsonify({"message": "GPS data received and saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def get_gps():
    point_id = request.args.get('point_id', type=int)
    offset = request.args.get('offset', default=0, type=int)
    count = request.args.get('count', default=1, type=int)

    gps_data = db.session.query(GPS).filter_by(point_id=point_id).offset(offset).limit(count).all()


    result = [{
        "id": gps.id,
        "point_id": gps.point_id,
        "lat": gps.lat,
        "lon": gps.lon,
        "speed": gps.speed,
        "time": gps.time
    } for gps in gps_data]

    return jsonify(result)



