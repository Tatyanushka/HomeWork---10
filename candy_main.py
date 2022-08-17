#На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга. 
# Первый ход определяется жеребьёвкой. За один ход можно забрать не более чем 28 конфет. 
# Тот, кто берет последнюю конфету - проиграл.


# ход = сумма конфет // (28+1) - остаток от деления

# import ast
from asyncio.log import logger
from random import randint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup
import telegram
import logging

START, LEVEL, CANDY = range(3)

logger = logging.getLogger('logger')
case_lever = logging.getLogger('case_lever')
logger.info = 2021


bot = telegram.Bot('5495662945:AAERbmVD48DUU2f9DtlcuYL_gv3Gr7XV0Ho')

updater = Updater(token='5495662945:AAERbmVD48DUU2f9DtlcuYL_gv3Gr7XV0Ho', use_context=True)
dispatcher = updater.dispatcher

def game (update, context): # 
    
    task = str("На столе лежит 2021 конфета. Играют два игрока делая ход друг после друга."
                "За один ход можно забрать не более чем 28 конфет." 
                "Тот, кто берет последнюю конфету - проиграл. " )
    context.bot.send_message(chat_id=update.effective_chat.id, text = task)
      
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Ты готов?: да/нет")
    return LEVEL

def level (update, context):
    if str(update.message.text).lower() == 'да':
        keyboard = [['Простой(против бота)', 'Сложный(против бота с интеллектом ']]
        markup_key = ReplyKeyboardMarkup(keyboard, resize_keyboard = True, one_time_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Выбери уровень игры: Простой(против бота)/Сложный(против бота с интеллектом)",reply_markup=markup_key,)
        return START
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "ОК. До встречи! Поиграем в следующий раз!")
        return ConversationHandler.END


def start (update, context): # 
    case_lever.info = update.message.text
    
    lever = str("Твой ход! Введите кол-во конфет (от 1 до 28): ")
    context.bot.send_message(chat_id=update.effective_chat.id, text = lever)
    
    return CANDY

def candy (update, context):
    user = update.message.from_user  # определяем пользователя
  
    stack_candy = int(logger.info)
    if update.message.text == 'stop':
        return ConversationHandler.END
    elif update.message.text.isdigit() == False:
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Попробуйте еще раз (выход по слову /stop)")
    else:
        step_game = int(update.message.text)

        if (step_game > 28):
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Проснись!) Не более 28 конфет! Попробуйте еще раз!")
        elif (step_game == stack_candy)and(step_game < 29): # игрок забирает остатки конфет
            context.bot.send_message(chat_id=update.effective_chat.id, text = f"{user.first_name}, ты проиграл!")
            return ConversationHandler.END
        elif (stack_candy - step_game)<29 : # ход бота и конфет 28 и меньше - тогда бот проиграл
            context.bot.send_message(chat_id=update.effective_chat.id, text = f"{user.first_name}, я забираю остаток конфет и я проиграл!")
            return ConversationHandler.END
        else:
            stack_candy = stack_candy - step_game
            
            if case_lever.info == "Простой(против бота)": 
                step_bot = randint(1,29)
            else:
                if stack_candy%29 == 0: 
                    step_bot =  28
                else : 
                    step_bot =  stack_candy%29

            msg = f"Мой ход: {step_bot}. \n В куче осталось {(stack_candy - step_bot)}" #ход бота
            context.bot.send_message(chat_id=update.effective_chat.id, text = msg)
            stack_candy -= step_bot #определяем остаток конфет в куче
            logger.info =  stack_candy 
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Теперь твой ход. (выход по слову stop)")      

def end(update, context):
    user = update.message.from_user  # определяем пользователя
    context.bot.send_message(chat_id=update.effective_chat.id, text ="Конец игры!")
    # Заканчиваем игру
    return ConversationHandler.END

candy_handler = ConversationHandler(
        entry_points=[CommandHandler('game', game)],
        states= {
            LEVEL: [MessageHandler(Filters.text, level)],
            START: [MessageHandler(Filters.text, start)], 
            CANDY: [MessageHandler(Filters.text, candy)]
                },
        fallbacks=[CommandHandler('end', end)],
    )

dispatcher.add_handler(candy_handler)



print('start bot')
updater.start_polling()
updater.idle()