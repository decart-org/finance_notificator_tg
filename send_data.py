import telebot
from telebot import types
import time
import config
import logging
from datetime import datetime
import database

logging.basicConfig(level=logging.DEBUG)
bot = telebot.TeleBot(config.token, threaded=False)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, message.chat.id)

def main():
    while True:
        today = datetime.now().date()
        time_now = datetime.now().time().hour
        check_insert_today_date = database.select_database_date(today)

        if int(time_now) == 20 and check_insert_today_date is None: #додати перевірку на відправлене повідомлення в цей день
            #data
            firini_total_sum = int(database.select_all_data('Firini'))
            decart_total_sum = int(database.select_all_data('DecArt'))

            firini_count_records = int(database.select_quantity_records('Firini')) 
            decart_count_records = int(database.select_quantity_records('DecArt')) 

            #Підрахунки загальних показників
            firini_s_check = int(firini_total_sum) / int(firini_count_records)
            decart_s_check = int(decart_total_sum) / int(decart_count_records)
            
            message_all_data = '*Загальний звіт за ' + str(datetime.now().date()) + '*\n\n\n' + \
                'Оборот DecArt: {0}\nОборот Firini: {1}\n\nСередній чек DecArt: {2}\nСередній чек Firini: {3}'.format(
                    decart_total_sum, firini_total_sum, firini_s_check, decart_s_check)

            message_to_manager = '*Звіт по менеджерах за '  + str(datetime.now().date()) + '*\n\n\n*DecArt*\n'

            bot.send_message(604377972, message_all_data, parse_mode='Markdown')

            #=============================================================
            #Отримуємо дані по менеджерах
            manager_list_decart = database.select_manager_list('DecArt')
            manager_list_firini = database.select_manager_list('Firini')


            for manager_decart in manager_list_decart:
                try:
                    manager_original_name = database.get_manager_original_name(manager_decart)
                    manager_count_order = database.get_manager_count_order(manager_decart)
                    manager_total_sum = database.get_manager_total_sum(manager_decart)
                    manager_s_check = manager_total_sum / manager_count_order

                    #Додаємо в повідомлення
                    message_to_manager += '*' + str(manager_original_name) + '*\n' +  \
                        'Сума замовлень: ' + str(manager_total_sum) + '\nКількість замовлень: ' + str(manager_count_order) + \
                            '\nСередній чек: ' + str(manager_s_check) + '\n\n'
                except:
                    continue

            message_to_manager += '\n\n\n*Firini*\n'

            for manager_firini in manager_list_firini:
                try:
                    manager_original_name = database.get_manager_original_name(manager_firini)
                    manager_count_order = database.get_manager_count_order(manager_firini)
                    manager_total_sum = database.get_manager_total_sum(manager_firini)
                    manager_s_check = manager_total_sum / manager_count_order

                    #Додаємо в повідомлення
                    message_to_manager += '*' + str(manager_original_name) + '*\n' +  \
                        'Сума замовлень: ' + str(manager_total_sum) + '\nКількість замовлень: ' + str(manager_count_order) + \
                            '\nСередній чек: ' + str(manager_s_check) + '\n\n'
                except:
                    continue
            
            bot.send_message(604377972, message_to_manager, parse_mode='Markdown')
            database.insert_date_notification()
        else:
            time.sleep(10)

main()