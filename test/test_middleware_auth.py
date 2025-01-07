import sys
from pathlib import Path

from environ.vars import env

sys.path.insert(0, str(Path(__file__).parent.parent))

from http import HTTPStatus
from flask import Flask, jsonify

from api.middleware import require_auth

app = Flask(__name__)


@app.route("/test")
@require_auth
def test_endpoint():
    return jsonify({"status": "success"})


def test_require_auth():
    """Test the require_auth decorator with both valid and invalid auth"""
    client = app.test_client()

    response = client.get(
        "/test", headers={"Authorization": f"Bearer {env['API_KEY']}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.get_json()["status"] == "success"

    response = client.get("/test")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "No 'Authorization' header" in response.get_json()["message"]

    response = client.get("/test", headers={"Authorization": f"Basic {env['API_KEY']}"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Invalid Authorization header format" in response.get_json()["message"]

    response = client.get("/test", headers={"Authorization": "Bearer wrong_key"})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "Invalid API key" in response.get_json()["message"]
