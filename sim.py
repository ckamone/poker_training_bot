from treys import Deck, Card, Evaluator
import random
import math
#from get_cards import *

class Simulations:
    def __init__(self):
        pass

    def sim_monte(self,list,list2,opCards): #list1=userH, list2=board
        deck = Deck()
        evaluator = Evaluator()
        w = 0; #wins
        n = 0; #iterations
        nmax = 3000

        while n != nmax:  # monte carlo cycle
            c = deck.GetFullDeck()  # get deck and rand it
            random.shuffle(c)

            handsL = [[Card.new(list[0]), Card.new(list[1])]]  # choose some cards and remove from main list
            c.remove(handsL[0][0])
            c.remove(handsL[0][1])

            # get op hands and clear main list
            l = [Card.new(opCards[0]), Card.new(opCards[1])]
            handsL.append(l)
            c.remove(l[0]); c.remove(l[1])

            Board = [list2[0], list2[1], list2[2], list2[3], list2[4]]  # get wished board

            # clear our cards from deck
            for i in range(len(Board)):
                if Board[i] == '':
                    Board[i] = c[0]
                    c.remove(c[0])
                else:
                    Board[i] = Card.new(Board[i])
                    c.remove(Board[i])

            # count points for all players
            scoreL = [10000]
            for i in range(len(handsL)):
                score = evaluator.evaluate(Board, handsL[i])
                scoreL.append(score)

            f = [i for i, x in enumerate(scoreL) if x == min(scoreL)]  # sort all players by hands score

            for i in range(len(f)):  # count w if player1 is winning
                if f[i] == 1:
                    w += 1
            n += 1
        rate = round(((100 / nmax) * w),1)  # count win ratio in whole number of itterations
        return rate

    def simple_sim(self,list,list1,board):
        boardL = []
        for i in range(len(board)):
            boardL.append(Card.new(board[i]))

        user=[Card.new(list[0]), Card.new(list[1])]
        op=[Card.new(list1[0]), Card.new(list1[1])]

        # получить список рук в числовом формате
        handsL = [(user),(op)]

        # count points for all players
        evaluator = Evaluator()
        scoreL = []
        for i in range(len(handsL)):
            score = evaluator.evaluate(boardL, handsL[i])
            scoreL.append(score)

        temp = []
        for y in range(len(scoreL)):
            f = [i for i, x in enumerate(scoreL) if x == min(scoreL)]
            temp.append(f[0])
            scoreL[f[0]] = 10000 + y

        return temp # returns ids of bestH

    def get_card_power(self, card1, card2): #func to regulate preflop betsize
        bad_bet = random.randint(1, 10)
        if bad_bet == 1:
            power = random.randint(30000, 70000)
        else:
            power=(Card.new(card1)/10**6)*(Card.new(card2)/10**6)
        return round(math.log(power)+6)

    def rand_oddsRatio(self,opWinRate,opHandPower):  # func to regulate postflop sizing

        if opWinRate>=65:
            ratios=[3,2,1.5]
        elif opWinRate<65 and opWinRate>30:
            ratios=[4,3,2]
        else:
            ratios=[5,4]

        bank=1000+(100*opHandPower) #на банк должен влиять preflop
        opBetRatio = random.choice(ratios) # на оп бет ратио должны влиять шансы postflop

        if opBetRatio == 5:  # 5 to 1 = 16%
            opBet = bank / 4
        elif opBetRatio == 4:  # 4 to 1 = 20%
            opBet = bank / 3
        elif opBetRatio == 3:  # 3 to 1 = 25%
            opBet = bank / 2
        elif opBetRatio == 2:  # 2 to 1 = 33%
            opBet = bank
        elif opBetRatio == 1.5:  # 1.5 to 1 = 40%
            opBet = bank * 2

        opBet = round(opBet)
        pot = round((bank + opBet), 2)
        L = [bank, opBet, pot,opBetRatio]

        return L


