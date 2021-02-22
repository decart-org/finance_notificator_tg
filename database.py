from datetime import datetime, timedelta
import mysql.connector
import time
import requests

conn = mysql.connector.connect(
  host="45.82.70.87",
  user="decartadmin",
  passwd="Jp^3L#2h",
  database="global_database"
)

cursor = conn.cursor(buffered=True)

def select_all_data(store):
    sql = 'SELECT SUM(total_sum) FROM manager_web_history WHERE DATE = \'' + str(datetime.now().date()) + '\' AND store = \'' + str(store) + '\';'
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result:
        return result[0]

def select_quantity_records(store):
    sql = 'SELECT COUNT(*) FROM manager_web_history WHERE DATE = \'' + str(datetime.now().date()) + '\' AND store = \'' + str(store) + '\';'
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result:
        return result[0]

def select_manager_list(store):
    sql = 'select login_m from manager_password where departament = \'{0}\' and user_group = \'manager\';'.format(store)
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchall()
    list_manager = []
    if result:
        for manager in result:
            list_manager.append(manager[0])
    return list_manager
        

def get_manager_total_sum(manager):
    sql = 'SELECT SUM(total_sum) FROM manager_web_history WHERE DATE = \'' + str(datetime.now().date()) + '\' AND manager_name = \'' + str(manager) + '\';'
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result:
        return result[0]

def get_manager_count_order(manager):
    sql = 'SELECT COUNT(total_sum) FROM manager_web_history WHERE DATE = \'' + str(datetime.now().date()) + '\' AND manager_name = \'' + str(manager) + '\';'
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result:
        return result[0]

def get_manager_original_name(manager):
    sql = 'SELECT original_name FROM manager_list where crm_name = \'{0}\';'.format(manager)
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result:
        return result[0]

def select_database_date(date):
    sql = 'select date from telegram_notification_admin where date = \'{0}\';'.format(str(date))
    cursor.execute(sql)
    conn.commit()
    result = cursor.fetchone()
    if result:
        return result[0]

def insert_date_notification():
    sql = 'insert into telegram_notification_admin(date)values(\'{0}\');'.format(datetime.now().date())
    cursor.execute(sql)
    conn.commit()