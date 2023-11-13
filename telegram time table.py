import telebot
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


kees = open('my_rog/Characteristics.txt')
kees = kees.read().split()

CREDENTIALS_FILE = kees[0]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
spreadsheetId = '1ZSY5WVG4r1gvX17a7FF8kBXykT2cNouWPfaU0YQ5iJQ'
data = []
all_data, madrih_df, yilpan_df, qa_df, uxui_df, tii_df = [], [], [], [], [], []

real_bot_token = kees[1]

bot = telebot.TeleBot(real_bot_token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True).row('Катя', 'Виталик', 'Аля')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True).row('Авива', 'Орна', 'Ора', 'Сара и Илана')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True).row('UX UI', 'QA', 'Стаж')
keyboard4 = telebot.types.ReplyKeyboardMarkup(True, True).row('Оставить', 'Изменить')
keyboard_main = telebot.types.ReplyKeyboardMarkup(True, False).row('Расписание')

work_on = True

def update_google_sheets():
    global data
    results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId,
                                     ranges = 'User info',
                                     valueRenderOption = 'FORMATTED_VALUE',
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute()
    data = results['valueRanges'][0]['values']

def get_data(rangee):
        spreadsheetId = '1ZSY5WVG4r1gvX17a7FF8kBXykT2cNouWPfaU0YQ5iJQ'
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId,
                                            ranges = rangee,
                                            valueRenderOption = 'FORMATTED_VALUE',
                                            dateTimeRenderOption = 'FORMATTED_STRING').execute()
        return results

def update_all_datas():
    global all_data, madrih_df, yilpan_df, qa_df, uxui_df, tii_df
    update_google_sheets()
    all_data = pd.DataFrame(data)

    madrih_data = get_data('Мадрихи!A:D')['valueRanges'][0]['values']
    ylipan_data = get_data('Ульпан!A:E')['valueRanges'][0]['values']
    qa_data = get_data('QA!A:C')['valueRanges'][0]['values']
    uxui_data = get_data('UX/UI!A:C')['valueRanges'][0]['values']
    tii_data = get_data('TII!A:C')['valueRanges'][0]['values']

    madrih_df = pd.DataFrame(madrih_data).fillna('')
    yilpan_df = pd.DataFrame(ylipan_data).fillna('')
    qa_df = pd.DataFrame(qa_data).fillna('')
    uxui_df = pd.DataFrame(uxui_data).fillna('')
    tii_df = pd.DataFrame(tii_data).fillna('')

def madrih_paln(name, today_plan, tomorrow_plan):
    if name == 'Виталик':
        if madrih_df.at[1, 1] != '':
            today_plan.append('Встреча с мадрихом\n' + madrih_df.at[1, 1])
        if madrih_df.at[2, 1] != '':
            tomorrow_plan.append('Встреча с мадрихом\n' + madrih_df.at[2, 1])
    elif name == 'Катя':
        if madrih_df.at[1, 3] != '':
            today_plan.append('Встреча с мадрихом\n' + madrih_df.at[1, 3])
        if madrih_df.at[2, 3] != '':
            tomorrow_plan.append('Встреча с мадрихом\n' + madrih_df.at[2, 3])
    elif name == 'Аля':
        if madrih_df.at[1, 2] != '':
            today_plan.append('Встреча с мадрихом\n' + madrih_df.at[1, 2])
        if madrih_df.at[2, 2] != '':
            tomorrow_plan.append('Встреча с мадрихом\n' + madrih_df.at[2, 2])
    return today_plan,tomorrow_plan

