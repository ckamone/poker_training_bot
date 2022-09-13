from classes import *
from sim import *


def getGame():
    start_sim=0
    opHand=0
    while round(start_sim)>=90 or round(start_sim)<=10 or opHand<=10: #избегаем 100% и 0% раздачи и раздачи, с ужасной рукой у опонента(1 из 10 ужасные руки пропускаем)
        # get class
        k = Koloda()

        # get ranks and suits
        r = k.card_ranks()
        s = k.card_suitL()

        cardL = k.allCards_list(r, s)  # spisok 52 karty
        # print('spisok iz 52 kart\n', cardL)

        # get straight cards
        stR = k.card_straightRanks()  # get ranks in straight type
        strL = k.genDraw_list(stR, s)  # get 4 straight cards
        # print('spisok iz straightDraw kart\n', strL)

        # get shuffled deck with draw
        draw = k.getDraw(strL, cardL)
        # print('gen 4 draw\n', len(draw), draw)

        drawH = k.getDrawHand(draw)
        # print('create hand1\n', drawH, len(draw))

        board = k.getDrawBoard(draw)
        # print('create board\n', board, len(draw))

        opCards = k.getOpHand(draw)
        # print('create hand2\n', opCards, len(draw))

        # print('print hand2 pretty way\n', k.convertSuit(opCards))

        sim = Simulations()

        start_sim = sim.sim_monte(drawH, board, opCards)
        # print('in 10k samples: rate hand1 against hand2=', start_sim)

        opHand = sim.get_card_power(opCards[0], opCards[1])
        betting = sim.rand_oddsRatio(100 - start_sim,opHand)
        # print('pot from previous', betting[0], '\nop bet', betting[1], '\ntotal pot', betting[2], '\nratio is', betting[3])

        board_filled = k.fillDrawBoard(board, draw)

        simple_game = sim.simple_sim(drawH, opCards, board_filled)
        # print('in 1 sample: board=', board_filled, ',winner is hand', simple_game[0] + 1)
        """
        call = input("call? (y/n)")
        file = open("bankroll.txt", 'r')
        bankroll = int(file.read())
        print(bankroll)

        if call == 'y' and simple_game[0] + 1 == 1:
            res = bankroll + betting[1] + betting[2]
        elif call == 'n':
            res = bankroll + (betting[2] / 2)
        else:
            res = bankroll - betting[1] - (betting[2] / 2)

        file = open("bankroll.txt", 'w')
        file.write(str(res))
        print(res)"""


    return [k.convertSuit(board),           #0 flop/turn board
            k.convertSuit(drawH),           #1 hand1 with draw
            k.convertSuit(opCards),         #2 hand2 random
            start_sim,                      #3 get winrate
            betting[0],                     #4 bank
            betting[1],                     #5 oponent bet
            betting[2],                     #6 totalpot
            k.convertSuit(board_filled),    #7 board full
            simple_game[0] + 1]             #8 winner

#print(main())