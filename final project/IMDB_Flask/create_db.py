# %%
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship, sessionmaker
import pandas as pd

# %%
# Define the base for models
Base = declarative_base()

# Define the relationships
movie_actors = Table('movie_actors', Base.metadata,
                     Column('movie_id', Integer, ForeignKey('movie.id')),
                     Column('actor_id', Integer, ForeignKey('actor.id')))

movie_directors = Table('movie_directors', Base.metadata,
                        Column('movie_id', Integer, ForeignKey('movie.id')),
                        Column('director_id', Integer, ForeignKey('director.id')))

director_actors = Table('director_actors', Base.metadata,
                        )

# Define models
class Movie(Base):
    __tablename__ = 'movie'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime)
    average_rating = Column(Float)
    genre = Column(String)
    duration = Column(String)
    gross_earnings = Column(String)
    image = Column(String)
    actors = relationship('Actor', secondary=movie_actors, back_populates='movies')
    directors = relationship('Director', secondary=movie_directors, back_populates='movies')
    PrimaryKeyConstraint('id')
    
    
class Actor(Base):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    actor = Column(Boolean, default=True)
    movies = relationship('Movie', secondary=movie_actors, back_populates='actors')
    
    PrimaryKeyConstraint('id')
    
class Director(Base):
    __tablename__ = 'director'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    director = Column(Boolean, default=True)
    movies = relationship('Movie', secondary=movie_directors, back_populates='directors')
    PrimaryKeyConstraint('id')
    
# %%

# Database setup
engine = create_engine('sqlite:///movies.db')  # Replace with your actual database URI
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# %%
data = pd.read_csv('imdb.csv')
data.head()
# %%
try:
    for _, row in data.iterrows():
        
        if not pd.notna(row['Movie_title']):
            continue
            
        if pd.notna(row['Year']):
            release_date = datetime.strptime(str(row['Year']),'%Y')
        else:
            release_date = datetime.now()  # Handle missing or malformed dates
            
        try:
            average_rating = float(row['IMDB Rating'])
        except ValueError:
            average_rating = None  # Default or error handling for invalid data
            
        if pd.notna(row['Genre']):
            genre=row['Genre']
        else:
            genre = None  # Handle missing or malformed dates
            
        if pd.notna(row['Duration']):
            duration=row['Duration']
        else:
            duration = None  # Handle missing or malformed dates
            
        if pd.notna(row['Gross earnings']):
            gross_earnings=row['Gross earnings']
        else:
            gross_earnings = None  # Handle missing or malformed dates
            
        movie = Movie(title=row['Movie_title'], 
                    release_date=release_date,
                    average_rating=average_rating,
                    genre=genre, 
                    duration=duration,
                    gross_earnings=gross_earnings,
                    image=row['Images'])
        
        director_names = row['Director'].split(', ')
        for name in director_names:
            director = session.query(Director).filter_by(name=name).first()
            if not director:
                director = Director(name=name)
            movie.directors.append(director)
        
        actors_list = eval(row['Actors'])
        for name in actors_list:
            actor = session.query(Actor).filter_by(name=name).first()
            if not actor:
                actor = Actor(name=name)
            movie.actors.append(actor)
        session.add(movie)

    session.commit()
except Exception as e:
    print(f"An error occurred: {e}")
    session.rollback()  
    
movies_in_db = session.query(Movie).count()
actors_in_db = session.query(Actor).count()
directors_in_db = session.query(Director).count()
# %%
session.close()
