from flask import abort, jsonify, request
from flask.views import MethodView

# Dummy database to hold movie examples
movies = {
    "123": {"title": "Top Gun: Maverick", "description": "Fighter planes"},
    "456": {"title": "Sonic the Hedgehog", "description": "Blue Sega character"},
    "789": {"title": "A Quiet Place", "description": "Scary monsters"},
}


class Movies(MethodView):
    def get(self, movie_id):
        if movie_id is None:
            # Return a list of all movies
            return jsonify({"movies": [dict({"title": movie["title"]}, **{"id": i}) for i, movie in movies.items()]})
        else:
            # Return the details of a specific movie
            movie = movies.get(str(movie_id))
            if movie is None:
                abort(404)
            return jsonify({"movie": dict(movie, id=movie_id)})

    def post(self):
        payload = request.get_json(silent=True) or {}
        if not payload.get("title") or not payload.get("description"):
            abort(400, description="title and description are required")

        movie_id = str(max(map(int, movies), default=0) + 1)
        movies[movie_id] = {
            "title": payload["title"],
            "description": payload["description"],
        }
        return jsonify({"movie": dict(movies[movie_id], id=int(movie_id))}), 201

    def put(self, movie_id):
        key = str(movie_id)
        if key not in movies:
            abort(404)

        payload = request.get_json(silent=True) or {}
        movies[key].update({field: payload[field] for field in ("title", "description") if field in payload})
        return jsonify({"movie": dict(movies[key], id=movie_id)})

    def delete(self, movie_id):
        movie = movies.pop(str(movie_id), None)
        if movie is None:
            abort(404)
        return "", 204
