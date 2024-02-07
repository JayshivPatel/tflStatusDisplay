import json
import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import time
import datetime
from tabulate import tabulate

sync_frequency = 30

kingsbury = {
    "station": "Kingsbury",
    "code": "940GZZLUKBY",
    "lines": ["jubilee"],
}
wembleyPark = {
    "station": "Wembley Park",
    "code": "940GZZLUWYP",
    "lines": ["jubilee", "metropolitan"],
}
finchleyRoad = {
    "station": "Finchley Road",
    "code": "940GZZLUFYR",
    "lines": ["jubilee", "metropolitan"],
}
trainStations = [kingsbury, wembleyPark, finchleyRoad]


def extract(stationData):
    arrivals = []
    for datum in stationData:
        trainData = []
        addSafely("platformName", datum, trainData)
        addSafely("destinationName", datum, trainData)
        addSafely("timeToStation", datum, trainData)
        addSafely("currentLocation", datum, trainData)
        arrivals.append(trainData)
    return arrivals

def error(message):
    print(message)

def addSafely(entry, dictionary, data):
    if entry in dictionary:
        data.append(dictionary[entry])
    else:
        data.append([])

def getArrivals(stations):
    toReturn = []
    for station in stations:
        lines = station["lines"]
        for line in lines:
            stationData = getArrivalsAtStation(line, station["code"])
            if stationData:
                toReturn.append(extract(stationData))
    return toReturn


def getArrivalsAtStation(line, stop):
    url = 'https://api.tfl.gov.uk/Line/' + line + '/Arrivals/' + stop
    try:
        response = requests.get(url, timeout = 10)
    except (ConnectTimeout, ReadTimeout, Timeout, HTTPError, ConnectionError):
        error("Error fetching from API")
        return
    if (response.status_code != 200):
        error("Error fetching from API")
        return
    else:
        returns = [] 
        for result in response.json():
            returns.append(result)
        return returns


def getStatus(line):
    response = requests.get('https://api.tfl.gov.uk/Line/' + line + '/Disruption')
    if (response.status_code != 200):
        error("Error fetching from API")
    else:
        json = response.json()
        if len(json) != 0:
            return ([json[0]['closureText'], json[0]['description']])

def main():
    while True:
        stationArrivals = getArrivals(trainStations)
        for station in stationArrivals:
            platforms = dict()
            for arrival in station:
                if arrival:
                    platform = arrival[0]
                    if platform in platforms:
                        platforms[platform].append(arrival[1:])
                    else:
                        platforms.update({platform: [arrival[1:]]})
            for platform in platforms:
                print(platform, tabulate(platforms[platform]))
        time.sleep(sync_frequency)


main()

