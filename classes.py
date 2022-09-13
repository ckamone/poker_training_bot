import random

class Koloda:
    def __init__(self):
        pass

    def card_ranks(self):
        L = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return L

    def card_straightRanks(self):
        L = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return L

    def card_suitL(self):
        L = ['s','h','d','c']
        return L

    def card_suitS(self):
        L = ['♠️','♥️','♦️','♣️']
        return L

    def allCards_list(self,ranks,suit):
        # генерим список всех карт в колоде в формате Ah Kd 9s 2c...
        myHandL = []
        for i in range(len(ranks)):
            for j in range(len(suit)):
                a = ranks[i]
                b = suit[j]
                myHandL.append(a + b)
        return myHandL

    def genDraw_list(self,straightRanks,suitL):
        temp = []
        randStartCard = random.randint(0, 10)
        gutShot = random.randint(0, 1)

        if straightRanks[randStartCard] != 'J' and gutShot == 1:
            for i in range(0, 4):
                if i == 0:
                    temp.append(straightRanks[randStartCard + i] + suitL[random.randrange(0, 4)])
                else:
                    temp.append(straightRanks[randStartCard + i + 1] + suitL[random.randrange(0, 4)])
        else:
            for i in range(0, 4):
                temp.append(straightRanks[randStartCard + i] + suitL[random.randrange(0, 4)])
        return temp

    def getDraw(self,strtL,fullDeck):
        for i in strtL:
            fullDeck.remove(i)  # chistim kolodu
        random.shuffle(strtL)  # шафлим список стритовых карт
        random.shuffle(fullDeck)  # шафлим список колоды
        cardsL = strtL + fullDeck
        return cardsL

    def getDrawHand(self,DrawCardList):
        rand=random.randint(0,1)
        if rand==1:
            temp=[DrawCardList[0],DrawCardList[1]]
        else:
            temp = [DrawCardList[0], DrawCardList[-1]]
        for i in temp:
            DrawCardList.remove(i)
        return temp

    def getDrawBoard(self,list):
        temp=[]
        flopOrTurn=random.randint(3,4)
        for i in range(0,flopOrTurn):
            a=list[0]
            temp.append(a)
            list.remove(a)
        while len(temp)!=5:
            temp.append('')
        return temp

    def fillDrawBoard(self,list1,remCards):
        list=list1.copy()
        for i in range(len(list)):
            if list[i]=='':
                list[i]=remCards[-1]
                remCards.remove(list[i])
        return list

    def getOpHand(self,list):
        temp=[]
        for i in range(0,2):
            a=list[0]
            temp.append(a)
            list.remove(a)
        return temp

    def convertSuit(self,list):
        copy = list.copy()
        for i in range(len(copy)):
            if copy[i] != '':
                if copy[i][1] == 's':
                    copy[i] = copy[i][0] + '♠️'
                elif copy[i][1] == 'h':
                    copy[i] = copy[i][0] + '♥️'
                elif copy[i][1] == 'd':
                    copy[i] = copy[i][0] + '♦️'
                elif copy[i][1] == 'c':
                    copy[i] = copy[i][0] + '♣️'
        return copy
