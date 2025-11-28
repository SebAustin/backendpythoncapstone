import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth
from datetime import datetime


def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
        )
        return response

    # Routes

    @app.route('/')
    def index():
        """Health check endpoint"""
        return jsonify({
            'success': True,
            'message': 'Casting Agency API is running!'
        })

    # ============================================================================
    # Actor Endpoints
    # ============================================================================

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        """
        GET /actors
            Public endpoint that requires the 'get:actors' permission
            Returns status code 200 and json {"success": True, "actors": actors}
                where actors is the list of actors
        """
        try:
            actors = Actor.query.order_by(Actor.id).all()
            
            if not actors:
                return jsonify({
                    'success': True,
                    'actors': []
                })

            formatted_actors = [actor.format() for actor in actors]

            return jsonify({
                'success': True,
                'actors': formatted_actors
            })

        except Exception:
            abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        """
        POST /actors
            Endpoint that requires the 'post:actors' permission
            Creates a new row in the actors table
            Returns status code 200 and json {"success": True, "actor": actor}
                where actor is the newly created actor
        """
        body = request.get_json()

        if not body:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        if not name or not age or not gender:
            abort(400)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        """
        PATCH /actors/<actor_id>
            Endpoint that requires the 'patch:actors' permission
            Updates the corresponding row for <actor_id>
            Returns status code 200 and json {"success": True, "actor": actor}
                where actor is the updated actor
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()

        if not body:
            abort(400)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except Exception:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        """
        DELETE /actors/<actor_id>
            Endpoint that requires the 'delete:actors' permission
            Deletes the corresponding row for <actor_id>
            Returns status code 200 and json {"success": True, "delete": actor_id}
                where actor_id is the id of the deleted actor
        """
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            })

        except Exception:
            abort(422)

    # ============================================================================
    # Movie Endpoints
    # ============================================================================

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        """
        GET /movies
            Public endpoint that requires the 'get:movies' permission
            Returns status code 200 and json {"success": True, "movies": movies}
                where movies is the list of movies
        """
        try:
            movies = Movie.query.order_by(Movie.id).all()
            
            if not movies:
                return jsonify({
                    'success': True,
                    'movies': []
                })

            formatted_movies = [movie.format() for movie in movies]

            return jsonify({
                'success': True,
                'movies': formatted_movies
            })

        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        """
        POST /movies
            Endpoint that requires the 'post:movies' permission
            Creates a new row in the movies table
            Returns status code 200 and json {"success": True, "movie": movie}
                where movie is the newly created movie
        """
        body = request.get_json()

        if not body:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if not title or not release_date:
            abort(400)

        try:
            # Convert string date to date object
            date_obj = datetime.strptime(release_date, '%Y-%m-%d').date()
            
            movie = Movie(title=title, release_date=date_obj)
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except ValueError:
            abort(400)
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        """
        PATCH /movies/<movie_id>
            Endpoint that requires the 'patch:movies' permission
            Updates the corresponding row for <movie_id>
            Returns status code 200 and json {"success": True, "movie": movie}
                where movie is the updated movie
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()

        if not body:
            abort(400)

        title = body.get('title', None)
        release_date = body.get('release_date', None)

        try:
            if title:
                movie.title = title
            if release_date:
                date_obj = datetime.strptime(release_date, '%Y-%m-%d').date()
                movie.release_date = date_obj

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except ValueError:
            abort(400)
        except Exception:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        """
        DELETE /movies/<movie_id>
            Endpoint that requires the 'delete:movies' permission
            Deletes the corresponding row for <movie_id>
            Returns status code 200 and json {"success": True, "delete": movie_id}
                where movie_id is the id of the deleted movie
        """
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            })

        except Exception:
            abort(422)

    # ============================================================================
    # Error Handlers
    # ============================================================================

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        """Handle 422 errors"""
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 errors"""
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        """Handle AuthError exceptions"""
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
