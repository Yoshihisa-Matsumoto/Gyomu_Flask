from flask import request,jsonify
from flask_restful import Resource
from http import HTTPStatus
from gyomu.gyomu_db_model import GyomuAppsInfoCdtbl
from gyomu.gyomu_db_schema import GyomuAppsSchema
from gyomu.gyomu_db_access import GyomuAppsInfoCdtblAccess, gyomuapps_schema
from gyomu.db_connection_factory import DbConnectionFactory
import gyomu.gyomu_db_access
from gyomu.json import Json
from marshmallow import ValidationError


import os

gyomuapps_total_list_schema = GyomuAppsSchema(many=True)
gyomuapps_summary_list_schema = GyomuAppsSchema(many=True, only=('application_id','description'))


def get_app_from_request() -> GyomuAppsInfoCdtbl :
    json_data = request.json
    return Json.deserialize(json_data,GyomuAppsInfoCdtbl,gyomuapps_schema)
    # data = gyomuapps_schema.loads(json_data)
    #
    # gyomu_app = GyomuAppsInfoCdtbl(**data)
    # return gyomu_app


class GyomuAppListResource(Resource):
    def get(self):
        gyomuapps_list, return_value = GyomuAppsInfoCdtblAccess.get_all()
        if not return_value.is_success:
            return {'message':'fail to retrieve application list'}, HTTPStatus.INTERNAL_SERVER_ERROR
        if len(gyomuapps_list)==0:
            return [], HTTPStatus.OK
        #return Json.to_json(gyomuapps_list), HTTPStatus.OK
        return gyomuapps_total_list_schema.dump(gyomuapps_list), HTTPStatus.OK

    def post(self):
        gyomu_app = get_app_from_request()
        check_app , return_value =GyomuAppsInfoCdtblAccess.get(gyomu_app.application_id)
        if not return_value.is_success:
            return {'message': 'application fails to be retrieved'}, HTTPStatus.INTERNAL_SERVER_ERROR
        if check_app is not None:
            return {'message': 'application id already used'}, HTTPStatus.BAD_REQUEST
        try:
            gyomu_app, return_value= GyomuAppsInfoCdtblAccess.add(gyomu_app)
            if not return_value.is_success:
                return {'message': 'application fails to be retrieved'}, HTTPStatus.INTERNAL_SERVER_ERROR
            return Json.to_json(gyomu_app,gyomuapps_schema), HTTPStatus.CREATED
        except:
            return {'message': 'Application addition returns error'}, HTTPStatus.INTERNAL_SERVER_ERROR


class GyomuAppListSummaryResource(Resource):
    def get(self):
        gyomuapps_list, return_value = GyomuAppsInfoCdtblAccess.get_all()
        if not return_value.is_success:
            return {'message':'fail to retrieve application list'}, HTTPStatus.INTERNAL_SERVER_ERROR
        if len(gyomuapps_list)==0:
            return [], HTTPStatus.OK
        #return Json.to_json(gyomuapps_list), HTTPStatus.OK
        return gyomuapps_summary_list_schema.dump(gyomuapps_list), HTTPStatus.OK


class GyomuAppResource(Resource):
    def delete(self, application_id):
        gyomu_app, return_value =GyomuAppsInfoCdtblAccess.get(application_id)
        if not return_value.is_success:
            return {'message': 'target application fail to retrieve'}, HTTPStatus.BAD_REQUEST
        if gyomu_app is None:
            return {'message': 'application id does not exist'}, HTTPStatus.BAD_REQUEST
        return_value = GyomuAppsInfoCdtblAccess.delete(gyomu_app)
        if not return_value.is_success:
            return {'message': 'fail to delete application'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return {}, HTTPStatus.OK

    def put(self, application_id):
        app = get_app_from_request()
        # json_data = request.get_json()
        if app is None:
            return {'message': 'update fails due to incorrect data'}, HTTPStatus.BAD_REQUEST

        return_value = GyomuAppsInfoCdtblAccess.update(app,original_application_id=application_id)
        if not return_value.is_success:
            return {'message': 'fail to delete application'}, HTTPStatus.INTERNAL_SERVER_ERROR
        return Json.to_json(app,gyomuapps_schema), HTTPStatus.OK