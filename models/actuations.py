from db import db


class MeteringActuation(db.Model):

    __tablename__ = 'metering_actuation'
    __tableargs__ = {'schema': 'public'}

    client_id = db.Column(db.INTEGER(), primary_key=True)
    location_id = db.Column(db.INTEGER(), primary_key=True)
    metering_id = db.Column(db.INTEGER(), primary_key=True)
    actuation_type_id = db.Column(db.INTEGER(), primary_key=True)
    timestamp = db.Column(db.DateTime(), primary_key=True)
    value = db.Column(db.Float())


class MeteringActuationType(db.Model):

    __tablename__ = 'metering_actuation_type'
    __tableargs__ = {'schema': 'public'}

    id = db.Column(db.INTEGER(), primary_key=True)
    actuation_type = db.Column(db.TEXT())


class LocationActuation(db.Model):

    __tablename__ = 'location_actuation'
    __tableargs__ = {'schema': 'public'}

    client_id = db.Column(db.INTEGER(), primary_key=True)
    location_id = db.Column(db.INTEGER(), primary_key=True)
    actuation_type_id = db.Column(db.INTEGER(), primary_key=True)
    timestamp = db.Column(db.DateTime(), primary_key=True)
    value = db.Column(db.Float())


class LocationActuationType(db.Model):

    __tablename__ = 'location_actuation_type'
    __tableargs__ = {'schema': 'public'}

    id = db.Column(db.INTEGER(), primary_key=True)
    actuation_type = db.Column(db.TEXT())