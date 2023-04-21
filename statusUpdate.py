import json
import requests
from sense_hat import SenseHat
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout, ConnectionError
import time
import datetime

sense = SenseHat()
sense.set_rotation(180)
sense.low_light = True
sync_frequency = 30
#Kingsbury, Preston Road
trainStations = ['jubilee', '940GZZLUKBY'], ['metropolitan', '940GZZLUPRD']
#79, 204 to Kingsbury, 204 to Preston Road
busStops = [['79', '490013367N1'], ['204', '490009792K'], ['204', '490009792J']]

jubileeTerminuses = ['Stratford Underground Station', 'Canning Town Underground Station', 'West Ham Underground Station',
        'North Greenwich Underground Station']
metropolitanTerminuses = ['Baker Street Underground Station, Aldgate Underground Station']

jubilee = [128, 128, 128]
metropolitan = [128, 0, 32]
edgeware = [255, 0, 0]
sudburyTown = [65, 105, 205]
alperton = [255, 128, 0]
O = [0,0,0]




def displayError():
    sense.show_message("Server Error") 

def getNext(stations, direction):
    toReturn = []
    for station in stations:
        temp = getFromAPI(station[0],station[1], direction)
        if (temp != []): 
            for x in temp:
                toReturn.append(x)
        else:
            toReturn.append([station[0] + ": updates unavailable", 0])
    return toReturn


def getFromAPI(line, stop, direction):
    url = 'https://api.tfl.gov.uk/Line/' + line + '/Arrivals/' + stop + '?direction=' + direction
    try:
        response = requests.get(url, timeout = 10)
    except (ConnectTimeout, ReadTimeout, Timeout, HTTPError, ConnectionError):
        displayError()
        return
    if (response.status_code != 200):
        displayError()
        return
    else:
        returns = [] 
        for result in response.json():
            returns.append([result['destinationName'], int(result['timeToStation'] / 60)])
        return returns


def getStatus():
    updates = []
    for lines in trainStations:
        response = requests.get('https://api.tfl.gov.uk/Line/' + lines[0] + '/Disruption')

        if (response.status_code != 200):
            displayError()
        else:
            json = response.json()
            if len(json) != 0:
                updates.append([json[0]['closureText'], json[0]['description']])

def scroll(array):
    if array != None:
        for item in array:
            print(item[0] + " will arrive at " + str(item[1]))

def calculateBlobs(time):
    if time > 15:
        return 7 
    elif time > 10:
        return 6
    elif time > 8:
        return 5
    elif time > 6:
        return 4
    elif time > 4:
        return 3
    elif time > 2:
        return 2
    elif time > 1:
        return 1
    else:
        return 0
    
def draw(trains, buses):
    toDraw = [
            [O,O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O,O]
            ]
    for station, time in trains:
        blob = calculateBlobs(time)
        if station in jubileeTerminuses:
            toDraw[0][7 - blob] = jubilee  
        elif station in metropolitanTerminuses:
            toDraw[3][7 - blob] = metropolitan
    
    for stop, time in buses:
        blob = calculateBlobs(time)
        if stop == 'Sudbury Town':
            toDraw[4][7 - blob] = sudburyTown
        elif stop == "Alperton, Sainsbury's":
            toDraw[5][7 - blob] = alperton
        elif stop == 'Edgware Station':
            toDraw[1][7 - blob] = edgeware

    transpose = []
    for i in range(0,8):
        for j in range(0,8):
            transpose.append(toDraw[j][i])

    sense.set_pixels(transpose)


def main():
    sense.clear()
    while True:
        #hour = datetime.datetime.now().hour
        #if hour > 10:
        #    sense.clear()
        #    time.sleep ((24 - hour) * 60 * 60)
        #if hour < 6:
        #    sense.clear()
        #    time.sleep ((6 - hour) * 60 * 60)

        statuses = getStatus()
        trains = getNext(trainStations, 'outbound')
        buses = getNext(busStops, 'all')

        trains.sort(key = lambda x: x[1])
        buses.sort(key = lambda x: x[1])
    
        #scroll(statuses)
        #scroll(trains)
        #scroll(buses)

        if statuses != None and len(statuses) > 0:
            for status in statuses:
                sense.show_message(status[0] + ":" + status[1])

        draw(trains, buses)
        time.sleep(sync_frequency)


main()

