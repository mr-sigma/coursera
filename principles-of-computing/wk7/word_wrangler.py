"""
Student code for Word Wrangler game

Can't use set, sorted, or sort

Always return a new list (no working in place)
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list (ascending).

    Returns a new sorted list with the same elements in list1, but
    with no duplicates (ascending).

    This function can be iterative.
    """
    new_list = []
    
    for element in list1:
        if element not in new_list:
            new_list.append(element)
    return new_list

def binarySearch(alist, item):
        first = 0
        last = len(alist)-1
        found = False
    
        while first<=last and not found:
            midpoint = (first + last)//2
            if alist[midpoint] == item:
                found = True
            else:
                if item < alist[midpoint]:
                    last = midpoint-1
                else:
                    first = midpoint+1
    
        return found, value

def intersect(list1, list2):
    new_list = []
    index = 0
    length2 = len(list2)
    for element in list1:
        while True:
            if index == length2:
                break
            if element == list2[index]:
                new_list.append(element)
                index += 1
                break
            else:
                index += 1
    return new_list

def intersect3(list1, list2):
    """
    Retry intersect function to speed it up
    
    Returns a new sorted list containing only elements that are
    in both list1 and list2
    """
    new_list = []
    for element in list1:
        found = False
        first = 0
        last = len(list2)
        while first <= last and not found:
            midpoint = (first + last) // 2
            if list2[midpoint] == element:
                new_list.append(element)
                found = True
            else:
                if element < list2[midpoint]:
                    last = midpoint - 1
                else:
                    first = midpoint + 1
    return new_list

def intersect2(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    new_list = []
    
    for element1 in list1:
        if element1 in list2:
            new_list.append(element1)
    return new_list

# Functions to perform merge sort
        
def merge(list1, list2):
    """
    Merge two sorted lists (ascending).

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    list1_cp = list1[:]
    list2_cp = list2[:]
    new_list = []
    
    while True:
        if len(list1_cp) == 0:
            new_list.extend(list2_cp)
            break
        elif len(list2_cp) == 0:
            new_list.extend(list1_cp)
            break
        to_add = list1_cp.pop(0) if list1_cp[0] <= list2_cp[0] else list2_cp.pop(0)
        new_list.append(to_add)
        
    return new_list
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    # check if the list length is 1
    if len(list1) < 2:
        # if yes, return the list (sorted)
        return list1
    else:        
        # if no, cut the list in half (rounded) and
        # call merge sort again on both halves
        mid_index = int(math.floor(len(list1) / 2))
        list_a = merge_sort(list1[:mid_index])
        list_b = merge_sort(list1[mid_index:])
        # merge the two halves back together and return
        return merge(list_a, list_b)
    
# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    # if string is length 1, return "" and itself
    if word == "":
        return [""]
    else:
        # split the word into the first character and the rest
        first = word[0]
        rest = word[1:]
        # gen all strings for the rest of the word
        rest_strings = gen_all_strings(rest)
        # for all strings in rest_strings insert first
        # into every possible position (separate list)
        combos = []
        for string in rest_strings:
            for index in range(len(string) + 1):
                combos.append(str(string[0:index]) + first + str(string[index:]))
    
    return combos + rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    dictionary = []
    f_open = urllib2.urlopen(codeskulptor.file2url(filename))
    for line in f_open:
        dictionary.append(line.strip())
    return dictionary

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

# print remove_duplicates([1,1,2,2,3,3,4,1,1,1])    
# print intersect([1,2,3,4],[1,2,3,5,6]) 
# print intersect2([1,2,3,4],[1,2,3,5,6]) 
# print merge([1,2,3,4],[1,2,3,5,6])
# print merge([1,3,5,7,8], [2,4,6,8,9])
# print merge_sort([2,5,17,2,5,1,2,1])
# print gen_all_strings("ab")   
# print len(gen_all_strings("eating"))
# print load_words(WORDFILE)
