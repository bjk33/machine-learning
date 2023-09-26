import random


class NimGame:
    """ Class to keep track of a nim game. """

    def __init__(self, starting_piles):
        """
        Construct a new game with the list starting_piles 
        as the piles
        """
        self.piles = starting_piles[:]

    def get_piles(self):
        """ Returns a copy of the current piles """
        # return a copy to avoid messing with the internal
        # state of the game
        return self.piles[:]

    def make_move(self, pile_number, num_to_remove):
        """ 
        Move num_to_remove from pile_number.
        
        Return True if the move was valid, False otherwise.
        """
        if pile_number < 0 or pile_number >= len(self.piles):
            return False
        elif num_to_remove < 0 or num_to_remove > self.piles[pile_number]:
            return False
        else:
            self.piles[pile_number] -= num_to_remove
            return True

    def is_over(self):
        """ Is the game over? """
        return sum(self.piles) == 0

    def __str__(self):
        return str(self.piles)


def play_nim(player1, player2, game_state):
    # player1 will start
    player1_turn = True
    legal_move = True

    while not game_state.is_over() and legal_move:
        if player1_turn:
            print("Player 1's turn")
            print(game_state)
            (pile_number, num_to_remove) = player1(game_state.get_piles())
            print("Player 1:", end='')
        else:
            print("Player 2's turn")
            print(game_state)
            (pile_number, num_to_remove) = player2(game_state.get_piles())
            print("Player 2:", end='')

        print(str(num_to_remove) + " from pile " + str(pile_number))
        print()

        if not game_state.make_move(pile_number, num_to_remove):
            print("ILLEGAL MOVE!")
            legal_move = False
            player1_turn = not player1_turn

        player1_turn = not player1_turn

    # game's over, see who won
    if player1_turn:
        print("Player 2 won!")
    else:
        print("Player 1 won!")


def human_player(piles):
    print_piles_with_indices(piles)

    pile = -1

    while pile < 0 or pile >= len(piles) or \
            piles[pile] <= 0:
        pile = int(input("Enter the pile number: "))
        pile = pile - 1

    num_to_move = -1

    while num_to_move < 0 or num_to_move > piles[pile]:
        num_to_move = int(input("Enter num to remove: "))

    return pile, num_to_move


def print_piles_with_indices(piles):
    str_piles = str(piles)

    prev = 0
    next_comma = str_piles.find(",")
    count = 1
    line = ""

    while next_comma != -1:
        line += " " * (next_comma - prev - 1)
        line += str(count)
        prev = next_comma
        count += 1
        next_comma = str_piles.find(",", prev + 1)

    line += " " * (len(str_piles) - prev - 2)
    line += str(count)
    print(line)


def nim2_strategy(piles):
    """ A strategy for 2-pile nim that tries to keep the piles equal. """

    if piles[0] > piles[1]:
        pile_number = 0
        num_to_move = piles[0] - piles[1]
    elif piles[1] > piles[0]:
        pile_number = 1
        num_to_move = piles[1] - piles[0]
    else:
        # doh, they're already equal :(
        pile_number = 0
        num_to_move = 1

    return (pile_number, num_to_move)


def random_nim_strategy(piles):
    """ Pick a random pile and a random number to remove in that pile """

    # get all the non_zero_piles
    non_empty = []

    for i in range(len(piles)):
        if piles[i] > 0:
            non_empty.append(i)

    pile_number = random.choice(non_empty)
    num_to_remove = random.randint(1, piles[pile_number])

    return pile_number, num_to_remove
