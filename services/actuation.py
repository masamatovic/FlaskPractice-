from datetime import datetime

import pandas as pd

from models.main_units import UnitTypeName
from . import actuation_repository
from db import db


class Actuation:

    def __init__(self):
        pass

    @staticmethod
    def gel_all_actuations(client_id):

        actuations_query = actuation_repository.get_all_actuations(client_id)
        actuations_df = pd.read_sql(actuations_query.statement, db.session.bind)
        actuations = actuations_df.to_dict('records') if not actuations_df.empty else []

        return actuations

    @staticmethod
    def gel_all_actuations_by_name(actuation_type):

        metering_actuation_type = actuation_repository.get_metering_actuation_type_by_name(actuation_type)

        location_actuation_type = actuation_repository.get_location_actuation_type_by_name(actuation_type)

        if not metering_actuation_type and not location_actuation_type:
            raise ValueError(f"Unknown actuation type with name {actuation_type}.")

        metering_actuations = []
        location_actuations = []

        if metering_actuation_type:
            metering_actuation_type_query = actuation_repository.get_all_metering_actuation_by_actuation_type(
                actuation_type
            )
            metering_actuations_df = pd.read_sql(metering_actuation_type_query.statement, db.session.bind)
            metering_actuations = metering_actuations_df.to_dict('records') if not metering_actuations_df.empty else []

        if location_actuation_type:
            location_actuation_type_query = actuation_repository.get_all_location_actuation_by_actuation_type(
                actuation_type
            )
            location_actuations_df = pd.read_sql(location_actuation_type_query.statement, db.session.bind)
            location_actuations = location_actuations_df.to_dict('records') if not location_actuations_df.empty else []

        actuations = metering_actuations + location_actuations

        return actuations

    @staticmethod
    def insert_new_actuation(client_id: int, location_id: int, metering_id: int, actuation_type_id: int,
                             timestamp: datetime, value: float):

        if metering_id:
            actuation_type = actuation_repository.get_actuation_type_by_id(actuation_type_id, UnitTypeName.METERING)
        else:
            actuation_type = actuation_repository.get_actuation_type_by_id(actuation_type_id, UnitTypeName.LOCATION)

        if not actuation_type:
            raise ValueError(f"Unknown actuation type with id {actuation_type_id}.")

        new_actuation = actuation_repository.insert_actuation(
            client_id=client_id,
            location_id=location_id,
            metering_id=metering_id,
            actuation_type_id=actuation_type_id,
            timestamp=timestamp,
            value=value
        )

        return {
            "client_id": new_actuation.client_id,
            "location_id": new_actuation.location_id,
            "metering_id": new_actuation.metering_id if metering_id else 0,
            "actuation_type_id": new_actuation.actuation_type_id,
            "timestamp": new_actuation.timestamp,
            "value": value
        }

    @staticmethod
    def update_actuation(client_id: int, location_id: int, metering_id: int, actuation_type_id: int,
                         timestamp: datetime, value: float):

        if metering_id:
            actuation_type = actuation_repository.get_actuation_type_by_id(actuation_type_id, UnitTypeName.METERING)
        else:
            actuation_type = actuation_repository.get_actuation_type_by_id(actuation_type_id, UnitTypeName.LOCATION)

        if not actuation_type:
            raise ValueError(f"Unknown actuation type with id {actuation_type_id}.")

        actuation = actuation_repository.update_actuation(
            client_id=client_id,
            location_id=location_id,
            metering_id=metering_id,
            actuation_type_id=actuation_type_id,
            timestamp=timestamp,
            value=value
        )

        return {
            "client_id": actuation.client_id,
            "location_id": actuation.location_id,
            "metering_id": actuation.metering_id if metering_id else 0,
            "actuation_type_id": actuation.actuation_type_id,
            "timestamp": actuation.timestamp,
            "value": value
        }

    @staticmethod
    def delete_actuation(client_id: int, location_id: int, metering_id: int, actuation_type_id: int,
                         timestamp: datetime):

        actuation_repository.delete_actuation(
            client_id=client_id,
            location_id=location_id,
            metering_id=metering_id,
            actuation_type_id=actuation_type_id,
            timestamp=timestamp,
        )
