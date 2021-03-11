# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 16:42:17 2021

@author: eljac
"""

import pygame
from network import network
#import pickle
pygame.font.init()

width, height = 700, 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

# Define some RGB tuple colours
LIGHT_ORANGE, TEAL, LILAC, PURPLE = (255,153,0), (0,128,128), (153,153,255), (51,51,153)
WHITE, BLACK, GREY, RED, GREEN, BLUE= (255,255,255), (0,0,0), (150,150,150), (220,0,0), (0,255,0), (0,0,255)

class button():
    def __init__(self, text, x, y, colour, w=150, h=100):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = w
        self.height = h

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('Times New Roman', 40)
        text = font.render(self.text, 1, WHITE)
        # Some maths to center the text in the button, using the size of the button and text
        win.blit(text, ( self.x + round(self.width/2) - round(text.get_width()/2) , self.y + round(self.height/2) - round(text.get_height()/2) ))

    def click(self, pos):
        x1, y1 = pos  # Check if the click is inside the bounds of the button
        return True if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height else False



def redraw_window(win, game, p):
    win.fill(GREY)

    if not game.connected():  # if only one players connected -> print waiting
        font = pygame.font.SysFont('Times New Roman', 80)
        text = font.render('Waiting for player...', 1, BLACK)  # True for bold
        win.blit(text, ( width/2 - text.get_width()/2, height/2 - text.get_height()/2 ) )
    else: # if we are connected
        font = pygame.font.SysFont('Times New Roman', 60)
        text = font.render('Your Move', 1, LIGHT_ORANGE)
        win.blit(text, ( 60, 200 ))

        text = font.render('Opponents', 1, LIGHT_ORANGE)
        win.blit(text, ( 380, 200 ))


        # Get the two players moves -> check if they've both gone -> if so, display
        move1, move2 = game.get_player_move(0), game.get_player_move(1)
        if game.both_went():  # If both players have gone, show both moves on screen
            text1 = font.render(move1, 1, BLACK)
            text2 = font.render(move2, 1, BLACK)

        else:  # if one (or no) players have gone
            if game.p1_went and p==0:  # If we are p1 and have gone, show our move
                text1 = font.render(move1, 1, BLACK)
            elif game.p1_went:  # If we are NOT p1 but p1 has gone, show 'locked in'
                text1 = font.render('Locked in', 1, BLACK)
            else:  # if we are not p1 and they have not gone, show 'waiting'
                text1 = font.render('Waiting...', 1, BLACK)

            if game.p2_went and p==1:  # If we are p1 and have gone, show our move
                text2 = font.render(move2, 1, BLACK)
            elif game.p2_went:  # If we are NOT p1 but p1 has gone, show 'locked in'
                text2 = font.render('Locked in', 1, BLACK)
            else:  # if we are not p1 and they have not gone, show 'waiting'
                text2 = font.render('Waiting...', 1, BLACK)

        if p==1:  # draw the text so that client always apears on the LHS
            win.blit(text2, (80, 350)), win.blit(text1, (400, 350))
        else:
            win.blit(text1, (80, 350)), win.blit(text2, (400, 350))

        for btn in btns:  # draw the buttons... easier than the text
            btn.draw(win)

    pygame.display.update()  # finally update window with our desired positions.


btns = [button('Rock', 50, 500, BLACK), button('Scissors', 250, 500, RED),\
        button('Paper', 450, 500, BLUE), button('back', 50, 50, (135,135,135), 80, 30)]
def main():
    run = True
    clock = pygame.time.Clock()
    n = network()
    p = int( n.get_p() )  # get player number
    if p == 9:
        print('server error\n'); pygame.quit()
    print('You are player {}\n'.format(p))  # check previous line worked

    while run:  # Main game loop here
        clock.tick(60)
        # Every tick, want sever to send the current game state
        try: game = n.send('get')
        except:
            run = False
            print( "Could not get game :(" )
            break

        if game.both_went():  # Check if both players have gone in the updated game from server
            redraw_window(win, game, p)
            pygame.time.delay(690)  # delay in ms to allow for latency etc.
            try: game = n.send('reset')
            except:
                run = False
                print( "Could not get game :(\n" )
                break

            # Check who won and print message to the screen if player 0 won and this client instance is player 0 -> print 'Won' etc.
            font = pygame.font.SysFont('Times New Roman', 90)
            if (game.winner() == 1 and p == 1) or (game.winner() == 0 and p == 0):
                text = font.render('You Won! :D', 1, RED)
            elif game.winner() == -1:
                text = font.render('Tie Game! :O', 1, RED)
            else:
                text = font.render('You lost! D:', 1, RED)
            win.blit(text, ( width/2 - text.get_width()/2, height/2 - text.get_height()/2 ) )
            pygame.display.update()
            pygame.time.delay(1000)  # pause 1 second before displaying result

        # Handle all events in the pygame window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if top right x is clicked
                run = False     # If window is closed, tell the server client has pressed
                n.send('back')  # 'back' button so server knows to disconnect them
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # If a mousebutton is pressed
                pos = pygame.mouse.get_pos()  # get position of click
                for btn in btns:  # Check if clicked position conincides with one of the buttons
                    if btn.click(pos) and game.connected():  # Make sure both players are connected before enabling buttons
                        if btn.text == 'back':
                            print('yep')
                            n.send(btn.text)
                            return
                        else:
                            if p == 0 and not game.p1_went:  # if we are player 1 have not already made our move
                                n.send(btn.text)
                            elif p == 1 and not game.p2_went: # if we are player 2 have not already made our move
                                n.send(btn.text)

        redraw_window(win, game, p)


# Menu screen while waiting for another player or when other player disconnects
def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(BLACK)
        font = pygame.font.SysFont('Times New Roman', 60)
        text = font.render('Click to play!', 1, LILAC)  # True for bold
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    # Run main if screen clicked
    main()


# run da ting
while True:  # If main exits (some error or a player leaves) bring other player back to menu screen rather than crashing...
    menu_screen()

# if main exits ('could not get game' error)
pygame.quit()

