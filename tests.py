import pytest

from app import create_app
from app.services import URLNotFoundError, URLService, URLValidationError
from config import CIConfig


@pytest.fixture()
def app():
    flask_app = create_app(CIConfig())
    with flask_app.app_context():
        yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def service(app):
    return URLService(short_code_length=6)


class TestURLService:
    def test_shorten_creates_new_entry(self, service):
        entry, created = service.shorten("https://google.com")
        assert created is True
        assert entry.original_url == "https://google.com"
        assert len(entry.short_code) == 6

    def test_shorten_returns_existing_for_duplicate(self, service):
        entry1, _ = service.shorten("https://google.com")
        entry2, created = service.shorten("https://google.com")
        assert created is False
        assert entry1.id == entry2.id

    def test_shorten_strips_whitespace(self, service):
        entry, _ = service.shorten("  https://google.com  ")
        assert entry.original_url == "https://google.com"

    def test_shorten_raises_for_empty_url(self, service):
        with pytest.raises(URLValidationError):
            service.shorten("")

    def test_shorten_raises_for_missing_scheme(self, service):
        with pytest.raises(URLValidationError):
            service.shorten("google.com")

    def test_shorten_raises_for_ftp_scheme(self, service):
        with pytest.raises(URLValidationError):
            service.shorten("ftp://files.example.com")

    def test_get_by_code_returns_entry(self, service):
        entry, _ = service.shorten("https://example.com")
        found = service.get_by_code(entry.short_code)
        assert found.id == entry.id

    def test_get_by_code_raises_for_missing(self, service):
        with pytest.raises(URLNotFoundError):
            service.get_by_code("doesnotexist")


class TestAPIShorten:
    def test_returns_201_for_new_url(self, client):
        res = client.post("/api/shorten", json={"url": "https://example.com"})
        assert res.status_code == 201
        data = res.get_json()
        assert "short_url" in data
        assert "short_code" in data

    def test_returns_200_for_existing_url(self, client):
        client.post("/api/shorten", json={"url": "https://example.com"})
        res = client.post("/api/shorten", json={"url": "https://example.com"})
        assert res.status_code == 200

    def test_returns_400_for_missing_url(self, client):
        res = client.post("/api/shorten", json={})
        assert res.status_code == 400

    def test_returns_400_for_invalid_url(self, client):
        res = client.post("/api/shorten", json={"url": "not-a-url"})
        assert res.status_code == 400

    def test_returns_400_for_empty_body(self, client):
        res = client.post("/api/shorten", content_type="application/json", data="")
        assert res.status_code == 400


class TestAPIInfo:
    def test_returns_info_for_existing_code(self, client):
        create_res = client.post("/api/shorten", json={"url": "https://example.com"})
        code = create_res.get_json()["short_code"]
        res = client.get(f"/api/info/{code}")
        assert res.status_code == 200
        assert res.get_json()["short_code"] == code

    def test_returns_404_for_missing_code(self, client):
        res = client.get("/api/info/nonexistent")
        assert res.status_code == 404


class TestRedirect:
    def test_redirects_to_original_url(self, client):
        create_res = client.post("/api/shorten", json={"url": "https://example.com"})
        code = create_res.get_json()["short_code"]
        res = client.get(f"/{code}", follow_redirects=False)
        assert res.status_code == 302
        assert res.headers["Location"] == "https://example.com"

    def test_returns_404_for_unknown_code(self, client):
        res = client.get("/unknowncode")
        assert res.status_code == 404
