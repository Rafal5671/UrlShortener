from flask import Blueprint, current_app, redirect, render_template

from app.services import URLNotFoundError, URLService

web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def index():
    base_url = current_app.config["BASE_URL"]
    return render_template("index.html", base_url=base_url)


@web_bp.get("/<short_code>")
def redirect_to_url(short_code: str):
    service = URLService(
        short_code_length=current_app.config.get("SHORT_CODE_LENGTH", 6)
    )
    try:
        entry = service.get_by_code(short_code)
    except URLNotFoundError:
        return render_template("404.html"), 404

    return redirect(entry.original_url, code=302)
