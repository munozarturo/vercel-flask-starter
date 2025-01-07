import logging

from typing import Any, Dict

from flask import Flask, Response, make_response, request

from api.middleware import requires_auth

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.get("/ping")
def ping() -> Response:
    data: Dict[str, Any] = {}

    return make_response({"status": "ok", "data": data}, 200)


@app.get("/secure/ping")
@requires_auth
def secure_ping() -> Response:
    data: Dict[str, Any] = {}

    return make_response({"status": "ok", "data": data}, 200)
