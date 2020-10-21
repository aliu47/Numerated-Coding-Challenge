import sys
import requests
import datetime
import dateutil.parser
from pytz import timezone
# Title: Numerated Coding Challenge
# Author: Andrew Liu
# giDate: 10/21/2020
# Description: Find the next departing train for a particular stop on the MBTA T network.
# First the program asks the user to select a route from a list of routes.
# Next the user selects a stop that is on the route. Next the user selects the direction
# That their train is going. Finally the program will take this data and return the estimated time.

# Object for Route
class Route:
    def __init__(self, id, name, directions):
        super().__init__()
        self.id = id
        self.name = name
        self.directions = directions

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.directions == other.directions

# Object for Stop
class Stop:
    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

# Object for Direction
class Direction:
    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

class App:
    def main():
        railType = "0,1"
        routes = App.getRoutes(railType)
        route = App.selectRoute(routes)
        stops = App.getStops(route)
        stop = App.selectStop(stops)
        direction = App.selectDirection(route)
        App.getPrediction(route, stop, direction)

    def getRoutes(railType):
        try:
            # Get light and heavy rail trains
            r = requests.get(
                "https://api-v3.mbta.com/routes?filter[type]="+railType)
            r_dict = r.json()
            routes = dict()
            # add each route object to the routes dictonary
            for data in r_dict['data']:
                routes[data["attributes"]["long_name"]] = Route(
                    data["id"], data["attributes"]["long_name"], data["attributes"]["direction_names"])
        except:
            print("Error retrieving routes")
            exit()
        return routes

    # Get the list of stops based on route id

    def getStops(route):
        try:
            r = requests.get(
                "https://api-v3.mbta.com/stops?filter[route]="+route.id)
            r_dict = r.json()
            stops = dict()
            # add each stop object to the stops dictionary
            for data in r_dict['data']:
                # print('"'+data["attributes"]["name"]+'":Stop("'+data["id"]+'","' +
                #       data["attributes"]["name"]+'"),')
                stops[data["attributes"]["name"]] = Stop(
                    data["id"], data["attributes"]["name"])
        except:
            print("Error retrieving stops")
            exit()
        return stops

    # Using the data provided find the next arrival time of the train

    def getPrediction(route, stop, direction):
        r = requests.get("https://api-v3.mbta.com/predictions?filter[route]="+route.id +
                         "&filter[stop]="+stop.id+"&filter[direction_id]="+direction.id+"&include=stop")
        r_dict = r.json()
        # set the closet prediction to the maximum time delta value
        closestPrediction = datetime.timedelta.max
        # get the current time
        currentTime = datetime.datetime.now(timezone("US/Eastern"))
        # check each arrival prediction, keep track of the prediction that is closest to the current time that has not passed
        for data in r_dict['data']:
            # make sure that the arrival_time is not null
            if(data["attributes"]["arrival_time"] != None):
                time = data["attributes"]["arrival_time"]
                arrivalTime = dateutil.parser.parse(time)
                temp = arrivalTime-currentTime
                # check if the current arrival time is sooner than the last one stored
                if((temp) < closestPrediction and temp.days >= 0):
                    closestPrediction = temp
            else:
                print("Sorry, this stop is unavailable at this time.")
                exit()
        print("\nRoute: "+route.name+" | Stop: " +
              stop.name + " | Direction: "+direction.name)
        # Something went wrong and the prediction did not change
        if(closestPrediction == datetime.timedelta.max):
            print("Sorry, this stop is unavailable at this time.")
            return closestPrediction
        else:
            print("The train will be arriving in " +
                  str(int(closestPrediction.seconds/60))+" minutes")
            return closestPrediction

    # Prompt user to select a route from the list and return the route selected

    def selectRoute(routes):
        routeName = None
        while not (routeName in routes):
            # display the list of stops
            print("\nRoutes: ")
            for route in routes:
                print(route)
            print("Please select a route: ")
            routeName = input()
            try:
                routeSelected = routes[routeName]
            except:
                print("\nInvalid route")
            return routeSelected

    # Prompt user to select a stop from the list and return the stop selected

    def selectStop(stops):
        stopName = None
        while not (stopName in stops):
            # display the list of stops
            print("\nStops: ")
            for stop in stops:
                print(stop)
            print("Please select a stop: ")
            stopName = input()
            try:
                stopSelected = stops[stopName]
            except:
                print("\nInvalid stop")
            return stopSelected

    # Prompt user to select a direction from the list and return the direction selected

    def selectDirection(route):
        directionName = None
        while not(directionName in route.directions):
            # display the list of directions
            print("\nDirections:")
            for direction in route.directions:
                print(direction)
            print("Please select a direction: ")
            directionName = input()
            # get the id of the direction and convert it to string
            try:
                directionId = route.directions.index(directionName)
                directionId = str(directionId)
                directionSelected = Direction(directionId, directionName)
            except:
                print("\nInvalid direction")
            return directionSelected


# Run the program
if __name__ == '__main__':
    App.main()
