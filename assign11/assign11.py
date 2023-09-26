# Brandon Kaplan; CS51A; Section 1; Assignment 11; 4/25/2022

# import packages
from nimsupport import *


# Team name: "Brandon's Nim Player" b/c no one wants me to be in their group :(
"""

My strategy makes use of some cool properties from combinatorial game theory. Because I didn't have a partner I thought
it would be okay to play against a computer online. I also read about the Sprague-Grundy theorem and I learned that the 
strategy to playing the game nim in the "normal" fashion (i.e., the way we play where the winner takes the last stone) 
has more general implications for impartial games (i.e., games where moves are independent of who is playing depending
only on position and the payout is symmetric). I thought this was interesting and I actually tried playing other 
impartial games such as "brussels sprouts" with my housemate following the more trivial strategy for playing nim with 
a single pile. In a nutshell, my strategy exploits a fundamental feature of the game of nim: in a given turn, a player 
can only making a winning move or a losing move and there are only winning states/positions of the game and losing 
states/positions. Because there are only two players the optimal strategy becomes a matter of converting every 
losing state into a winning state on your turn. To determine whether or not a given board state is a winning or losing 
state I convert the number of stones in each pile from their decimal number to their binary number. Then I calculate
the cumulative XOR of the number of stones in each pile (basically add the columns bitwise modulo 2). This cumulative
XOR can be calculated at any state of the game and is called the nim-sum. Now, a winning state always has a nim-sum 
equal to 0 while a losing state is any combination of piles with a nim-sum greater than 0. If a player inherits a board 
state with a nim-sum greater than 0 they must always remove stones such that the resulting piles have a nim-sum of 0. 
If a player doesn't manipulate the piles to result in a 0 nim-sum they are not playing optimally and have a worse chance
at winning. Thus, assuming both players play with optimal strategy, if the starting state of the board is a losing state
(i.e., has non-zero nim-sum) then the first player will always win. On the other hand, if the starting state of the 
board is a winning state then the first player to pick always loses! The player can actually implement this strategy 
(convert losing states into winning states) by manipulating the binary notation of the number of stones in each pile. 
The idea is to flip 1s into 0s such that when summing column-wise every 1 will be paired with another 1 resulting in a 
zero in every column (a nim-sum equal to 0). Since each turn a player can only manipulate one row (take from a single 
pile) any move from a winning state will result in a losing state.

I came to this strategy by starting with a more simple version of the problem at hand. I thought about, and spoke with 
my housemate the simplified game of nim where number of stones in each pile is uniform (i.e., every row in binary 
notation is the same). It was immediately clear what the optimal strategy would be in this case because with uniform 
number of stones per pile, every pile could be treated the same and the winner could be predicted if one knew if the 
number of piles of stones was odd or even. This was a special case of the strategy I ended up implementing. Essentially,
if there were an even number of piles the resulting nim-sum of the start state is always 0 because each bit is paired
with another. If there were were an odd number of piles the nim-sum of the start state is always non-zero and so the 
start state is a losing state. I got the idea to add the binary notations up column-wise from reading about GF(2) on 
wiki. I learned that GF(2) is the unique field with two elements, its additive and multiplicative identities are 0 and 1
respectively. Implementing vector addition on this field seemed like one of GF(2)'s compsci applications: "The elements 
of GF(2) may be identified with the two possible values of a bit and to the boolean values true and false. It follows 
that GF(2) is fundamental and ubiquitous in computer science and its logical foundations." (source: GF(2) wiki).
"""
# Below I will write a couple helper functions to assist my strategy.


def num_to_bin_list(num):
    """
    This function takes in a decimal integer (num) as parameter and returns a list containing the integer in binary
    notation. I.e., each element of the list corresponds to one bit making up the number. If you read the output list
    from left to right you would have the binary number form of input decimal integer (num).
    :param num:
    :return: bin_lst: a list where every element is either a 0 or a 1
    """
    # construct a list by iterating over each character in the string bin(num) and for each character in the string from
    # index 2 onward store the character as an element in binlst.

    # slice from index 2 until end of string is b/c bin(num) returns two unwanted characters denoting this number is
    # a binary number but this isn't part of the number itself.
    bin_lst = [c for c in bin(num)[2:]]
    return bin_lst


