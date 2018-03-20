"""
File which will test the implementation of the 
TwentyFortyEight class
"""
class TestSuite():
    """
    Class which will run a suite of tests
    on a 2048 class
    """
    def __init__(self, inst):
        self.to_test = inst
    
    def test_str(self, obj):
        print obj.__str__()
        
    def test_new_tile(self, obj):
        trigger = False
        while not trigger:
            trigger = obj.new_tile()
            print obj.__str__()
        print obj.__str__()
    
    def run_suite(self):
        # test __str__() method
        print self.test_str(self.to_test)
        
        # set a unique value to determie if 
        # anything overwritten
        self.to_test.grid[0][0] = 10
        
        # test that the new_tile method trips
        # when all cells are full
        self.test_new_tile(self.to_test)
        
        
        
        
#class Thing():
#    def __str__(self):
#        return "ababa"

#thing = Thing()     
#test = TestSuite(thing)
#test.run_suite()
