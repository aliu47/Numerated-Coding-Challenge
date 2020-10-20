import unittest
from Numerated_Coding_Challenge import App 

class Tests(unittest.TestCase):
    def test_getRoutes(self):
        a = App.getRoutes("0")
        print(a)
        self.assertEqual(a,"{'Mattapan Trolley': <Numerated_Coding_Challenge.Route object at 0x04244B10>, 'Green Line B': <Numerated_Coding_Challenge.Route object at 0x04244B30>, 'Green Line C': <Numerated_Coding_Challenge.Route object at 0x04244B50>, 'Green Line D': <Numerated_Coding_Challenge.Route object at 0x04244B70>, 'Green Line E': <Numerated_Coding_Challenge.Route object at 0x04244B90>}")


    def test_getStops(self):
        print()


    def test_getPrediction(self):
        print()


    def test_selectRoute(self):
        print()


    def test_selectStop(self):
        print()


    def test_selectDirection(self):
        print()

if __name__ == '__main__':
      unittest.main() 
