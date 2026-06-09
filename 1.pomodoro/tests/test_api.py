import pytest
from app import app as flask_app


@pytest.fixture
def client():
    """Flask テストクライアントを提供するフィクスチャ。"""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


class TestIndexRoute:
    """GET / エンドポイントのテスト。"""

    def test_returns_200(self, client):
        """GET / が HTTP 200 を返すこと。"""
        response = client.get("/")
        assert response.status_code == 200

    def test_content_type_is_html(self, client):
        """GET / のレスポンスが HTML であること。"""
        response = client.get("/")
        assert "text/html" in response.content_type

    def test_page_title_is_correct(self, client):
        """ページタイトルに「ポモドーロタイマー」が含まれること。"""
        response = client.get("/")
        assert "ポモドーロタイマー".encode() in response.data

    def test_page_contains_heading(self, client):
        """ページに h1 見出しが含まれること。"""
        response = client.get("/")
        assert b"<h1>" in response.data

    def test_stylesheet_link_exists(self, client):
        """ページに CSS スタイルシートのリンクが含まれること。"""
        response = client.get("/")
        assert b"style.css" in response.data

    def test_unknown_route_returns_404(self, client):
        """存在しないパスへのアクセスが 404 を返すこと。"""
        response = client.get("/not-found")
        assert response.status_code == 404
