from flask import Flask, render_template, jsonify, request, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import json
import random
global graph

app = Flask(__name__)
# app.use_reloader = True
app.secret_key = '55344663'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/zhongyinjiao/Desktop/SI 507/final project/movies.db'
# # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class Movie_Actors(db.Model):
#     __tablename__ = 'movie_actors'
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
#     actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), primary_key=True)

# class Movie_Directors(db.Model):
#     __tablename__ = 'movie_directors'
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), primary_key=True)
#     director_id = db.Column(db.Integer, db.ForeignKey('director.id'), primary_key=True)

# class Director_Actors(db.Model):
    


# class Movie(db.Model):
#     __tablename__ = 'movie'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable=False)
#     release_date = db.Column(db.DateTime)  
#     average_rating = db.Column(db.Float)
#     genre = db.Column(db.String)
#     duration = db.Column(db.String)  #
#     gross_earnings = db.Column(db.String)  #
#     image = db.Column(db.String)  #
#     actors = db.relationship('Actor', secondary='movie_actors', back_populates='movies')
#     directors = db.relationship('Director', secondary='movie_directors', back_populates='movies')

# class Actor(db.Model):
#     __tablename__ = 'actor'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     actor = db.Column(db.Boolean, default=True)
#     movies = db.relationship('Movie', secondary='movie_actors', back_populates='actors')

# class Director(db.Model):
#     __tablename__ = 'director'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     director = db.Column(db.Boolean, default=True)
#     movies = db.relationship('Movie', secondary='movie_directors', back_populates='directors')
    
class Movies:
    def __init__(self, id, title, release_date, average_rating, genre, duration, gross_earnings, image):
        self.id = id
        self.title = title
        self.release_date = release_date.strftime("%Y-%m-%d")
        self.average_rating = average_rating
        self.genre = genre
        self.duration = duration
        self.gross_earnings = gross_earnings
        self.image = image
        self.actors = []
        self.directors = []

    def to_dict(self):
        return vars(self)

class Actors:
    def __init__(self, id, name, actor):
        self.id = id
        self.name = name
        self.actor = actor
        

    def to_dict(self):
        return vars(self)

class Directors:
    def __init__(self, id, name, director):
        self.id = id
        self.name = name
        self.director = director
        
    def to_dict(self):
        return vars(self)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        """Add a new node"""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.edges[node.id] = []

    def add_edge(self, from_node_id, to_node_id):
        """Adds an edge to a node that points to another node"""
        if from_node_id in self.edges:
            self.edges[from_node_id].append(to_node_id)
            
        if to_node_id not in self.edges:  # Ensure to_node has an entry in edges
            self.edges[to_node_id] = []
            
    def to_json(self):
        """Convert the graph structure to JSON format"""
        return json.dumps({"nodes": self.nodes, "edges": self.edges}, indent=4)
    
def build_graph():
    with app.app_context():
        graph = Graph()
        data = pd.read_csv('imdb.csv')
        movies = []
        actors = []
        directors = []
        movie_ids = []
        for i, row in data.iterrows():
            if not pd.notna(row['Movie_title']):
                continue
            if pd.notna(row['Year']):
                release_date = datetime.strptime(str(row['Year']),'%Y')
            else:
                release_date = datetime.now()  # Handle missing or malformed dates
                
            try:
                average_rating = float(row['IMDB Rating'])
            except ValueError:
                average_rating = None
            
            if pd.notna(row['Genre']):
                genre=row['Genre']
            else:
                genre = None
                
            if pd.notna(row['Duration']):
                duration=row['Duration']
            else:
                duration = None
            if pd.notna(row['Gross earnings']):
                gross_earnings=row['Gross earnings']
            else:
                gross_earnings = None
            
            
            movie_id = random.randint(1000, 9999)
            while movie_id in movie_ids:
                movie_id = random.randint(1000, 9999)
            movie_ids.append(movie_id)
            movie = Movies(movie_id, row['Movie_title'], release_date, average_rating, genre, duration, gross_earnings, row['Images'])
            movies.append(movie)
            
            director_names = row['Director'].split(', ')
            for name in director_names:
                director_id = random.randint(1000, 9999)
                while director_id in movie_ids:
                    director_id = random.randint(1000, 9999)
                movie_ids.append(director_id)
                director = Directors(director_id, name, True)
                directors.append(director)
                movie.directors.append(director)
                
            actors_list = eval(row['Actors'])
            for name in actors_list:
                actor_id = random.randint(1000, 9999)
                while actor_id in movie_ids:
                    actor_id = random.randint(1000, 9999)
                movie_ids.append(actor_id)
                actor = Actors(actor_id, name, True)
                actors.append(actor)
                movie.actors.append(actor)

        for movie in movies:
            graph.add_node(movie)
            
        for actor in actors:
            graph.add_node(Actors(actor.id, actor.name, actor.actor))
            
        for director in directors:
            graph.add_node(Directors(director.id, director.name, director.director))

        # Suppose that the relationship between the movie, the actor and the director are also taken from the database
        for movie in movies:
            for actor in movie.actors:
                graph.add_edge(movie.id, actor.id)
                graph.add_edge(actor.id, movie.id)
            for director in movie.directors:
                graph.add_edge(movie.id, director.id)
                graph.add_edge(director.id, movie.id)

    return graph


