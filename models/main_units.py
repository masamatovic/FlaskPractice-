import enum

from db import db


class UnitTypeName(str, enum.Enum):

    LOCATION = "LOCATION"
    METERING = "METERING"
    SUBMETERING = "SUBMETERING"


class Client(db.Model):
    """
    Clients
    """

    __tablename__ = 'client'
    __tableargs__ = {'schema': 'public'}

    id = db.Column(db.INTEGER(), primary_key=True, default=db.Sequence("client_id_seq"))
    name = db.Column(db.TEXT())
    code = db.Column(db.VARCHAR(length=10))
    headquarters_location = db.Column(db.TEXT())
    contact = db.Column(db.TEXT())
    about = db.Column(db.TEXT())
    energy_unit = db.Column(db.VARCHAR(length=10))
    currency = db.Column(db.VARCHAR(length=3))


class Location(db.Model):
    """
    Locations
    """

    __tablename__ = 'location'
    __tableargs__ = {'schema': 'public'}

    client_id = db.Column(db.INTEGER(), primary_key=True, default=db.Sequence("client_id_seq"))
    location_id = db.Column(db.INTEGER(), primary_key=True, default=db.Sequence("location_location_id_seq"))
    name = db.Column(db.TEXT())
    facility = db.Column(db.VARCHAR(length=100))
    region = db.Column(db.TEXT())
    tariff = db.Column(db.VARCHAR(length=20))
    muncipality = db.Column(db.VARCHAR(length=100))
    monitor = db.Column(db.BOOLEAN())
    control = db.Column(db.BOOLEAN())
    show = db.Column(db.BOOLEAN())
    latitude = db.Column(db.FLOAT())
    longitude = db.Column(db.FLOAT())
    solar_orientation = db.Column(db.VARCHAR(length=2))
    winter_climatic_zone = db.Column(db.VARCHAR(length=10))
    summer_climatic_zone = db.Column(db.VARCHAR(length=10))


class Metering(db.Model):
    """
    Metering
    """

    __tablename__ = 'metering'
    __tableargs__ = {'schema': 'public'}

    client_id = db.Column(db.INTEGER(), primary_key=True, default=db.Sequence("client_id_seq"))
    location_id = db.Column(db.INTEGER(), primary_key=True, default=db.Sequence("location_location_id_seq"))
    metering_id = db.Column(db.INTEGER(), primary_key=True, default=db.Sequence("metering_metering_id_seq"))
    name = db.Column(db.TEXT())
    contracted_power_kw = db.Column(db.FLOAT())
