import json
import requests
sync_frequency = 30
#Kingsbury, Preston Road
trainStations = {'jubilee': '940GZZLUKBY', 'metropolitan': '940GZZLUPRD'}
#79, 204 to Kingsbury, 204 to Preston Road
busStops = {'79': '490013367N1','204': '490009792K','204': '490009792J'}


def displayError():
    pass

def getNext(stations, direction):
    toReturn = []
    for line, stop in stations.items():
        temp = getFromAPI(line, stop, direction)
        if (temp != []): 
            for x in temp:
                toReturn.append(x)
        else:
            toReturn.append([line + ": updates unavailable", 0])
    return toReturn


def getFromAPI(line, stop, direction):
   url = 'https://api.tfl.gov.uk/Line/' + line + '/Arrivals/' + stop + '?direction=' + direction
   response = requests.get(url)
   if (response.status_code != 200):
       displayError()
   else:
       returns = [] 
       for result in response.json():
           returns.append([line + ' to ' + result['destinationName'], int(result['timeToStation'] / 60)])
       return returns


def getStatus():
    updates = []
    for line in trainStations:
        response = requests.get('https://api.tfl.gov.uk/Line/' + line + '/Disruption')

        if (response.status_code != 200):
            displayError()
        else:
            json = response.json()
            if len(json) != 0:
                updates.append([json[0]['closureText'], json[0]['description']])

def main():
    statuses = getStatus()
    trains = getNext(trainStations, 'outbound')
    buses = getNext(busStops, 'all')

    trains.sort(key = lambda x: x[1])
    buses.sort(key = lambda x: x[1])
    
    if (statuses != None):
        for status in statuses:
            print(status)
    if (buses != None):
        for bus in buses:
            print(bus)
    if (trains != None):
        for train in trains:
            print(train)


main()