initialized = False


@app.before_first_request
def load_graph():
    print("Loading graph...")
    global graph
    graph = build_graph()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies')
def movies():
    movies_list = [graph.nodes[node_id].to_dict() for node_id in graph.nodes if isinstance(graph.nodes[node_id], Movies)]
    return render_template('movies.html', movies=movies_list)

@app.route('/actors')
def actors():
    # Access the graph to get actors and their movies
    actors_list = [graph.nodes[node_id].to_dict() for node_id in graph.nodes if isinstance(graph.nodes[node_id], Actors)]
    # Process each actor to ensure unique movies
    for actor in actors_list:
        seen = set()
        unique_movies = []
        for movie_id in graph.edges[actor['id']]:  # Assuming edges store movie connections
            movie = graph.nodes[movie_id]
            if movie.title not in seen:
                seen.add(movie.title)
                unique_movies.append(movie)
        actor['movies'] = unique_movies  # Assuming each actor dict can store its movies directly
    return render_template('actors.html', actors=actors_list)

@app.route('/directors')
def directors():
    # Access the graph to get directors and their movies
    directors_list = [graph.nodes[node_id].to_dict() for node_id in graph.nodes if isinstance(graph.nodes[node_id], Directors)]
    # Process each director to ensure unique movies
    for director in directors_list:
        seen = set()
        unique_movies = []
        for movie_id in graph.edges[director['id']]:  # Assuming edges store movie connections
            movie = graph.nodes[movie_id]
            if movie.title not in seen:
                seen.add(movie.title)
                unique_movies.append(movie)
        director['movies'] = unique_movies  # Assuming each actor dict can store its movies directly

    return render_template('directors.html', directors=directors_list)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    # Fetch the movie details from the graph
    movie = graph.nodes.get(movie_id, None)
    if movie is None:
        return render_template('404.html'), 404  # Assuming there's a 404 error page
    # Render the movie details page
    return render_template('movie_details.html', movie=movie.to_dict())

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        release_date = request.form['release_date']
        genre = request.form['genre']
        duration = request.form['duration']
        gross_earnings = request.form['gross_earnings']
        image_url = request.form['image_url']
        actor_names = [name.strip() for name in request.form['actors'].split(',')]
        director_names = [name.strip() for name in request.form['directors'].split(',')]

        movie = Movies(title=title, release_date=release_date, genre=genre,
                      duration=duration, gross_earnings=gross_earnings, image=image_url)

        for name in actor_names:
            for node_id in graph.nodes:
                if isinstance(graph.nodes[node_id], Actors) and graph.nodes[node_id].name == name:
                    actor = graph.nodes[node_id]
                    movie.actors.append(actor)
                    graph.add_edge(movie.id, actor.id)
                    graph.add_edge(actor.id, movie.id)
                    break
                elif isinstance(graph.nodes[node_id], Actors) and graph.nodes[node_id].name != name:
                    actor_id = random.randint(1000, 9999)
                    while actor_id in graph.nodes:
                        actor_id = random.randint(1000, 9999)
                    actor = Actors(actor_id, name, True)
                    graph.add_node(actor)
                    movie.actors.append(actor)
                    graph.add_edge(movie.id, actor.id)
                    graph.add_edge(actor.id, movie.id)
                    break
    

        for name in director_names:
            for node_id in graph.nodes:
                if isinstance(graph.nodes[node_id], Directors) and graph.nodes[node_id].name == name:
                    director = graph.nodes[node_id]
                    movie.directors.append(director)
                    graph.add_edge(movie.id, director.id)
                    graph.add_edge(director.id, movie.id)
                    break
                elif isinstance(graph.nodes[node_id], Directors) and graph.nodes[node_id].name != name:
                    director_id = random.randint(1000, 9999)
                    while director_id in graph.nodes:
                        director_id = random.randint(1000, 9999)
                    director = Directors(director_id, name, True)
                    graph.add_node(director)
                    movie.directors.append(director)
                    graph.add_edge(movie.id, director.id)
                    graph.add_edge(director.id, movie.id)
                    break

        graph.add_node(movie)
        return redirect(url_for('list_movies'))

    return render_template('add_movie.html')

