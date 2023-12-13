import uuid

import telebot
import requests
import base64

bot_token = ''
bot = telebot.TeleBot(bot_token)


def sendPhotoToBackEnd(photo):
    data_url = "data:image/jpg;base64,%s" % base64.b64encode(photo)
    data_url = data_url[0:22] + data_url[24:]
    title = str(uuid.uuid4())[:12]
    response = requests.post("http://localhost:8000" + "/photo_analysis/",
                             data={'title': title, 'image': data_url})
    data = response.json()

    # data = {
    #     "columns": {"name": "название анализа", "result": "Численный результат", "norm": "численная норма анализа"},
    #     "rows": [
    #         {"is_composite_analysis": True, "name": "Анализ крови"},
    #         {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "", "measurement_unit": "г/л"},
    #         {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160", "measurement_unit": "г/л"},
    #         {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160", "measurement_unit": "г/л"},
    #         {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160", "measurement_unit": "г/л"},
    #         {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160", "measurement_unit": "г/л"},
    #         {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160", "measurement_unit": "г/л"},
    #         {"is_composite_analysis": False, "name": "Анализ на эритроциты", "value": "116", "norm": "130-160", "measurement_unit": "г/л"},
    #     ]
    # }

    return data


def rawToTable(data):
    table = ""
    try:
        for row in data["rows"]:
            if row["is_composite_analysis"]:
                table = table + "<b><u>" + row["name"] + "</u></b>" + "\n"
            else:
                table = table + f'<code>{row["name"]}</code>: <b>{row["value"]} {row["measurement_unit"]}</b>'
                if len(row["norm"]) != 0:
                    table = table + f' <i>(норма: {row["norm"]})</i>'
            table = table + "\n"
    except:
        table = data['error']
    return table


@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = "Привет! Меня зовут MedOne - я помогу тебе преобразовать твои мед. документы в электронный вид."
    bot.send_message(message.chat.id, welcome_message)

    instructions_message = "Пожалуйста, отправь фотографию или скан твоих документов."
    bot.send_message(message.chat.id, instructions_message)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    thank_you_message = "Спасибо! Скоро ты получишь таблицу с твоими данными."
    bot.send_message(message.chat.id, thank_you_message)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    data = sendPhotoToBackEnd(downloaded_file)

    table = rawToTable(data)

    bot.send_message(message.chat.id, table, parse_mode="HTML")


@bot.message_handler(content_types=['document', 'audio', 'video', 'text'])
def handle_other_types(message):
    other_types_message = "Пожалуйста, отправьте только фотографии или сканы ваших документов."
    bot.send_message(message.chat.id, other_types_message)


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
