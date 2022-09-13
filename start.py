#!/usr/bin/python3
import telebot,os
from telebot import types
import config
from main import getGame
from watch_users import getTablesCount
from dbFuncs import *
from draw_plot import getDistance
from datetime import datetime
import time
from threading import *

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])#если /start
def welcome(message):
    markup=types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,
                     'Привет ✌ ' + message.from_user.first_name + ', я бот-симулятор покерных раздач (beta). Я помогу тебе научиться анализировать ситуацию за покреным столом с точки зрения математики 👨‍🎓. Жми /sim чтобы начать.',
                     reply_markup=markup)
###############################################################################################################poker_funcs
#функция1 - бот приветствует юзера и предлагает сыграть в игру. после сообщения приветствия вызывается функция2
@bot.message_handler(commands=['sim'])
def start_game(message):
    if checkDb(message.chat.id) == '0':
        create_table(message.chat.id)
    else:
        bot.send_message(message.chat.id,'Баланс 💰: '+str(checkDb(message.chat.id)[-1][1])+' $')

    #sim bets and bank and send result
    bot.send_message(message.chat.id,'Мешаем колоду... ⏳')
    #game=Thread(target=getGame())
    game = getGame()
    '''
    msg = bot.send_message(message.chat.id,
                           'Раздача: ' + str(game[1]) + '\nСтавка: ' + str((game[4]) / 2) + '\nПринимаем? ответы:\ncall\nfold\nstop')
    bot.register_next_step_handler(msg, get_user_call, game)
    '''
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    item1=types.KeyboardButton("CALL")
    item2 = types.KeyboardButton("Fold")
    item3 = types.KeyboardButton("Stop")
    markup.add(item1,item2,item3)
    msg = bot.send_message(message.chat.id,'Раздача: ' + str(game[1]) + '\nСтавка: ' + str((game[4]) / 2) + '\nПринимаем?',reply_markup=markup)
    bot.register_next_step_handler(msg, get_user_call, game)


def get_user_call(message,game):
    user_calls = message.text
    if user_calls.lower()=='call':
        markup = types.ReplyKeyboardRemove(selective=False)
        start = datetime.now()
        msg = bot.send_message(message.chat.id, 'В банке (pot) уже ' + str(
            game[4]) + ' фишек с прошлого круга торговли. В новом противник ставит ' + str(
            game[5]) + ' фишек (bet). \nСколько фишек в общем банке (total pot)?\ntotal pot=pot+bet=...',reply_markup=markup)
        bot.register_next_step_handler(msg, process_calc_odds, game, start)
    elif user_calls.lower()=='fold':
        start_game(message)
    else:
        welcome(message)

#функция 2 - юзер считает сумму фишек, затем вводит сумму фишек на столе. алгоритм анализирует точность. печатаем следующее задание и вызываем функцию 3
def process_calc_odds(message,game,start):
    try:
        user_pot = float(message.text)
        #odds = round((pot / opBet),2)
        #rank=0
        x=check_answer(game[6],user_pot,100)
        bot.send_message(message.chat.id,x)
        msg = bot.send_message(message.chat.id, 'Далее рассчитай шансы (odds), как отношение банка (total pot) к ставке (bet), используя формулу odds=total pot/bet')
        bot.register_next_step_handler(msg, process_step2,game,start)
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй сначала /start')

#функция 3 получаем ответ юзера и проверяем его точность. печатаем результат, следующее задание и вызываем следующую функцию 4
def process_step2(message,game,start):
    try:
        user_odds=float(message.text)
        x = check_answer((game[6]/game[5]), user_odds, 0.5)
        bot.send_message(message.chat.id, x)
        msg = bot.send_message(message.chat.id, 'И последнее - переведи отношение в проценты\nodds%=100/(odds+1)')
        bot.register_next_step_handler(msg, process_step3, game,start)
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй заново /start')

# функция 4 юзер отвечает на последнее задание. проверяем ответ, считаем очки, печатаем результат. предлагаем начать сначала
def process_step3(message,game,start):
    try:
        user_oddsP=float(message.text)
        #oddsP=round((100/((game[6]/game[5])+1)),2)
        x = check_answer(round((100/((game[6]/game[5])+1)),2), user_oddsP, 3)
        bot.send_message(message.chat.id,x)

        #board_uniqe_shuffle = rand_shuf_new()#[(commonCards),koloda]
        #board_pretty_situation = print_scen(print_mast_symbol(board_uniqe_shuffle[0]))#красивый вывод общих карт
        bot.send_message(message.chat.id, 'на столе:\n'+str(game[0]))
        #res = sim_for_bot_new2(board_uniqe_shuffle[1], board_uniqe_shuffle[0][7])  # передаем лист и кол-во игроков
        #for i in range(board_uniqe_shuffle[0][7]):
         #   if i==0:
          #      bot.send_message(message.chat.id, 'игрок ' + str(i + 1) +' (вы)\n'+ str(print_mast_symbol_t(res[i])))
           # else:
            #    bot.send_message(message.chat.id, 'игрок '+str(i+1)+'\n'+str(print_mast_symbol_t(res[i])))
        bot.send_message(message.chat.id, 'Ваши карты:\n'+str(game[1]))

        #msg=bot.send_message(message.chat.id,'Принимаем ставку оппонента (напиши call или fold)?')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        item1 = types.KeyboardButton("CALL")
        item2 = types.KeyboardButton("Fold")
        markup.add(item1, item2)
        msg = bot.send_message(message.chat.id,
                               'Принимаем ставку оппонента?',
                               reply_markup=markup)

        bot.register_next_step_handler(msg,bet_or_not,game,start)
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй заново /start')

