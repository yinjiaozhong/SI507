
import numpy as np
import json
import os
import random
import time
random.seed(17)
import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from collections import Counter



# step 1 fetch the JSON data
#response = requests.get("https://dsl.richmond.edu/panorama/redlining/static/downloads/geojson/MIDetroit1939.geojson")

# Check if the request was successful
#if response.status_code == 200:
    # Deserialize the JSON data into a Python object
    #RedliningData = response.json()
    #with open('request.json', 'w', encoding='utf-8') as file:
        #json.dump(RedliningData, file, ensure_ascii=False, indent=4)
#else:
    # Print an error message
    #print(f"Failed to retrieve the data. HTTP Status Code: {response.status_code}")

# directly read cache instead of using request
#with open('request.json', 'r', encoding='utf-8') as file:
    #RedliningData = json.load(file)

# step 2: develop the structure of the redlining data
# step 2.1: defining detroit district class
# define arrays of x and y coordinates
#xgrid = np.arange(-83.5, -82.8, .004)
#ygrid = np.arange(42.1, 42.6, .004)
#xmesh, ymesh = np.meshgrid(xgrid, ygrid)
#points = np.vstack((xmesh.flatten(), ymesh.flatten())).T

class DetroitDistrict:
    """
    A class representing a district in Detroit with attributes related to historical redlining.
    coordinates,holcGrade,holcColor,id,description should be load from the redLine data file
    if cache is not available

    Parameters 
    ------------------------------
    coordinates : list of lists, 2D List, not list of list of list
        Coordinates defining the district boundaries from the json file
        Note that some districts are non-contiguous, which may
        effect the structure of this attribute

    holcGrade : str
        The HOLC grade of the district.

    id : str
        The identifier for the district, the HOLC ID.

    description : str, optional
        Qualitative description of the district.

    holcColor : str, optional
        A string represent the color of the holcGrade of the district

    randomLat : float, optional
        A random latitude within the district (default is None).

    randomLong : float, optional
        A random longitude within the district (default is None).

    medIncome : int, optional
        Median household income for the district, to be filled later (default is None).
        
    censusTract : str, optional
        Census tract code for the district (default is None).


    Attributes
    ------------------------------
    self.coordinates 
    self.holcGrade 
    holcColor : str
        The color representation of the HOLC grade.
        • Districts with holc grade A should be assigned the color 'darkgreen'
        • Districts with holc grade B should be assigned the color 'cornflowerblue'
        • Districts with holc grade C should be assigned the color 'gold'
        • Districts with holc grade D should be assigned the color 'maroon'
        If there is no input for holcColor, it should be generated based on the holcGrade and the rule above.

    self.id 
    self.description 
    self.randomLat 
    self.randomLong 
    self.medIncome 
    self.censusTract 


    """
    def __init__(self, coordinates, holcGrade, id, description, holcColor = None, randomLat=None, randomLong=None, medIncome=None, censusTract=None):
        self.coordinates = coordinates
        self.holcGrade = holcGrade
        self.id = id
        self.description = description
        self.randomLat = randomLat
        self.randomLong = randomLong
        self.medIncome = medIncome
        self.censusTract = censusTract

        if holcColor is None:
            # Assigning holcColor based on holcGrade
            color_map = {'A': 'darkgreen', 'B': 'cornflowerblue', 'C': 'gold', 'D': 'maroon'}
            self.holcColor = color_map.get(holcGrade, None)
        else:
            self.holcColor = holcColor



