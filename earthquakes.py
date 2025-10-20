import json
# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests

from datetime import date
import matplotlib.pyplot as plt

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )


    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return json.loads(text)

def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year

def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake["properties"]["mag"]

def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    from collections import defaultdict
    mag_per_year = defaultdict(list)

    for earthquanke in earthquakes:
        mag_per_year[get_year(earthquanke)].append(get_magnitude(earthquanke))
    
    return mag_per_year

def plot_average_magnitude_per_year(earthquakes):
    mag_per_year = get_magnitudes_per_year(earthquakes)
    x , y = [] , []
    for year in mag_per_year:
        x.append(year)
        y.append(sum(mag_per_year[year]) / len(mag_per_year[year]))
    
    from matplotlib import pyplot as plt
    plt.plot(x , y)
    plt.xlabel('Year')
    plt.ylabel('Average magnitude per year')


def plot_number_per_year(earthquakes):
    mag_per_year = get_magnitudes_per_year(earthquakes)
    x , y = [] , []
    for year in mag_per_year:
        x.append(year)
        y.append(len(mag_per_year[year]))
    
    from matplotlib import pyplot as plt
    plt.plot(x , y)
    plt.xlabel('Year')
    plt.ylabel('Number per year')



# Get the data we will work with
quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
plot_number_per_year(quakes)
plt.clf()  # This clears the figure, so that we don't overlay the two plots
plot_average_magnitude_per_year(quakes)