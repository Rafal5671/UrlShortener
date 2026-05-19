from flask import Blueprint, jsonify

errors_bp = Blueprint("api_errors", __name__)


@errors_bp.app_errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Not found"}), 404


@errors_bp.app_errorhandler(405)
def method_not_allowed(_error):
    return jsonify({"error": "Method not allowed"}), 405


@errors_bp.app_errorhandler(500)
def internal_error(_error):
    return jsonify({"error": "Internal server error"}), 500