class RedLines:
    """
    A class to manage and analyze redlining district data.

    Attributes
    ----------
    districts : list of DetroitDistrict
        A list to store instances of DetroitDistrict.

    """

    def __init__(self, cacheFile=None):
        """
        Initializes the RedLines class without any districts.
        assign districts attribute to an empty list
        """
        self.districts = []

        

    def createDistricts(self, fileName):
        """
        Creates DetroitDistrict instances from redlining data in a specified file.
        Based on the understanding in step 1, load the file,parse the json object, 
        and create 238 districts instance.
        Finally, store districts instance in a list, 
        and assign the list to be districts attribute of RedLines.

        Parameters
        ----------
        fileName : str
            The name of the file containing redlining data in JSON format.

        Hint
        ----------
        The data for description attribute could be from  
        one of the dict key with only number.

        """
        with open(fileName, 'r') as f:
            data = json.load(f)


        # Iterate over the data and create DetroitDistrict instances

        for feature in data['features']:
            #print(type(data['features']))
            properties = feature['properties']
            geometry = feature['geometry']
            coordinates = geometry['coordinates']
            description = properties.get('area_description_data', {}).get('1', '')
            #print("Loaded description:", description)  # Add this line to check loaded descriptions

            district = DetroitDistrict(
                coordinates=feature['geometry']['coordinates'],
                holcGrade=properties['holc_grade'],
                id=properties['holc_id'],
                description=description,
            )
            # Extract relevant information for creating a district instance

            self.districts.append(district)


    def plotDistricts(self):
        """
        Plots the districts using matplotlib, displaying each district's location and color.
        Name it redlines_graph.png and save it to the current directory. 
        """
        # Extracting coordinates and colors for plotting
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon
        fig, ax = plt.subplots()  # Uncommented to create a subplot
        for district in self.districts:
            #print("District ID:", district.id)

            # Ensure that the district has coordinates
            if not district.coordinates:
                #print("Skipping empty coordinates for district:", district.id)
                continue

            for polygon_coords in district.coordinates:
                # Sometimes the coordinates are nested even more for multipolygons,
                # so we make sure to access the innermost list
                while isinstance(polygon_coords[0][0], list):
                    polygon_coords = polygon_coords[0]

                # Polygon expects a list of (x, y) tuples
                polygon = Polygon(polygon_coords, edgecolor='r', fill=False)
                ax.add_patch(polygon)
                #ax.autoscale()

        ax.set_xlim(-83.15, -83.1)
        ax.set_ylim(42.42, 42.45)
        #plt.rcParams["figure.figsize"] = (15, 15)
        plt.savefig('redlines_graph.png')  # Saving the image before displaying
        plt.show()  # Finally display the plot

            # Assuming that district.coordinates is a list of tuples of (x, y) coordinates
            # for the vertices of a polygon
            #coordinates = district.coordinates
            #print("Coordinates:", coordinates)

            #if not isinstance(coordinates, list) or not all(isinstance(coord, tuple) for coord in coordinates):
                #print("Skipping invalid coordinates format for district:", district.id)
                #continue



    # # Save the map to an HTML file
        # m.save('districts_map.html')
        # #fig, ax = plt.subplots()
        # for district in self.districts:
        #     print("District ID:", district.id)
        #     print("Coordinates:", district.coordinates)
        #
        #     if not district.coordinates:
        #         print("Skipping empty coordinates for district:", district.id)
        #         continue
        #
        #     coordinates = district.coordinates[0][0][0]
        #     print("Coordinates:", coordinates)
        #     print("Type of coordinates:", type(coordinates))
        #
        #     if not isinstance(coordinates, list):
        #         print("Skipping non-list coordinates for district:", district.id)
        #         continue
        #
        #     x_coords = [coord[0] for coord in coordinates]
        #     y_coords = [coord[1] for coord in coordinates]
        #     print("x_coords:", x_coords)
        #     print("y_coords:", y_coords)
        #     # Convert x_coords and y_coords to lists
        #     x_coords = list(x_coords)
        #     y_coords = list(y_coords)
        #     print("Number of x_coords:", len(x_coords))
        #     print("Number of y_coords:", len(y_coords))
        #
        #     polygon = Polygon(coordinates, edgecolor='r', fill=False)
        #     plt.gca().add_patch(polygon)
        # plt.xlim(-83.15, -83.1)
        # plt.ylim(42.42, 42.45)
        # plt.show()



    def generateRandPoint(self):
        """
        Generates a random point within the boundaries of each district.

        This method creates a mesh grid of points covering the geographical area of interest
        and then selects a random point within the boundary of each district.

        Attributes
        ----------
        self.districts : list of DetroitDistrict
            The list of district instances in the RedLines class.

        Note
        ----
        The random point is assigned as the randomLat and randomLong  for each district.
        This method assumes the 'self.districts' attribute has been populated with DetroitDistrict instances.

        """
        for district in self.districts:
            min_x = min(y[0] for y in district.coordinates[0])
            max_x = max(y[0] for y in district.coordinates[0])
            min_y = min(y[1] for y in district.coordinates[0])
            max_y = max(y[1] for y in district.coordinates[0])
            district.randomLat = np.random.uniform(min_x, max_x)
            district.randomLong = np.random.uniform(min_y, max_y)



    def fetchCensus(self):

        """
        Fetches the census tract for each district in the list of districts using the FCC API.

        This method iterates over the all districts in `self.districts`, retrieves the census tract 
        for each district based on its random latitude and longitude, and updates the district's 
        `censusTract` attribute.

        Note
        ----
        The method fetches data from "https://geo.fcc.gov/api/census/area" and assumes that 
        `randomLat` and `randomLong` attributes of each district are already set.

        The function `fetch` is an internal helper function that performs the actual API request.

        In the api call, check if the response.status_code is 200.
        If not, it might indicate the api call made is not correct, check your api call parameters.

        If you get status_code 200 and other code alternativly, it could indicate the fcc webiste is not 
        stable. Using a while loop to make anther api request in fetch function, until you get the correct result. 

        Important
        -----------
        The order of the API call parameter has to follow the following. 
        'lat': xxx,'lon': xxx,'censusYear': xxx,'format': 'json' Or
        'lat': xxx,'lon': xxx,'censusYear': xxx

        """

        def fetch(lat, lon, censusYear='2010'):
            # API endpoint
            url = "https://geo.fcc.gov/api/census/area"
            # Parameters for the API call
            params = {'lat': lat, 'lon': lon, 'censusYear': censusYear, 'format': 'json'}
            retries = 3  # Set a max number of retries
            delay = 1  # Set a delay between retries in seconds

            for attempt in range(retries):
                try:
                    response = requests.get(url, params=params, timeout=5)
                    if response.status_code == 200:
                        return response.json()
                        if 'results' in data and data['results']:
                            return data['results'][0]['block_fips']
                except requests.RequestException as e:
                    print(f"Request failed: {e}")

                if attempt < retries - 1:
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff

            return None  # Could not get data

        failed_districts = []
        for district in self.districts:
            try:
                censusTract = fetch(district.randomLat, district.randomLong)
                if censusTract:
                    district.censusTract = censusTract
                else:
                    print(f"Failed to fetch census data for district {district.id}")
                    failed_districts.append(district.id)
            except KeyboardInterrupt:
                print("The program terminates manually and is currently processed to the region:", district.id)
                break

        # failed districts
        if failed_districts:
            print("The following areas failed to obtain census data:", failed_districts)



    def fetchIncome(self):

        """
        Retrieves the median household income for each district based on the census tract.

        This method requests income data from the ACS 5-Year Data via the U.S. Census Bureau's API 
        for the year 2018. It then maps these incomes to the corresponding census tracts and updates 
        the median income attribute of each district in `self.districts`.

        Note
        ----
        The method assumes that the `censusTract` attribute for each district is already set. It updates 
        the `medIncome` attribute of each district based on the fetched income data. If the income data 
        is not available or is negative, the median income is set to 0.

        """
        for district in self.districts:
            # API endpoint for ACS 5-Year Data
            url = "https://api.census.gov/data/2018/acs/acs5/profile"
            # Parameters for the API call
            params = {'get': 'DP03_0062E',
                      'for': 'tract:{}'.format(district.censusTract),
                      'in': 'state:26'}
            response = requests.get(url, params=params)
            # Parsing JSON response
            data = response.json()
            try:
                median_income = int(data[1][0])
                district.medIncome = max(median_income, 0)
            except:
                district.medIncome = 0

        


    def cacheData(self, fileName):
        """
        Saves the current state of district data to a file in JSON format.
        Using the __dict__ magic method on each district instance, and save the 
        result of it to a list.
        After creating the list, dump it to a json file with the inputted name.
        You should name the cache file as redlines_cache.json

        Parameters
        ----------
        filename : str
            The name of the file where the district data will be saved.
        """
        # Serializing each district instance to a dictionary
        district_data_list = [district.__dict__ for district in self.districts]

        # Dumping the list to a JSON file
        with open(fileName, 'w') as f:
            json.dump(district_data_list, f)

    def loadCache(self, fileName):
        """
        Loads district data from a cache JSON file if it exists.

        Parameters
        ----------
        fileName : str
            The name of the file from which to load the district data.
            You should name the cache file as redlines_cache.json

        Returns
        -------
        bool
            True if the data was successfully loaded, False otherwise.
        """
        if os.path.exists(fileName):
            with open(fileName, 'r') as f:
                data = json.load(f)
                self.districts = [DetroitDistrict(
                    **district_data) for district_data in data]
            return True
        else:
            return False

    def calcIncomeStats(self):
        """
        Use np.median and np.mean to
        Calculates the mean and median of median household incomes for each district grade (A, B, C, D).

        This method computes the mean and median incomes for districts grouped by their HOLC grades.
        The results are stored in a list following the pattern: [AMean, AMedian, BMean, BMedian, ...].
        After your calculations, you need to round the result to the closest whole int.
        Relate reading https://www.w3schools.com/python/ref_func_round.asp


        Returns
        -------
        list
            A list containing mean and median income values for each district grade in the order A, B, C, D.
        """
        grades = {'A': [], 'B': [], 'C': [], 'D': []}
        for district in self.districts:
            grades[district.holcGrade].append(district.medIncome)
        result = []
        for grade in grades:
            mean = round(np.mean(grades[grade]))
            median = round(np.median(grades[grade]))
            result.extend([mean, median])
        return result



    def findCommonWords(self):
        """
        Analyzes the qualitative descriptions of each district category (A, B, C, D) and identifies the
        10 most common words unique to each category.

        This method aggregates the qualitative descriptions for each district category, splits them into
        words, and computes the frequency of each word. It then identifies and returns the 10 most 
        common words that are unique to each category, excluding common English filler words.

        Returns
        -------
        list of lists
            A list containing four lists, each list containing the 10 most common words for each 
            district category (A, B, C, D). The first list should represent grade A, and second for grade B,etc.
            The words should be in the order of their frequency.

        Notes
        -----
        - Common English filler words such as 'the', 'of', 'and', etc., are excluded from the analysis.
        - The method ensures that the common words are unique across the categories, i.e., no word 
        appears in more than one category's top 10 list.
        - Regular expressions could be used for word splitting to accurately capture words from the text.
        - Counter from collections could also be used.

        """
        # List of common filler words to exclude, you could add more if needed.
        filler_words = set(['the', 'of', 'and', 'in', 'to', 'a', 'is', 'for', 'on', 'that'])
        grades = {'A': [], 'B': [], 'C': [], 'D': []}
        for district in self.districts:
            grades[district.holcGrade].append(district.description)
        result = []
        for grade in grades:
            words = []
            for description in grades[grade]:
                words.extend(description.split())
            filtered_words = [word.lower() for word in words if word.lower() not in filler_words]
            counts = Counter(filtered_words)
            top_words = [word for word, _ in counts.most_common(10)]
            result.append(top_words)
        return result
    def calcRank(self):
        """
        Calculates and assigns a rank to each district based on median income.

        This method sorts the districts in descending order of their median income and then assigns
        a rank to each district, with 1 being the highest income district.

        Note
        ----
        The rank is assigned based on the position in the sorted list, so the district with the highest
        median income gets a rank of 1, the second-highest gets 2, and so on. Ties are not accounted for;
        each district will receive a unique rank.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "rank" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache. 

        Attribute 
        ----
        rank

        """
        self.districts.sort(key=lambda x: x.medIncome, reverse=True)
        for i, district in enumerate(self.districts):
            district.rank = i + 1




    def calcPopu(self):
        """
        Fetches and calculates the percentage of Black or African American residents in each district.

        This method fetch the total and Black populations for each census tract in Michigan from 
        the U.S. Census Bureau's API, like the median income data.  It then calculates the percentage of Black residents in each tract
        and assigns this value to the corresponding district percent attribute.

        Note
        ----
        The method assumes that the census tract IDs in the district data match those used by the Census Bureau.
        The percentage is rounded to two decimal places. If the Black population is zero, the percentage is set to 0. 
        Elif the total population is zero, the percentage is set to 1.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "percent" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache. 


        Attribute 
        ----
        percent

        """
        def fetch_population(tract):
            url = "https://api.census.gov/data/2019/acs/acs5"
            params = {'get': 'B02001_001E,B02001_003E',
                      'for': 'tract:{}'.format(tract),
                      'in': 'state:26', 'key': 'your_api_key_here'}
            response = requests.get(url, params=params)
            data = response.json()
            try:
                total_population = int(data[1][0])
                black_population = int(data[1][1])
                if total_population == 0:
                    return 1
                else:
                    return round(black_population / total_population * 100, 2)
            except:
                return 0

        for district in self.districts:
            district.percent = fetch_population(district.censusTract)

    def comment(self):
        '''
        Look at the
        districts in each category, A, B, C and D. Are there any trends that you see? Share 1 paragraph of your
        findings. And a few sentences(more than 50 words) about how this exercise did or did not change your understanding of
        residential segregation. Print you thought in the method.
        '''
        print("Analysis and Reflection:")


# Use main function to test your class implementations.
# Feel free to modify the example main function.
def main():
    myRedLines = RedLines()
    myRedLines.createDistricts('redlines_data.json')
    myRedLines.plotDistricts()
    myRedLines.generateRandPoint()
    myRedLines.fetchCensus()
    myRedLines.fetchIncome()
    myRedLines.calcRank()  # Assuming you have this method
    myRedLines.calcPopu()  # Assuming you have this method
    myRedLines.cacheData('redlines_cache.json')
    myRedLines.loadCache('redlines_cache.json')
    # Add any other function calls as needed
    try:
        myRedLines.generateRandPoint()
        myRedLines.fetchCensus()
        myRedLines.fetchIncome()

    except KeyboardInterrupt:
        print("The program was interrupted by the user")

if __name__ == '__main__':
    main()


