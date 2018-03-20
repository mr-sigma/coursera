"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 1000
# 3999999999.0 * 4

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies = float(0)
        self._cps = float(1)
        self._total_cookies_produced = float(0)
        self._time = float(0)
        # history defined as:
        # (time, item_bought = None, item_cost, 
        # total_cookies_produced)
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        to_return = ""
        to_return += "Time: " + str(self._time)
        to_return += "\nTotal Cookies Produced: "
        to_return += str(self._total_cookies_produced)
        to_return += "\nCPS: " + str(self._cps) + "\n"
        return to_return
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return float(self._cookies)
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return float(self._cps)
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return float(self._time)
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        time_remaining = math.ceil((cookies - self._cookies) / self._cps)
        if time_remaining < 0.0:
            return 0.0
        else:
            return float(time_remaining)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        else:
            self._time += time
            cookies_generated = self._cps * time
            self._total_cookies_produced += cookies_generated
            self._cookies += cookies_generated
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state and history

        Should do nothing if you cannot afford the item
        
        (time, item, cost of item, total cookies)
        """
        if cost > self._cookies:
            # print "Cannot afford", str(item_name)
            return
        else:
            self._cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost,
                            self._total_cookies_produced))
            return
   
    
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    
    # Thinking that the the function should pass most
    # of the work to the strategy function
    cookie_clicker = ClickerState()
    
    while cookie_clicker.get_time() <= duration:
        time_left = duration - cookie_clicker.get_time()
        # strategy tells what item to buy
        # may get really intentse with best strat
            # which will incorporate a cps/$$ calculation
        to_buy = strategy(cookie_clicker.get_cookies(), 
                          cookie_clicker.get_cps(),
                          cookie_clicker.get_history(),
                          time_left,
                          build_info.clone())
        # if strategy returns None, break the loop (nothing left to buy or 
        # out of time
        if to_buy == None:
            cookie_clicker.wait(time_left)
            break
        else:
            item_cost = build_info.get_cost(to_buy)    
            item_cps = build_info.get_cps(to_buy)
            # calculate the time required to wait (Might already be done by the strat
            to_wait = cookie_clicker.time_until(item_cost)
            
            # check that we can buy the item
            if to_wait > time_left:
                cookie_clicker.wait(time_left)
                break
            else:
                # wait the required amount of time
                cookie_clicker.wait(to_wait)
                # buy the item and update the history & build_info
                cookie_clicker.buy_item(to_buy, item_cost, item_cps)
                build_info.update_item(to_buy)
        
    return cookie_clicker


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    cookies_to_be_had = cookies + cps * time_left
    if build_info.get_cost("Cursor") > cookies_to_be_had:
        return None
    else:
        return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    # find the minimum item
    item_list = build_info.build_items()
    min_cost = float("inf")
    min_item = ""
    for item in item_list:
        item_cost = build_info.get_cost(item)
        if item_cost < min_cost:
            min_cost = item_cost
            min_item = item
    # determine if we can afford it before time expires
    cookies_to_be_had = cookies + cps * time_left
    # return None if we can't afford it 
    if cookies_to_be_had < min_cost:
        return None
    else:
        return min_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    # find the maximum cookies we can spend
    cookies_to_be_had = cookies + cps * time_left
    item_list = build_info.build_items()
    max_cost = float("-inf")
    max_item = None
    for item in item_list:
        item_cost = build_info.get_cost(item)
        # find the most expensive item we can afford
        if item_cost > max_cost and item_cost <= cookies_to_be_had:
            max_cost = item_cost
            max_item = item
    
    return max_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    cookies_to_be_had = cookies + cps * time_left
    item_list = build_info.build_items()
    best_cps_per_cost = 0
    best_item = None
    for item in item_list:
        # find the cps/cost or each item
        item_cost = build_info.get_cost(item)
        item_cps_per_cost = build_info.get_cps(item) / item_cost
        if item_cps_per_cost > best_cps_per_cost \
        and item_cost <= cookies_to_be_had:
            best_item = item
    # return item with the maximum cps/cookie
    return best_item
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    # print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 
    #                       'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("None", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
# run()
