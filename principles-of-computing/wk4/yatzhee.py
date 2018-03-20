"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    # loop through to create lists up to length
    for dummy_idx in range(length):
        temp_set = set()
        # one item in answer_set?
        for partial_sequence in answer_set:
            # for each of the outcomes
            for item in outcomes:
                new_sequence = list(partial_sequence)
                # add the outcome to the sequence (single item)
                # then append the sequence to the set (list of items)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    max_score = 0
    # iterate through unique dice values in the hand
    for num in set(hand):
        num_score = 0
        # iterate through all dice in hand
        for die in hand:
            # if the die is the current number
            # add the die value to the current score
            if die == num:
                num_score += die
        # update score maximum
        max_score = max(max_score, num_score)
    return max_score

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    # going to have to call gen all sequences on the dice
    # we choose to reroll
    # may have to use gen all holds to cerate the set of
    # outcomes to feed to get all sequences
    outcomes = range(1, num_die_sides + 1)
    rolls = gen_all_sequences(outcomes, num_free_dice)
    total = 0
    for roll in rolls:
        total += score(held_dice + roll)
    return float(float(total)/float(len(rolls)))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set()
    temp_list = [[]]
    for dice in hand:
        for entry in temp_list[:]:
            entry_copy = entry[:]
            entry_copy.append(dice)
            temp_list.append(entry_copy)
    for entry in temp_list:
        answer_set.add( tuple(entry) )
    return answer_set 



def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    hold_max = ()
    max_expected = 0
    holds = gen_all_holds(hand)
    # loop through all possible holds
    for hold in holds:
        # calculate expected value for the reroll
        temp_expected = expected_value(hold, num_die_sides, 
                                       len(hand) - len(hold))
        # find the best expected score
        if temp_expected > max_expected:
            hold_max = hold 
            max_expected = temp_expected
    return (max_expected, hold_max)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 1, 1)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
    
run_example()


# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
