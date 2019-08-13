import os

import telebot as tb
import cv2

# Constants
bot_token = ''

bot = tb.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, 'it`s work')
    user_keyboard = tb.types.ReplyKeyboardMarkup()
    user_keyboard.resize_keyboard = True
    user_keyboard.row('/image')
    bot.send_message(message.chat.id, 'Hello', reply_markup=user_keyboard)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, 'in developinggggg')


@bot.message_handler(commands=['image'])
def handle_text(message):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite('image.jpg', frame)
    img = open(os.getcwd() + '/image.jpg', 'rb')
    bot.send_photo(message.chat.id, img)
    if cv2.waitKey(1) & 0xFF == ord('y'):  # save on pressing 'y'
        cv2.destroyAllWindows()

    img.close()
    cap.release()


@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, 'in developing')


bot.polling(none_stop=True)
# if __name__ == '__main__':
#     pass
