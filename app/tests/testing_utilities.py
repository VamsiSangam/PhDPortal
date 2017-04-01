from django.test import TestCase, Client
from django.contrib import auth
from app.views import logger

GET = "GET"
POST = "POST"
OTHER = "OTHER"
ALL = "ALL"
STATUS_CODE_OK = 200
STATUS_CODE_BAD_REQUEST = 400
STATUS_CODE_NOT_FOUND = 404
STATUS_CODE_UNAUTHORISED = 401
STATUS_CODE_FORBIDDEN = 403
STATUS_CODE_INTERNAL_SERVER_ERROR = 500
LOGIN_URL = "http://localhost:8000/"

def login(client, username, password):
    client.post('/', {'username' : username, 'password' : password})

def logout(client):
    client.get('/logout')