from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    alias = db.Column(db.String(100), unique=True)

class GPS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey('point.id'))
    point_gps_id = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    speed = db.Column(db.Float)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, point_id, lat, lon, speed):
        self.point_id = point_id
        existing_gps_count = GPS.query.filter_by(point_id=point_id).count()
        self.point_gps_id = existing_gps_count + 1 if existing_gps_count > 0 else 1
        self.lat = lat
        self.lon = lon
        self.speed = speed