def bet_or_not(message,game,start):
    try:
        markup=types.ReplyKeyboardRemove(selective=False)
        call=message.text
        if call.lower()=='call' and game[8]==1:
            writeBankroll(message.chat.id,(game[4]+game[5]),'+')
        elif call.lower()=='call' and game[8]==2:
            writeBankroll(message.chat.id, ((game[4]/2)+game[5]), '-')
        elif call.lower()=='fold':
            writeBankroll(message.chat.id, ((game[4]) / 2), '-')
        bot.send_message(message.chat.id, 'итог раздачи\n'+str(game[7])+'\nКарты оппонента:\n'+str(game[2]),reply_markup=markup)
        bot.send_message(message.chat.id, 'Побеждает игрок ' + str(game[8]))
        bot.send_message(message.chat.id, '\nВаш bankroll составляет ' + str(checkDb(message.chat.id)[-1][1]))
        #a=[a[0],res[1]]

        msg=bot.send_message(message.chat.id,'Какое эквити (ev) вашей руки в данной раздаче?\nДля быстрого рассчета используйте формулы:\nev=outs*4 (на стадии flop);\nev=outs*2 (на стадии turn), где outs - это количество карт, усиливающих вашу руку по отношению к руке оппонента.')
        bot.register_next_step_handler(msg, results, game,start)
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй заново /start')

def results(message,game,start):
    try:
        user_ev = float(message.text)
        #bot.send_message(message.chat.id, 'Считаем вероятность по методу Монте Карло...')
        #wrate = round(sim_monte(list[0],list[1]))
        x = check_answer(game[3], user_ev, 10)
        bot.send_message(message.chat.id, x)
        time=datetime.now()-start
        bot.send_message(message.chat.id, 'Ваше время: '+str(time)[0:7])
        if game[3]>round((100/((game[6]/game[5])+1)),2):
            string = 'Шансы вашей руки были больше шансов банка. В такой ситуации на дистанции лучше принять ставку.'+ '\nНажми /sim для повтора. \n♠️️♥️♦️♣'
        else:
            string = 'Шансы вашей руки были меньше шансов банка. В такой ситуации на дистанции лучше сбросить.' + '\nНажми /sim для повтора. \n♠️️♥️♦️♣'
        bot.send_message(message.chat.id, string)
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй заново /start')

def check_answer(auto_calc, user_calc,pogreshnost):#val1= calculated; val2=user answer
    if auto_calc == user_calc:
        msg = 'Супер! Ты даешь точный ответ!'
        #rank = rank + 2
    elif auto_calc + pogreshnost > user_calc and auto_calc - pogreshnost < user_calc:
        msg = 'Близко! Точный ответ: ' + str(auto_calc)
        #rank = rank + 1
    else:
        msg = 'Неправильно, ответ: ' + str(auto_calc)
    #L=[msg,rank]
    return msg

@bot.message_handler(commands=['distance'])
def distance(message):
    try:
        imageName=getDistance(checkDb(message.chat.id))
        #print(image)
        image=open(imageName,'rb')
        bot.send_photo(message.chat.id, photo=image)
        comand='rm '+str(imageName)
        os.system(comand)
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй сначала /start')
######################################################################################################other func
@bot.message_handler(commands=['help'])#если /help
def help(message):
    string = 'В отличие от шахмат, покер — игра с неполной информацией. То есть, игроки не знают, какая карта (или диапазон карт) есть на руках у оппонентов — они могут это лишь предполагать с определенной степенью вероятности. Правила покера просты — выигрывает тот, у кого на руках сильнейшая комбинация, составленная из его карт и тех, что на столе, или последний оставшийся игрок, если все остальные сбросили. Всего в покере десять комбинаций: Роял-флеш, Стрит-флеш, Каре, Фулл-хаус, Флеш, Стрит, Сет/Трипс/Тройка, Две пары, Одна пара, Старшая карта. Существует много разных видов покера. Здесь мы будем рассматривать Texas Holdem No Limit Poker, он же турнирный покер.'
    markup=types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,string,
                     reply_markup=markup)

@bot.message_handler(commands=['more'])#если /more
def more(message):
    L=['https://en.wikipedia.org/wiki/Glossary_of_poker_terms','https://www.thepokerbank.com/strategy/basic/starting-hand-selection/sklansky-groups/','http://poker.srv.ualberta.ca/','https://xakep.ru/2010/10/28/53647/','https://app.edge.poker/','https://www.codingthewheel.com/archives/poker-hand-evaluator-roundup/#xpokereval','https://github.com/ihendley/treys']
    for i in range(len(L)):
        time.sleep(1)
        bot.send_message(message.chat.id, 'Link #'+str(i)+': '+L[i])

@bot.message_handler(commands=['sovet'])
def sovet(message):
    try:
        msg=bot.send_message(message.chat.id,'Данный проект находится в стадии развития. Напиши свою идею.')
        bot.register_next_step_handler(msg, save_sovet)
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй сначала /start')

def save_sovet(message):
    try:
        user_idea = message.text
        f = open('/opt/pb_v5/ideas.txt', 'a')
        f.write(message.from_user.first_name+' '+ message.from_user.last_name+ ' idea: ' + user_idea+'\n')
        bot.send_message(message.chat.id,'Ок. /start')
    except Exception as e:
        bot.send_message(message.chat.id,'Ошибка! Попробуй сначала /start')

@bot.message_handler(commands=['users'])
def countUsers(message):
    bot.send_message(message.chat.id, 'Количество пользователей: '+str(getTablesCount()))

@bot.message_handler(commands=['donate'])
def countUsers(message):
    bot.send_message(message.chat.id, 'Вы можете поддержать разработчика, переведя деньги по ссылке\nhttps://yoomoney.ru/to/4100117216222401')

bot.polling(none_stop=True)#RUN