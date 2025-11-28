import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date

database_path = os.environ.get('DATABASE_URL', 'postgresql://shenry@localhost:5432/casting')

# Handle Render/Heroku postgres:// URL format
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


class Movie(db.Model):
    """
    Movie
    A persistent movie entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(180), nullable=False)
    release_date = Column(Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        """
        insert()
            inserts a new movie into the database
            the movie must have a unique title
            the movie must have a title and release_date
            EXAMPLE
                movie = Movie(title=req_title, release_date=req_release_date)
                movie.insert()
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates a movie in the database
            the movie must exist in the database
            EXAMPLE
                movie = Movie.query.filter(Movie.id == id).one_or_none()
                movie.title = 'New Title'
                movie.update()
        """
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes a movie from the database
            the movie must exist in the database
            EXAMPLE
                movie = Movie.query.filter(Movie.id == id).one_or_none()
                movie.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        format()
            returns a dictionary representation of the movie
        """
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%Y-%m-%d')
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model):
    """
    Actor
    A persistent actor entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(180), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        """
        insert()
            inserts a new actor into the database
            the actor must have a unique name
            the actor must have a name, age, and gender
            EXAMPLE
                actor = Actor(name=req_name, age=req_age, gender=req_gender)
                actor.insert()
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        update()
            updates an actor in the database
            the actor must exist in the database
            EXAMPLE
                actor = Actor.query.filter(Actor.id == id).one_or_none()
                actor.name = 'New Name'
                actor.update()
        """
        db.session.commit()

    def delete(self):
        """
        delete()
            deletes an actor from the database
            the actor must exist in the database
            EXAMPLE
                actor = Actor.query.filter(Actor.id == id).one_or_none()
                actor.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def format(self):
        """
        format()
            returns a dictionary representation of the actor
        """
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return json.dumps(self.format())
