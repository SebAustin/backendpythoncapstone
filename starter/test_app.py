import os
import unittest
import json
from app import create_app
from models import db, Actor, Movie
from datetime import date


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # Set test database URL before creating app
        self.database_name = "casting_test"
        self.database_path = "postgresql://shenry@localhost:5432/{}".format(
            self.database_name
        )
        os.environ['DATABASE_URL'] = self.database_path
        
        # Create app with test config
        self.app = create_app()
        self.client = self.app.test_client
        
        # JWT tokens for testing
        # Replace these with actual JWT tokens from Auth0
        self.casting_assistant_token = os.environ.get('CASTING_ASSISTANT_TOKEN', '')
        self.casting_director_token = os.environ.get('CASTING_DIRECTOR_TOKEN', '')
        self.executive_producer_token = os.environ.get('EXECUTIVE_PRODUCER_TOKEN', '')

        # Sample actor data
        self.new_actor = {
            'name': 'Tom Hanks',
            'age': 65,
            'gender': 'Male'
        }

        # Sample movie data
        self.new_movie = {
            'title': 'Forrest Gump',
            'release_date': '1994-07-06'
        }

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            # Clean up database
            db.session.query(Actor).delete()
            db.session.query(Movie).delete()
            db.session.commit()

    # ============================================================================
    # Helper Methods
    # ============================================================================

    def get_headers(self, token):
        """Helper method to create authorization headers"""
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    # ============================================================================
    # Actor Endpoint Tests - Success Behavior
    # ============================================================================

    def test_get_actors_success(self):
        """Test GET /actors with valid token"""
        # Create a test actor first
        with self.app.app_context():
            actor = Actor(**self.new_actor)
            actor.insert()

        res = self.client().get(
            '/actors',
            headers=self.get_headers(self.casting_assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']) > 0)

    def test_create_actor_success(self):
        """Test POST /actors with valid token"""
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], self.new_actor['name'])

    def test_update_actor_success(self):
        """Test PATCH /actors/<id> with valid token"""
        # Create a test actor first
        with self.app.app_context():
            actor = Actor(**self.new_actor)
            actor.insert()
            actor_id = actor.id

        updated_data = {'name': 'Tom Hanks Updated', 'age': 66}
        
        res = self.client().patch(
            f'/actors/{actor_id}',
            json=updated_data,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], updated_data['name'])

    def test_delete_actor_success(self):
        """Test DELETE /actors/<id> with valid token"""
        # Create a test actor first
        with self.app.app_context():
            actor = Actor(**self.new_actor)
            actor.insert()
            actor_id = actor.id

        res = self.client().delete(
            f'/actors/{actor_id}',
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], actor_id)

    # ============================================================================
    # Movie Endpoint Tests - Success Behavior
    # ============================================================================

    def test_get_movies_success(self):
        """Test GET /movies with valid token"""
        # Create a test movie first
        with self.app.app_context():
            movie = Movie(
                title=self.new_movie['title'],
                release_date=date.fromisoformat(self.new_movie['release_date'])
            )
            movie.insert()

        res = self.client().get(
            '/movies',
            headers=self.get_headers(self.casting_assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']) > 0)

    def test_create_movie_success(self):
        """Test POST /movies with valid token"""
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.get_headers(self.executive_producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_update_movie_success(self):
        """Test PATCH /movies/<id> with valid token"""
        # Create a test movie first
        with self.app.app_context():
            movie = Movie(
                title=self.new_movie['title'],
                release_date=date.fromisoformat(self.new_movie['release_date'])
            )
            movie.insert()
            movie_id = movie.id

        updated_data = {'title': 'Forrest Gump Updated'}
        
        res = self.client().patch(
            f'/movies/{movie_id}',
            json=updated_data,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['title'], updated_data['title'])

    def test_delete_movie_success(self):
        """Test DELETE /movies/<id> with valid token"""
        # Create a test movie first
        with self.app.app_context():
            movie = Movie(
                title=self.new_movie['title'],
                release_date=date.fromisoformat(self.new_movie['release_date'])
            )
            movie.insert()
            movie_id = movie.id

        res = self.client().delete(
            f'/movies/{movie_id}',
            headers=self.get_headers(self.executive_producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], movie_id)

    # ============================================================================
    # Error Behavior Tests
    # ============================================================================

    def test_get_actors_no_auth_header(self):
        """Test GET /actors without authorization header"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_actor_missing_data(self):
        """Test POST /actors with missing required fields"""
        incomplete_actor = {'name': 'John Doe'}
        
        res = self.client().post(
            '/actors',
            json=incomplete_actor,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_actor_not_found(self):
        """Test PATCH /actors/<id> with non-existent actor"""
        updated_data = {'name': 'Non Existent Actor'}
        
        res = self.client().patch(
            '/actors/999999',
            json=updated_data,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor_not_found(self):
        """Test DELETE /actors/<id> with non-existent actor"""
        res = self.client().delete(
            '/actors/999999',
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies_no_auth_header(self):
        """Test GET /movies without authorization header"""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_create_movie_missing_data(self):
        """Test POST /movies with missing required fields"""
        incomplete_movie = {'title': 'Incomplete Movie'}
        
        res = self.client().post(
            '/movies',
            json=incomplete_movie,
            headers=self.get_headers(self.executive_producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_update_movie_not_found(self):
        """Test PATCH /movies/<id> with non-existent movie"""
        updated_data = {'title': 'Non Existent Movie'}
        
        res = self.client().patch(
            '/movies/999999',
            json=updated_data,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie_not_found(self):
        """Test DELETE /movies/<id> with non-existent movie"""
        res = self.client().delete(
            '/movies/999999',
            headers=self.get_headers(self.executive_producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # ============================================================================
    # RBAC Tests - Casting Assistant
    # ============================================================================

    def test_casting_assistant_get_actors(self):
        """Test Casting Assistant can view actors"""
        with self.app.app_context():
            actor = Actor(**self.new_actor)
            actor.insert()

        res = self.client().get(
            '/actors',
            headers=self.get_headers(self.casting_assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_assistant_get_movies(self):
        """Test Casting Assistant can view movies"""
        with self.app.app_context():
            movie = Movie(
                title=self.new_movie['title'],
                release_date=date.fromisoformat(self.new_movie['release_date'])
            )
            movie.insert()

        res = self.client().get(
            '/movies',
            headers=self.get_headers(self.casting_assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_assistant_cannot_create_actor(self):
        """Test Casting Assistant cannot create actors"""
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.get_headers(self.casting_assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_casting_assistant_cannot_delete_actor(self):
        """Test Casting Assistant cannot delete actors"""
        with self.app.app_context():
            actor = Actor(**self.new_actor)
            actor.insert()
            actor_id = actor.id

        res = self.client().delete(
            f'/actors/{actor_id}',
            headers=self.get_headers(self.casting_assistant_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # ============================================================================
    # RBAC Tests - Casting Director
    # ============================================================================

    def test_casting_director_create_actor(self):
        """Test Casting Director can create actors"""
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_director_delete_actor(self):
        """Test Casting Director can delete actors"""
        with self.app.app_context():
            actor = Actor(**self.new_actor)
            actor.insert()
            actor_id = actor.id

        res = self.client().delete(
            f'/actors/{actor_id}',
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_director_update_movie(self):
        """Test Casting Director can update movies"""
        with self.app.app_context():
            movie = Movie(
                title=self.new_movie['title'],
                release_date=date.fromisoformat(self.new_movie['release_date'])
            )
            movie.insert()
            movie_id = movie.id

        updated_data = {'title': 'Updated Movie Title'}
        
        res = self.client().patch(
            f'/movies/{movie_id}',
            json=updated_data,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_casting_director_cannot_create_movie(self):
        """Test Casting Director cannot create movies"""
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_casting_director_cannot_delete_movie(self):
        """Test Casting Director cannot delete movies"""
        with self.app.app_context():
            movie = Movie(
                title=self.new_movie['title'],
                release_date=date.fromisoformat(self.new_movie['release_date'])
            )
            movie.insert()
            movie_id = movie.id

        res = self.client().delete(
            f'/movies/{movie_id}',
            headers=self.get_headers(self.casting_director_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    # ============================================================================
    # RBAC Tests - Executive Producer
    # ============================================================================

    def test_executive_producer_create_movie(self):
        """Test Executive Producer can create movies"""
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers=self.get_headers(self.executive_producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_executive_producer_delete_movie(self):
        """Test Executive Producer can delete movies"""
        with self.app.app_context():
            movie = Movie(
                title=self.new_movie['title'],
                release_date=date.fromisoformat(self.new_movie['release_date'])
            )
            movie.insert()
            movie_id = movie.id

        res = self.client().delete(
            f'/movies/{movie_id}',
            headers=self.get_headers(self.executive_producer_token)
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
