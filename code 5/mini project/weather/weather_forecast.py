import json
import pandas as pd
import matplotlib.pyplot as plt
import requests


def request_data() -> dict:
    """Get data remotely from by darksky api"""
    lat = 37.7749
    long = 122.4194
    api_key = '6fc0287d72390b13b578404413dea623'
    url = 'https://api.darksky.net/forecast/%s/%s,%s' % (api_key, lat, long)

    response = requests.get(url)
    return json.loads(response.text)


def load_json_sample(path: str) -> dict:
    """Get data locally from pre-download JSON file"""
    with open(path, encoding='utf-8') as json_file:
        return json.load(json_file)


# ------------------------------------------


def daily_data_of_attributes(json_dict: dict, attributes: list) -> dict:
    """
    Filter out daily data for attributes from JSON dict and return a dict of list:
    {
        temperatureMax: [64.57, 64.33, 66.61, 66.52, 64.52, 67.63, 73.37, 68.41]
        temperatureMin: [61.17, 59.39, 61.44, 63.46, 62.5, 63.15, 65.41, 65.62]
        humidity: [0.89, 0.89, 0.71, 0.67, 0.69, 0.69, 0.69, 0.7]
    }
    """
    daily_attributes = {}
    for attr in attributes:
        daily_attributes[attr] = []

    daily_data = json_dict['daily']['data']
    for dict_data in daily_data:
        for attr in attributes:
            daily_attributes[attr].append(dict_data[attr])

    return daily_attributes


def daily_data_of_attributes_better(json_dict, attributes):
    """A better implementation of daily_data_of_attributes"""
    daily_data = json_dict['daily']['data']

    from collections import defaultdict
    daily_attributes = defaultdict(list)

    for dict_data in daily_data:
        for attr in attributes:
            daily_attributes[attr].append(dict_data[attr])

    return daily_attributes


# ------------------------------------------

def say(text: str):
    """Call system built-in "say" command for text-to-speech"""
    import subprocess as sp
    sp.call('say ' + text, shell=True)


# ------------------------------------------

def main(remote=False):

    # Get data
    if remote:
        json_obj = request_data()
    else:
        json_obj = load_json_sample('sample.json')

    # Filter data
    attributes = ['humidity', 'temperatureMax', 'temperatureMin']
    daily_data = daily_data_of_attributes_better(json_obj, attributes)

    # [Test] Print out filtered data
    from pprint import pprint
    pprint(daily_data)

    # Get report string for highest / lowest temp
    highest_temp = max(daily_data['temperatureMax'])
    lowest_temp = min(daily_data['temperatureMin'])
    report = "The highest temperature in the coming week will be" \
        + str(highest_temp) + " degrees, with the lowest of " + str(lowest_temp) + " degrees."

    # [macOS Only]
    say(report)

    # Plot
    df = pd.DataFrame(daily_data)
    df_temperature = df[["temperatureMin", "temperatureMax"]]
    df_humidity = df[["humidity"]]

    # Plot settings
    plt.style.use('ggplot')
    _, axes = plt.subplots(nrows=2)

    df_temperature.plot(ax=axes[0])
    df_humidity.plot(ax=axes[1])

    # Show plot
    plt.show()


# ------------------------------------------


if __name__ == '__main__':
    main(remote=True)
