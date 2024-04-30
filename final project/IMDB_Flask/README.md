SI507 Final Project: Movie Database Management System

Author: Yinjiao Zhong

Email: yinjiao@umich.edu

Github Repository: https://github.com/yinjiaozhong/SI507

Description

This project is a web-based movie database management system built using Flask and SQLAlchemy including graph structures. It allows users to view, add, and manage movies, actors, and directors in the database from https://www.imdb.com/list/ls062911411/.

Libariy

•	Flask - web framework for python

Compatibility

•	python 3.7 (Anaconda)

Interactions

1	Homepage:

•	Users are greeted with a homepage where they can navigate to different sections of the application.

2	View Movies, Actors, and Directors:

•	Users can click on the respective links to view lists of movies, actors, and directors stored in the database.

3	Movie Details:

•	Clicking on a movie title redirects the user to a page displaying detailed information about the selected movie, including its release date, average rating, genre, duration, gross earnings, image, actors, and directors.

4	Add Movie, Actor, or Director:

•	Users can navigate to the "Add Movie", "Add Actor", or "Add Director" page through the navigation bar.

•	They are prompted to fill in the necessary details such as title, release date, genre, duration, gross earnings, image URL, and associated actors/directors.

5	Search Functionality:

•	Users can search for movies, actors, or directors using the search bar provided on each page.

Potential Answers

•	For prompts requesting input (e.g., adding a movie), users can provide text-based answers such as movie title, actor name, etc.

•	Users can click on links and buttons to navigate through different sections of the application.

Responses

•	Upon submission of the "Add Movie", "Add Actor", or "Add Director" form, the program adds the respective entity to the database and redirects the user to the corresponding page.

•	Clicking on a movie title displays detailed information about the selected movie.

•	Search results are dynamically updated based on the user's input.

Special Instructions

•	Ensure the database file ('imdb.csv') is present in the project directory to populate the initial data.

•	The application requires Flask and SQLAlchemy Python packages to be installed.

•	Users may need to install additional dependencies specified in the project's requirements.txt file.

Network (Graph) Organization

•	The graph represents relationships between movies, actors, and directors.

Nodes:

•	Movies: Represented by instances of the 'Movies' class containing details such as title, release date, average rating, genre, duration, gross earnings, image URL, and associated actors/directors.

•	Actors: Represented by instances of the 'Actors' class containing details such as name and a boolean indicating whether they are an actor or director.

•	Directors: Represented by instances of the 'Directors' class containing details such as name and a boolean indicating whether they are a director or actor.

Edges:

•	Connections between movies, actors, and directors are established through the 'add_edge' method in the 'Graph' class, representing associations such as actors starring in movies and directors directing movies.

Data Sources

1. IMDB Dataset

Origin:
   - Data URL: https://www.imdb.com/list/ls062911411/

Format(s): CSV

Access:

   The IMDB dataset was obtained from https://www.imdb.com/list/ls062911411/. The dataset is publicly available and can be downloaded directly from the provided URL.

Caching:

   Caching was not used for accessing the IMDB dataset.

Summary:

   The IMDB dataset contains information about movies, including title, release date, average rating, genre, duration, gross earnings, and image URLs. 

   
How to Run

•	Step 1: Clone the repository and go to the code directory

git clone https://github.com/yinjiaozhong/SI507.git

cd final project

cd IMDB_Flask

cd templates

•	Step 2: Install flask, if haven’t already

pip install flask

•	Step 3: Run app.py

python app.py

•	Step 4: Open the link in browser

http://127.0.0.1:5000

Note: the specific port may vary. If you can not open the link, please follow the generated prompt instead

•	Step 5: Explore and Enjoy!

Demo
