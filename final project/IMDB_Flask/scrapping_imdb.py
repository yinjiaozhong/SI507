import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

pages = list(range(1,7))

title = []
runtime = []
genre = []
imdb_rating = []
year = []
metascore = []
director_names = []
actors_names = []
gross = []
image_links = []

for page in tqdm(pages):
    params = {
        'st_dt': '',
        'mode': 'detail',
        'page': page,
        'sort': 'list_order,asc'
    }

    web_page_url = 'https://www.imdb.com/list/ls062911411/'

    response = requests.get(web_page_url, params=params)


    film_soup = BeautifulSoup(response.content, 'html.parser')

    # Get the divs where the movie information is located
    film_info = film_soup.find_all('div', class_= 'lister-item-content')

    images = film_soup.find_all('img', class_ = 'loadlate')

    for image in images:
        image_links.append(image['loadlate'])
        
    # Loop through film_info object to extract necessary information
    for item in tqdm(film_info):
        title.append((item.a.string))

        time_ = item.find('span', class_ = 'runtime')
        runtime.append(time_.string)

        genre_= item.find('span', class_ = 'genre')
        genre.append(((genre_.string).replace('\n', '')).strip())

        rate = item.find('span',class_ = 'ipl-rating-star__rating')
        imdb_rating.append(float(rate.string))

        year_ = item.find('span', class_ = 'lister-item-year text-muted unbold').string.split()
        if len(year_) <= 1:
            year.append(int(year_[0][1:5]))
        else:
            year.append(int(year_[1][1:5]))

        if item.find('span', class_ = 'metascore favorable') == None:
            metascore.append(np.nan)
        else:
            metascore_ = item.find('span', class_ = 'metascore favorable').string.strip()
            metascore.append(int(metascore_))


    # Create an instance of beautiful soup for directors and actors information
    directors_actors_soup = BeautifulSoup(response.content, 'html.parser')

    # Retrieve all tags and links that have directors and actors information
    director_links = directors_actors_soup.find_all('p', {'class': 'text-muted text-small'})

    directors_info = []
    for links in director_links:
        directors_info.append(links.a)

    # Retreving director names. Ensuring the list is 100
    for name in tqdm(directors_info):
        if name != None:
            director_names.append(name.string)

    # Retreive actors information
    actors_links = []
    for each_tag in directors_actors_soup.find_all('p', {'class': 'text-muted text-small'}):
        if each_tag.find_all('a') != []:
            actors_links.append(each_tag.findAll('a')[1:])


    for links in actors_links:
        each_name = []
        for each_link in tqdm(links):
            each_name.append(each_link.string)
        actors_names.append(each_name)


    # Retrieve list for gross
    list_of_grossEarnings = []
    for i in directors_actors_soup.find_all('p', {'class': 'text-muted text-small'}):
        list_of_grossEarnings.append(i.findAll('span', {'name': 'nv' }))


    for lists in tqdm(list_of_grossEarnings):
        if len(lists) > 1:
            gross.append(lists[1].string)
        elif len(lists) == 1:
            gross.append('N/A')

print('Done Scrapping!')
check = [title, runtime, genre, imdb_rating, year, metascore, director_names, actors_names, gross]
for each_list in check:
    print(len(each_list))

data_frame = pd.DataFrame({'Movie_title': title, 'Genre': genre, 'Director': director_names, 'Actors': actors_names, 'Duration': runtime, 'Year': year, 'IMDB Rating': imdb_rating, 'Meta Score': metascore, 'Gross earnings': gross, 'Images': image_links[:len(title)]}, index=range(1, len(title)+1))

# save to csv
data_frame.to_csv('imdb.csv')