def nimsum(lst):
    """
    This function takes in a list representing the state of the board (each element corresponds to one pile and the
    element itself denotes the number of stones in that pile) as parameter and returns an integer value I call the
    nim_sum. The nim_sum is the sum of the elements of the input list when summed using the XOR operation. I.E., the
    bitwise XOR over the elements of the input list.
    :param lst: a list of piles of various sizes
    :return: nimsum: an integer
    """
    nim_sum = 0  # initialize nim_sum at 0

    # iterate over every element in the input list
    for i in lst:
        # cumulative XOR i.e., bitwise addition modulo 2
        nim_sum = nim_sum ^ i  # ^ compares nim_sum & element bitwise outputs a 0 if the bits are the same, 1 otherwise
    return nim_sum


def check_flips(lst):
    """
    This function takes in a list representing the state of the board (each element corresponds to one pile and the
    element itself denotes the number of stones in that pile) as parameter and returns a list named flips which contains
    the positions of the bits which are equal to 1. Note how this list of positions counts starting at len(nim_lst) - i
    and moves right to left so the if the bit element at the 0th index is a 1 this will be represented in the flips
    list as adding an element equal to len(nim_list) - 0 to flips (this will always be at least 1).
    :param lst: a list representing the state of the game
    :return flips: a list of positions to potentially swap 0 in place of 1
    """
    nim_lst = num_to_bin_list(nimsum(lst))  # define nim_lst as binary list form of nim_sum when param lst is passed
    flips = []  # define flips as empty list

    # iterate over each element (bit) in the list we just built
    for i in range(len(nim_lst)):
        # if element indexed at the ith position is a 1
        if nim_lst[i] == '1':
            flips.append(len(nim_lst) - i)  # add the integer i less than the number of bits in nim_lst to flips
    return flips


def valid_flip(pos, num):
    """
    This function takes in position (an integer) and number (an integer) as parameters and returns a boolean. Position
    is a bit position like an element of the output of check_flips(lst).  Number is a number that denotes the number of
    stones in a given pile. True indicates flipping the bit is valid and False indicates otherwise.
    :param pos: an integer
    :param num: an integer
    :return: a boolean
    """
    num_lst = num_to_bin_list(num)  # define a binary list corresponding to bits of parameter num
    check = len(num_lst) - pos  # define check as the number of bits in the binary list minus parameter pos

    # if check is negative (i.e., if the position passed as parameter is greater than the number of elements in num_lst,
    # that is to say the number of bits in the binary form of num passed as parameter)
    if check < 0:
        return False  # then this is not a valid bit to flip from 1 to 0

    # if the element of num_lst indexed at number of elements minus pos is a 1
    elif num_lst[check] == '1':
        return True  # then this is a valid bit to flip

    # otherwise, if the element of num_lst indexed at number of elements minus pos is a 0
    else:
        return False  # then this is also not a valid bit to flip (it isn't a 1)


def remove(flips, num):
    """
    This function takes in a list named flips (like the output of check_flips(lst)) and number (an integer) as
    parameters and returns an integer named diff that represents the amount of stones I should remove from the pile w/
    number of stones equal to num passed as parameter.
    :param flips: a list containing positions to flip
    :param num: an integer: the number of stones in the pile I seek to remove stones from
    :return diff: an integer:  the number of stones to remove from the pile I seek to remove stones from
    """
    new_num = num_to_bin_list(num)  # initialize new_num as the list containing the binary bits of num passed as param

    # iterate over each element in list named flips passed as param
    for i in flips:
        # index to position equal to number of bits in num minus i and fix it as a string representation of 1 minus
        # the integer element of new_num indexed at the position equal to number of bits in num minus i
        new_num[len(new_num) - i] = str(1 - int(new_num[len(new_num) - i]))

    new_num = int("".join(new_num), 2)  # set new_num to integer object of new_num list joined by whitespace (base 2)
    diff = num - new_num  # define difference as num passed as param minus the integer object new_num

    return diff  # number of stones to remove

# Below is my Nim Player


def nim_strategy(lst):
    """
    This method is our Nim Player. It takes in a list representing the state of the board (each element corresponds to
    one pile and the element itself denotes the number of stones in that pile) as parameter and returns a tuple the
    first element is the index of the pile I want to remove stones from and the second element is the number of stones
    I want to remove.
    :param lst: a list representing the state of the game
    :return: a tuple: contains the move making instructions
    """
    flips = check_flips(lst)  # initialize flips as the output of check_flips having passed lst
    # if flips is non-empty
    if flips:
        pos = flips[0]  # fix pos as first element in flips
        # iterate over piles
        for pile in range(len(lst)):
            # if it is valid to flip at positions in pile
            if valid_flip(pos, lst[pile]):
                return pile, remove(flips, lst[pile])  # return the tuple (pile number, number of stones to remove)
    else:
        return 0, 1  # otherwise, remove one stone from the first pile every time to draw out the game
