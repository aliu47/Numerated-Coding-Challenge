import unittest
from unittest import mock
from unittest import TestCase
from Numerated_Challenge import App, Route, Stop, Direction
import Numerated_Challenge
import datetime
import dateutil.parser
from pytz import timezone
# IMPORTANT: before running the test, make sure to update the value of testTime to match the API


class Tests(TestCase):
    # Testing for Heavy and Light rails
    routeDict = {"Red Line": Route("Red", "Red Line", ["South", "North"]),
                 "Mattapan Trolley": Route("Mattapan", "Mattapan Trolley",
                                           ["Outbound", "Inbound"]),
                 "Orange Line": Route("Orange", "Orange Line", ["South", "North"]),
                 "Green Line B": Route("Green-B", "Green Line B", ["West", "East"]),
                 "Green Line C": Route("Green-C", "Green Line C", ["West", "East"]),
                 "Green Line D": Route("Green-D", "Green Line D", ["West", "East"]),
                 "Green Line E": Route("Green-E", "Green Line E", ["West", "East"]),
                 "Blue Line": Route("Blue", "Blue Line", ["West", "East"])}
    # Testing for the Red Line stops
    stopDict = {"Alewife": Stop("place-alfcl", "Alewife"),
                "Davis": Stop("place-davis", "Davis"),
                "Porter": Stop("place-portr", "Porter"),
                "Harvard": Stop("place-harsq", "Harvard"),
                "Central": Stop("place-cntsq", "Central"),
                "Kendall/MIT": Stop("place-knncl", "Kendall/MIT"),
                "Charles/MGH": Stop("place-chmnl", "Charles/MGH"),
                "Park Street": Stop("place-pktrm", "Park Street"),
                "Downtown Crossing": Stop("place-dwnxg", "Downtown Crossing"),
                "South Station": Stop("place-sstat", "South Station"),
                "Broadway": Stop("place-brdwy", "Broadway"),
                "Andrew": Stop("place-andrw", "Andrew"),
                "JFK/UMass": Stop("place-jfk", "JFK/UMass"),
                "Savin Hill": Stop("place-shmnl", "Savin Hill"),
                "Fields Corner": Stop("place-fldcr", "Fields Corner"),
                "Shawmut": Stop("place-smmnl", "Shawmut"),
                "Ashmont": Stop("place-asmnl", "Ashmont"),
                "North Quincy": Stop("place-nqncy", "North Quincy"),
                "Wollaston": Stop("place-wlsta", "Wollaston"),
                "Quincy Center": Stop("place-qnctr", "Quincy Center"),
                "Quincy Adams": Stop("place-qamnl", "Quincy Adams"),
                "Braintree": Stop("place-brntn", "Braintree")}
    # Red Line Route
    route = Route("Red", "Red Line", ["South", "North"])
    #!IMPORTANT! This value must be updated before every test
    testTime = "2020-10-21T11:13:37-04:00"

    # Test to retrieve the list of heavy and light trains
    def test_getRoutes(self):
        result = App.getRoutes("0,1")
        for route in result:
            self.assertTrue(route in self.routeDict)

    # Test to retrieve stops from the Red Line
    def test_getStops(self):
        result = App.getStops(self.route)
        for stop in result:
            self.assertTrue(stop in self.stopDict)

    # Test the prediction based on the given values
    def test_getPrediction(self):
        route = self.route
        stop = Stop("place-alfcl", "Alewife")
        direction = Direction("1", "North")
        currentTime = datetime.datetime.now(timezone("US/Eastern"))
        testTime = dateutil.parser.parse(self.testTime)
        testPrediction = testTime-currentTime
        test = int(testPrediction.seconds/60)
        result = App.getPrediction(route, stop, direction)
        self.assertEqual(result, test)

    # Check if route is being properly selected
    @mock.patch('Numerated_Challenge.input', create=True)
    def test_selectRoute(self, mocked_input):
        mocked_input.side_effect = ['Red Line']
        test = Route("Red", "Red Line", ["South", "North"])
        result = App.selectRoute(self.routeDict)
        self.assertEqual(result.id, test.id)
        self.assertEqual(result.name, test.name)
        self.assertEqual(result.directions, test.directions)
    # Check if direction is being properly selected

    @mock.patch('Numerated_Challenge.input', create=True)
    def test_selectDirection(self, mocked_input):
        mocked_input.side_effect = ["South"]
        test = Direction("0", "South")
        result = App.selectDirection(self.route)
        self.assertEqual(result.id, test.id)
        self.assertEqual(result.name, test.name)
    # check if stop is being properly selected

    @mock.patch('Numerated_Challenge.input', create=True)
    def test_selectStop(self, mocked_input):
        mocked_input.side_effect = ['Alewife']
        test = Stop("place-alfcl", "Alewife")
        result = App.selectRoute(self.stopDict)
        self.assertEqual(result.id, test.id)
        self.assertEqual(result.name, test.name)


if __name__ == '__main__':
    unittest.main()
