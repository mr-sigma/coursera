"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    if len(line) < 2:
        return line
    slide_line = slide(line)
    for i in range(len(slide_line) - 1):
        try:
            if slide_line[i] == 0:
                continue
            if slide_line[i] == slide_line[i+1]:
                slide_line[i] *= 2
                slide_line[i+1] = 0
                continue
        except IndexError:
            continue
    return slide(slide_line)

def slide(lst):
    """
    Function to slide over numbers in a list
    """
    slide_line = [x for x in lst if x != 0]
    while len(slide_line) < len(lst):
        slide_line.append(0)
    return slide_line

#print merge([2,0,2,4]) == [4, 4, 0, 0]
#print merge([0, 0, 2, 2]) == [4, 0, 0, 0]
#print merge([2, 2, 0, 0]) == [4, 0, 0, 0]
#print merge([2, 2, 2, 2, 2]) == [4, 4, 2, 0, 0]
#print merge([8, 16, 16, 8]) == [8, 32, 8, 0]
#
#print merge([])
#print merge([1])
#print merge([1,1])
#print merge([0,1])
#print merge([0,1,2])