@app.route('/add_actor', methods=['GET', 'POST'])
def add_actor():
    if request.method == 'POST':
        name = request.form['name']
        movies_input = request.form['movies']
        movie_titles = [title.strip() for title in movies_input.split(',') if title.strip()]
        actor_id = random.randint(1000, 9999)
        while actor_id in graph.nodes:
            actor_id = random.randint(1000, 9999)
        actor = Actors(actor_id, name, True)
        graph.add_node(actor)
        for title in movie_titles:
            for node_id in graph.nodes:
                if isinstance(graph.nodes[node_id], Movies) and graph.nodes[node_id].title == title:
                    movie = graph.nodes[node_id]
                    movie.actors.append(actor)
                    graph.add_edge(movie.id, actor.id)
                    graph.add_edge(actor.id, movie.id)
                    break
                elif isinstance(graph.nodes[node_id], Movies) and graph.nodes[node_id].title != title:
                    movie_id = random.randint(1000, 9999)
                    while movie_id in graph.nodes:
                        movie_id = random.randint(1000, 9999)
                    movie = Movies(movie_id, title, datetime.now(), None, None, None, None, None)
                    graph.add_node(movie)
                    movie.actors.append(actor)
                    graph.add_edge(movie.id, actor.id)
                    graph.add_edge(actor.id, movie.id)
                    break
        
        return redirect(url_for('actors'))
    
    return render_template('add_actor.html')

@app.route('/add_director', methods=['GET', 'POST'])
def add_director():
    if request.method == 'POST':
        # Process the form data, create a new Director object, and save it
        name = request.form['name']
        movies_input = request.form['movies']
        movie_titles = [title.strip() for title in movies_input.split(',') if title.strip()]
        for title in movie_titles:
            for node_id in graph.nodes:
                if isinstance(graph.nodes[node_id], Movies) and graph.nodes[node_id].title == title:
                    movie = graph.nodes[node_id]
                    break
                elif isinstance(graph.nodes[node_id], Movies) and graph.nodes[node_id].title != title:
                    movie_id = random.randint(1000, 9999)
                    while movie_id in graph.nodes:
                        movie_id = random.randint(1000, 9999)
                    movie = Movies(movie_id, title, datetime.now(), None, None, None, None)
                    graph.add_node(movie)
                    break
            for node_id in graph.nodes:
                if isinstance(graph.nodes[node_id], Directors) and graph.nodes[node_id].name == name:
                    director = graph.nodes[node_id]
                    movie.directors.append(director)
                    graph.add_edge(movie.id, director.id)
                    graph.add_edge(director.id, movie.id)
                    break
                elif isinstance(graph.nodes[node_id], Directors) and graph.nodes[node_id].name != name:
                    director_id = random.randint(1000, 9999)
                    while director_id in graph.nodes:
                        director_id = random.randint(1000, 9999)
                    director = Directors(director_id, name, True)
                    graph.add_node(director)
                    movie.directors.append(director)
                    graph.add_edge(movie.id, director.id)
                    graph.add_edge(director.id, movie.id)
                    break
        return redirect(url_for('directors'))
    return render_template('add_director.html')


if __name__ == '__main__':
    app.run(debug=True)







