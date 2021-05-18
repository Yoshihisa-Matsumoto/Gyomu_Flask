import os

from gyomu.gyomu_db_model import GyomuAppsInfoCdtbl
import pytest
from gyomu.db_connection_factory import DbConnectionFactory, GYOMU_COMMON_MAINDB_CONNECTION
from gyomu_flask.app import create_app
from flask import Response
from http import HTTPStatus
from gyomu_flask.resources.gyomu_apps import gyomuapps_total_list_schema, gyomuapps_schema

from gyomu.json import Json

@pytest.fixture()
def environment_setup():
    original_setting = ""
    if GYOMU_COMMON_MAINDB_CONNECTION in os.environ:
        original_setting = os.environ[GYOMU_COMMON_MAINDB_CONNECTION]
    os.environ[GYOMU_COMMON_MAINDB_CONNECTION] = "postgresql://postgres:password@localhost:5432/gyomu"
    yield
    os.environ[GYOMU_COMMON_MAINDB_CONNECTION] = original_setting


@pytest.fixture
def app(environment_setup):
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

TEST_APPLICATION_ID2 = 32655
TEST_APPLICAIONT_ID_AMEND=32656

def test_newapp(client):
    response: Response = client.get('/apps')
    assert response.status_code==HTTPStatus.OK
    original_count = len(response.json)
    gyomu_app_list: list[GyomuAppsInfoCdtbl]
    if original_count > 0 :
        gyomu_app_list = Json.deserialize(response.data.decode(),GyomuAppsInfoCdtbl,gyomuapps_total_list_schema ) #gyomuapps_total_list_schema.load(response.json)
        gyomu_app = any(app for app in gyomu_app_list if app.application_id==TEST_APPLICATION_ID2)
        if gyomu_app is not None:
            response = client.delete('/apps/'+str(TEST_APPLICATION_ID2))
            assert response.status_code == HTTPStatus.OK

    gyomu_app = GyomuAppsInfoCdtbl()
    gyomu_app.application_id=TEST_APPLICATION_ID2
    gyomu_app.description = 'Test Application'
    gyomu_app.mail_from_address = 'mail@tost.com'
    gyomu_app.mail_from_name='Test person'
    response = client.post('/apps', json=Json.to_json(gyomu_app,gyomuapps_schema))
    print(response.data.decode())
    assert response.status_code == HTTPStatus.CREATED

    response = client.delete('/apps/' + str(TEST_APPLICATION_ID2))
    assert response.status_code == HTTPStatus.OK