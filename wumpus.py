import file_logic as fl
from agent import RandomAgent
from agent import AlphaBetaAgent
from board import Board
import sys

random_agent = RandomAgent(sys.argv[1])
alphabeta_agent = AlphaBetaAgent(sys.argv[1])
board = Board([[-1] * 15 for _ in range(15)])

initialized = False

while fl.wait_for_file(fl.endFilePath):
    while fl.wait_for_file(fl.goFilePath):
        continue

    print("Taking turn...")
    moveFile = open(fl.moveFilePath, "r")
    if not initialized:
        initialized = True
        readMove = moveFile.read()
        if len(readMove) > 0:
            alphabeta_agent.player = 1
            print("Reading opponent's move")
            readGo = fl.interpret_move(readMove, int(not alphabeta_agent.player))
            board.update_board(readGo[0], readGo[1], readGo[2])
        else:
            alphabeta_agent.player = 0
    else:
        print("Reading opponent's move")
        readGo = fl.interpret_move(moveFile.read(), int(not alphabeta_agent.player))
        board.update_board(readGo[0], readGo[1], readGo[2])

    print("Deciding...")
    move = alphabeta_agent.take_turn(board)
    print("Placing piece in: {0}, {1}".format(fl.convert_num_to_alphabet(move[1]), move[2] + 1))
    board.update_board(alphabeta_agent.player, move[1], move[2])
    moveFile = open(fl.moveFilePath, "w")
    moveFile.write("{0} {1} {2}".format(alphabeta_agent.name, fl.convert_num_to_alphabet(move[1]), move[2] + 1))
    moveFile.close()
    while not fl.wait_for_file(fl.goFilePath):
        if not fl.wait_for_file(fl.endFilePath):
            break


