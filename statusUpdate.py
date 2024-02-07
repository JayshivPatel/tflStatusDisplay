from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(180)
sense.low_light = True

jubilee = [128, 128, 128]
metropolitan = [128, 0, 32]
edgeware = [255, 0, 0]
sudburyTown = [65, 105, 205]
alperton = [255, 128, 0]
O = [0,0,0]


def displayError():
    sense.show_message("Server Error") 

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

