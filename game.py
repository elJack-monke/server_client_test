# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 00:47:51 2021

@author: eljac
"""

class game_cl():
    def __init__(self, id):
        self.p1_went = False  # Check if players have made their move yet
        self.p2_went = False
        self.ready = False    # If two players waiting to join game -> ready to start
        self.id = id          # Store game id -> allows for multiple games to be run
        self.moves = [None, None]
        self.wins = [0,0]  # Store number of wins/loses/ties for scorekeeping
        self.ties = 0

    def get_player_move(self, p):
        ''' p = player_id = [0, 1] '''
        return self.moves[p]

    def play(self, player, move):  # store whatever move was selected by the player
        self.moves[player] = move
        if player == 0: self.p1_went = True
        else: self.p2_went = True

    def connected(self): return self.ready

    def both_went(self): return self.p1_went and self.p2_went  # check if both players have went -> can reveal if so

    def winner(self):  # determine winner

        p1 = self.moves[0].upper()[0]   # Take first char from rock/paper/scissors for comparison
        p2 = self.moves[1].upper()[0]

        winner = -1  # handles a tie
        if p1+p2 in ['RS', 'PR', 'SP']: winner = 0
        elif p2+p1 in ['RS', 'PR', 'SP']: winner = 1
        return winner

    def reset_went(self):
        self.p1_went = False
        self.p2_went = False