def ylipan_plan(name, today_plan, tomorrow_plan):
    if name == 'Авива':
        if yilpan_df.at[1, 1] != '':
            today_plan.append('Ульпан \n' + yilpan_df.at[1, 1])
        if yilpan_df.at[2, 1] != '':
            tomorrow_plan.append('Ульпан \n' + yilpan_df.at[2, 1])
    elif name == 'Ора':
        if yilpan_df.at[1, 2] != '':
            today_plan.append('Ульпан \n' + yilpan_df.at[1, 2])
        if yilpan_df.at[2, 2] != '':
            tomorrow_plan.append('Ульпан \n' + yilpan_df.at[2, 2])
    elif name == 'Орна':
        if yilpan_df.at[1, 3] != '':
            today_plan.append('Ульпан \n' + yilpan_df.at[1, 3])
        if yilpan_df.at[2, 3] != '':
            tomorrow_plan.append('Ульпан \n' + yilpan_df.at[2, 3])
    elif name == 'Сара и Илана':
        if yilpan_df.at[1, 4] != '':
            today_plan.append('Ульпан \n' + yilpan_df.at[1, 4])
        if yilpan_df.at[2, 4] != '':
            tomorrow_plan.append('Ульпан \n' + yilpan_df.at[2, 4])
    return today_plan, tomorrow_plan

def program_plan(name, today_plan, tomorrow_plan):
    if name == 'UX UI':
        if uxui_df.at[1, 1] != '[]':
            today_plan.append('Занятие\n' + uxui_df.at[1, 1][2:-2])
        if uxui_df.at[1, 2] != '[]':
            today_plan.append('Занятие\n' + uxui_df.at[1, 2][2:-2])
        if uxui_df.at[2, 1] != '[]':
            tomorrow_plan.append('Занятие\n' + uxui_df.at[2, 1][2:-2])
        if uxui_df.at[2, 2] != '[]':
            tomorrow_plan.append('Занятие\n' + uxui_df.at[2, 2][2:-2])
    elif name == 'QA':
        if qa_df.at[1, 1] != '[]':
            today_plan.append('Занятие\n' + qa_df.at[1, 1][2:-2])
        if qa_df.at[1, 2] != '[]':
            today_plan.append('Занятие\n' + qa_df.at[1, 2][2:-2])
        if qa_df.at[2, 1] != '[]':
            tomorrow_plan.append('Занятие\n' + qa_df.at[2, 1][2:-2])
        if qa_df.at[2, 2] != '[]':
            tomorrow_plan.append('Занятие\n' + qa_df.at[2, 2][2:-2])
    elif name == 'Стаж':
        if tii_df.at[1, 1] != '[]':
            today_plan.append('Занятие\n' + tii_df.at[1, 1][2:-2])
        if tii_df.at[1, 2] != '[]':
            today_plan.append('Занятие\n' + tii_df.at[1, 2][2:-2])
        if tii_df.at[2, 1] != '[]':
            tomorrow_plan.append('Занятие\n' + tii_df.at[2, 1][2:-2])
        if tii_df.at[2, 2] != '[]':
            tomorrow_plan.append('Занятие\n' + tii_df.at[2, 2][2:-2])

    return today_plan, tomorrow_plan


@bot.message_handler(commands = ['start'])
def check_id(message):
    update_google_sheets()
    have_id = False
    for i in range(len(data)):
        if data[i][0] == str(message.chat.id):
            have_id = True
            your_info = data[i]

    if have_id:
        msg = bot.send_message(message.chat.id, f'Ваши данные уже есть \n Мадрих - {your_info[1]}\n Ульпан - {your_info[2]}\n Программа - {your_info[3]}', reply_markup = keyboard4)
        bot.register_next_step_handler(msg, your_info_cange)
    else:
        start_message(message)

def your_info_cange(message):
    if message.text == 'Изменить':
        start_message(message)
    if message.text == 'Оставить':
        bot.send_message(message.chat.id, 'Понял, принял', reply_markup = keyboard_main)

def start_message(message):
    msg = bot.send_message(message.chat.id, 'Салам, у кого ты группе', reply_markup = keyboard1)
    bot.register_next_step_handler(msg, madrih)

def madrih(message):
    if not message.text in {'Катя', 'Виталик', 'Аля'}:
        msg = bot.send_message(message.chat.id, 'Выберите из вариантов!', reply_markup = keyboard1)
        start_message(message)
    else:
        user_info = {}
        user_info['Мадрих'] = message.text
        msg = bot.send_message(message.chat.id, 'КТо у тебя ведет Ульпан', reply_markup = keyboard2)
        bot.register_next_step_handler(msg, program, user_info)

