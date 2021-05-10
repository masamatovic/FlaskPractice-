from datetime import datetime

from sqlalchemy import func, null, desc

from db import db
from models.actuations import MeteringActuation, LocationActuation, MeteringActuationType, LocationActuationType
from models.main_units import UnitTypeName


class ActuationRepository:

    @staticmethod
    def insert_actuation(client_id: int, location_id: int, metering_id: int, actuation_type_id: int,
                         timestamp: datetime, value: float):

        if metering_id:
            new_actuation = MeteringActuation()
            new_actuation.metering_id = metering_id
        else:
            new_actuation = LocationActuation()

        new_actuation.client_id = client_id
        new_actuation.location_id = location_id
        new_actuation.actuation_type_id = actuation_type_id
        new_actuation.timestamp = timestamp
        new_actuation.value = value

        try:
            db.session.add(new_actuation)
            db.session.commit()
            return new_actuation
        except Exception as e:
            db.session.rollback()
            db.session.flush()
            raise RuntimeError(
                f'Unable to create actuation for {client_id}, {location_id}, {metering_id},'
                f'with timestamp {str(timestamp)} and value {str(value)}.'
            )

    def update_actuation(self, client_id: int, location_id: int, metering_id: int, actuation_type_id: int,
                         timestamp: datetime, value: float):

        existing_actuation = self.get_actuation_by_pkey(
            client_id=client_id,
            location_id=location_id,
            metering_id=metering_id,
            actuation_type_id=actuation_type_id,
            timestamp=timestamp
        )

        if not existing_actuation:
            raise ValueError(f"Actuation does not exist")

        existing_actuation.actuation_type_id = actuation_type_id
        existing_actuation.timestamp = timestamp
        existing_actuation.value = value

        try:
            db.session.commit()
            return existing_actuation
        except:
            db.session.rollback()
            db.session.flush()
            raise RuntimeError("Unable to update")

    def delete_actuation(self, client_id: int, location_id: int, metering_id: int, actuation_type_id: int,
                         timestamp: datetime):

        existing_actuation = self.get_actuation_by_pkey(
            client_id=client_id,
            location_id=location_id,
            metering_id=metering_id,
            actuation_type_id=actuation_type_id,
            timestamp=timestamp
        )

        if not existing_actuation:
            raise ValueError(f"Actuation does not exist")

        try:
            db.session.delete(existing_actuation)
            db.session.commit()
            return existing_actuation
        except:
            db.session.rollback()
            db.session.flush()
            raise RuntimeError("Unable to delete")

    @staticmethod
    def get_actuation_by_pkey(client_id: int, location_id: int, metering_id: int, actuation_type_id: int,
                              timestamp: datetime):

        if metering_id:
            metering_actuation_query = db.session.query(
                MeteringActuation
            ).filter(
                MeteringActuation.client_id == client_id,
                MeteringActuation.location_id == location_id,
                MeteringActuation.metering_id == metering_id,
                MeteringActuation.actuation_type_id == actuation_type_id,
                MeteringActuation.timestamp == timestamp
            )

            return metering_actuation_query.first()
        else:
            location_actuation_query = db.session.query(
                LocationActuation
            ).filter(
                LocationActuation.client_id == client_id,
                LocationActuation.location_id == location_id,
                LocationActuation.actuation_type_id == actuation_type_id,
                LocationActuation.timestamp == timestamp
            )

            return location_actuation_query.first()

    @staticmethod
    def get_all_actuations(client_id):
        location_actuation_query = db.session.query(
            LocationActuation.client_id.label("client_id"),
            LocationActuation.location_id.label("location_id"),
            func.coalesce(0, null()).label("metering_id"),
            LocationActuation.timestamp.label("timestamp"),
            LocationActuation.actuation_type_id.label("actuation_type_id"),
            LocationActuation.value.label("value")
        ).filter(
            LocationActuation.client_id == client_id
        )

        metering_actuation_query = db.session.query(
            MeteringActuation.client_id.label("client_id"),
            MeteringActuation.location_id.label("location_id"),
            MeteringActuation.metering_id.label("metering_id"),
            MeteringActuation.timestamp.label("timestamp"),
            MeteringActuation.actuation_type_id.label("actuation_type_id"),
            MeteringActuation.value.label("value")
        ).filter(
            MeteringActuation.client_id == client_id
        )

        all_actuations_query = location_actuation_query.union(metering_actuation_query).order_by(desc("timestamp"))

        return all_actuations_query

    @staticmethod
    def get_actuation_type_by_id(actuation_type_id: int, unit_type: UnitTypeName):
        if unit_type == UnitTypeName.METERING:
            actuation_table = MeteringActuationType
        else:
            actuation_table = LocationActuationType

        actuation_type = actuation_table.query.filter_by(id=actuation_type_id).first()
        return actuation_type

    @staticmethod
    def get_metering_actuation_type_by_name(actuation_type_name: str):
        actuation_type = MeteringActuationType.query.filter_by(actuation_type=actuation_type_name).first()

        return actuation_type

    @staticmethod
    def get_location_actuation_type_by_name(actuation_type_name: str):
        actuation_type = LocationActuationType.query.filter_by(actuation_type=actuation_type_name).first()

        return actuation_type

    @staticmethod
    def get_all_metering_actuation_by_actuation_type(actuation_type):
        metering_actuation_query = db.session.query(
            MeteringActuation.client_id.label("client_id"),
            MeteringActuation.location_id.label("location_id"),
            MeteringActuation.metering_id.label("metering_id"),
            MeteringActuation.timestamp.label("timestamp"),
            MeteringActuation.actuation_type_id.label("actuation_type_id"),
            MeteringActuation.value.label("value"),
            MeteringActuationType.actuation_type.label("actuation_type_name")
                                                    ).join(
            MeteringActuationType, MeteringActuation.actuation_type_id == MeteringActuationType.id
            ).filter(
            MeteringActuationType.actuation_type == actuation_type
        )
        return metering_actuation_query

    @staticmethod
    def get_all_location_actuation_by_actuation_type(actuation_type):
        location_actuation_query = db.session.query(
            LocationActuation.client_id.label("client_id"),
            LocationActuation.location_id.label("location_id"),
            func.coalesce(0, null()).label("metering_id"),
            LocationActuation.timestamp.label("timestamp"),
            LocationActuation.actuation_type_id.label("actuation_type_id"),
            LocationActuation.value.label("value"),
            LocationActuationType.actuation_type.label("actuation_type_name")
                                                    ).join(
            LocationActuationType, LocationActuation.actuation_type_id == LocationActuationType.id
        ).filter(
            LocationActuationType.actuation_type == actuation_type
        )
        return location_actuation_query
