import socket
import pickle
import _thread as th  # need to have clients on separate threads so they can run concurrently
from game import game_cl

PORT = 5569
SERVER = '10.6.50.178'#socket.gethostbyname(socket.gethostname())  # local host IP address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # INET = internet, SOCK_STREAM = stream information through the socket
try:   s.bind(ADDR)  # try/except block in case port is not available
except socket.error as e: print(str(e))

s.listen(2)
print('Server Started')

# Storing dictionary of game IDs in a list
connected = set()
games = {}
id_count = 0

def threaded_client(conn, p, game_id):
    global id_count
    conn.send( str.encode(str(p)) )  # player is current_player = int, pos is the current stored position, make_pos converts to str, which is then encoded and sent

    run1 = True
    while run1:
        try: # Send get/reset/move to server & game -> receive back a diferent answer depending on that
            data  = conn.recv(4096).decode()  # read the data sent by the client

            if game_id in games:  # Check if game still exists each iteration
                game = games[game_id]

                if not data:
                    break  # if no message received
                else:
                    if data == 'reset':  # if client requests a reset, call game reset function
                        game.reset_went()
                    elif data != 'get':  # if not reset or get, then must be move, update current players selected move
                        game.play(p, data)

                    conn.sendall( pickle.dumps(game) )  # send game object to all the clients

                    # error reading an empty pickle if we break before the conn.sendall line
                    if data == 'back': break

            else: break  # if game no longer exists, break
        except: break  # if there's an error receiving data, break

    id_count -= 1
    print('Lost connection: players = {}'.format(id_count))
    try:
        del games[game_id]  # if both players disconnect at same time, will try and delete game twice -> need try block
        print('Closing game {}'.format(game_id+1))
    except:
        print('Game already closed.\n')

    conn.close()


conns = []
run = True
while run:
    print('Waiting for connection...')
    conn, addr = s.accept()
    print('Connected to: {}'.format(addr))
    conns.append(conn)

    id_count += 1
    p = 0
    game_id = (id_count - 1)//2  # 1 game for every two players
    print('Games: {}\tPlayers: {}'.format(game_id+1, id_count))
    if id_count%2 == 1:    # if odd number of players when one joins -> create new game
        games[game_id] = game_cl(game_id)  # create new game if odd numbers of players
        print('Creating new game...')
    else:  # if even number of players, send new player to game with one player already waiting and start that game
        try: games[game_id].ready = True
        except:
            print('\nServer error: game_id higher than num of games\n')
            for conn in conns: conn.close()
            continue
        p = 1

    th.start_new_thread(threaded_client, (conn, p, game_id))