def program(message, user_info):
    if not message.text in {'Авива', 'Орна', 'Ора', 'Сара и Илана'}:
        msg = bot.send_message(message.chat.id, 'Выберите из вариантов!', reply_markup = keyboard2)
        madrih(message)
    else:
        user_info['Ульпан'] = message.text
        msg = bot.send_message(message.chat.id, 'На какой ты программе', reply_markup = keyboard3)
        bot.register_next_step_handler(msg, write_info, user_info)

def write_info(message, user_info):
    if not message.text in {'UX UI', 'QA', 'Стаж'}:
        msg = bot.send_message(message.chat.id, 'Выберите из вариантов!', reply_markup = keyboard3)
        program(message, user_info)
    else:
        msg = bot.send_message(message.chat.id, 'Спасибо. Захочешь изменить пиши /start', reply_markup = keyboard_main)
        user_info['Программа'] = message.text
        number = 0
        have_id = False
        for i in data:
            number += 1
            if i[0] ==  str(message.chat.id):
                rangee = f"User info!R{number}C1:R{number}C4"
                have_id = True
            elif not have_id:
                rangee = f"User info!A{len(data)+1}:D"


        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                                                                "valueInputOption": "USER_ENTERED",
                                                                "data": [
                                                                    {"range": rangee,
                                                                    "values": [[message.chat.id, user_info['Мадрих'], user_info['Ульпан'], user_info['Программа']]]}
                                                                ]
                                                                }).execute()

@bot.message_handler(commands = ['help'])
def print_id(message):
    bot.send_message(message.chat.id, 'Есть вопросы? Порешаем! \n@adfasq, @aka_Mr_Pips')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEI6IpkWR2yWtYd64SM8UZPLkm2WyAtIgACmhUAAhjCOUoQthLkmEXldS8E')

@bot.message_handler(content_types=['text'])
def send_plan(message):
    if message.text == 'Расписание':
        update_all_datas()
        today_plan = []
        tomorrow_plan = []
        user_info = all_data.loc[all_data[0] == str(message.chat.id)].reset_index(drop = True)
        plans = ylipan_plan(user_info.at[0, 2], today_plan, tomorrow_plan)
        plans = madrih_paln(user_info.at[0, 1], plans[0], plans[1])
        plans= program_plan(user_info.at[0, 3], plans[0], plans[1])
        text_today, text_tomorrow = 'Сегодня\n', '\nЗавтра\n'

        if len(plans[0]) > 0:
            for i in plans[0]:
                text_today = f'{text_today}\n{str(i)}'
            bot.send_message(user_info.at[0, 0], text_today)
        else:
            text_today = 'Сегодня можешь отдохнуть. \nСходи на пляж или на массаж в 151'
            bot.send_message(user_info.at[0, 0], text_today)


        if len(plans[1]) > 0:
            for i in plans[1]:
                text_tomorrow = f'{text_tomorrow}\n{str(i)}'
            bot.send_message(user_info.at[0, 0], text_tomorrow,  reply_markup = keyboard_main)
        else:
            text_tomorrow = 'Завтра твой день полностью свободен. Сходи в зал, что ли'
            bot.send_message(user_info.at[0, 0], text_tomorrow,  reply_markup = keyboard_main)

        df = pd.DataFrame(data)
        ind = df.index[df[0] == str(message.chat.id)].to_list()[0]
        df = df.fillna('')
        
        if type(df.at[ind, 4]) == '':
            df.at[ind, 4] = 1
        else:
            df.at[ind, 4] = int(df.at[ind, 4]) + 1
        print (df.at[ind, 4])
        service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                                                                "valueInputOption": "USER_ENTERED",
                                                                "data": [
                                                                    {"range": "User info!A1:E",
                                                                    "values": df.values.tolist()}
                                                                ]
                                                                }).execute()

while work_on:
    bot.polling()