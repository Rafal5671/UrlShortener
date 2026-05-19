from flask import Blueprint, current_app, jsonify, request

from app.schemas import ShortURLResponse
from app.services import URLNotFoundError, URLService, URLValidationError

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _get_service() -> URLService:
    length = current_app.config.get("SHORT_CODE_LENGTH", 6)
    return URLService(short_code_length=length)


def _serialize(entry, base_url: str) -> dict:
    return ShortURLResponse.from_model(entry, base_url).to_dict()


@api_bp.post("/shorten")
def shorten():
    data = request.get_json(silent=True) or {}
    original_url = data.get("url", "")

    service = _get_service()
    try:
        entry, created = service.shorten(original_url)
    except URLValidationError as exc:
        return jsonify({"error": str(exc)}), 400

    base_url = current_app.config["BASE_URL"]
    status = 201 if created else 200
    return jsonify(_serialize(entry, base_url)), status


@api_bp.get("/info/<short_code>")
def info(short_code: str):
    service = _get_service()
    try:
        entry = service.get_by_code(short_code)
    except URLNotFoundError:
        return jsonify({"error": "Not found"}), 404

    base_url = current_app.config["BASE_URL"]
    return jsonify(_serialize(entry, base_url))
