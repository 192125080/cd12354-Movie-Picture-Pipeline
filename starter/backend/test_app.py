from . import app
import os


def test_movies_endpoint_returns_200():
    with app.test_client() as client:
        status_code = os.getenv("FAIL_TEST", 200)
        response = client.get("/movies/")
        assert response.status_code == status_code


def test_movies_endpoint_returns_json():
    with app.test_client() as client:
        response = client.get("/movies/")
        assert response.content_type == "application/json"


def test_movies_endpoint_returns_valid_data():
    with app.test_client() as client:
        response = client.get("/movies/")
        data = response.get_json()
        assert isinstance(data, dict)
        assert "movies" in data
        assert isinstance(data.get("movies"), list)
        assert len(data["movies"]) > 0
        assert "title" in data["movies"][0]


def test_required_routes_are_available():
    with app.test_client() as client:
        assert client.get("/").status_code == 200
        assert client.get("/movies/123").status_code == 200
        response = client.post("/movies", json={"title": "New", "description": "A movie"})
        movie_id = response.get_json()["movie"]["id"]
        assert response.status_code == 201
        assert client.put(f"/movies/{movie_id}", json={"title": "Updated"}).status_code == 200
        assert client.delete(f"/movies/{movie_id}").status_code == 204
