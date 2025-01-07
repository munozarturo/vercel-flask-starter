import logging

from jsonschema import validate, ValidationError

from typing import Callable, Optional

from functools import wraps
from flask import Response, jsonify, make_response, request
from http import HTTPStatus

from environ.vars import env

logger = logging.getLogger(__name__)


def requires_auth(f: Callable) -> Callable:
    @wraps(f)
    def decorator(*args, **kwargs) -> Response:
        auth_header: Optional[str] = request.headers.get("Authorization")

        if not auth_header:
            return make_response(
                jsonify({"status": "error", "message": "No 'Authorization' header."}),
                HTTPStatus.UNAUTHORIZED,
            )

        try:
            auth_type, api_key = auth_header.split(" ", 1)
            if auth_type.lower() != "bearer":
                raise ValueError("Invalid authorization type")
        except ValueError:
            return make_response(
                jsonify(
                    {
                        "status": "error",
                        "message": "Invalid Authorization header format. Use 'Bearer <api_key>'",
                    }
                ),
                HTTPStatus.UNAUTHORIZED,
            )

        if api_key != env["API_KEY"]:
            return make_response(
                jsonify(
                    {
                        "status": "error",
                        "message": "Invalid API key",
                    }
                ),
                HTTPStatus.UNAUTHORIZED,
            )

        return f(*args, **kwargs)

    return decorator


def validate_request_body(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if not request.is_json:
                    return (
                        jsonify({"error": "Content-Type must be application/json"}),
                        400,
                    )

                json_data = request.get_json()
                validate(instance=json_data, schema=schema)
                return f(*args, **kwargs)

            except ValidationError as e:
                return (
                    jsonify(
                        {"error": "Invalid request body", "details": str(e.message)}
                    ),
                    400,
                )

            except Exception as e:
                return (
                    jsonify({"error": "Internal server error", "details": str(e)}),
                    500,
                )

        return decorated_function

    return decorator
