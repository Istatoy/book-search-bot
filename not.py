import telebot
from telebot import types

# Токен бота от BotFather
BOT_TOKEN = '7611630052:AAG842wrunAsfmnlaWhWhI_PxpEVEEHXH2s'

# Инициализация бота
bot = telebot.TeleBot(BOT_TOKEN)

# Список книг (может быть заменен на базу данных)
books = [
    {'title': 'Технология программирования', 'author': 'Иванов Иван', 'file': 'C:/Users/User/Documents/book/books/.note/Технология программирования.pdf'},
    {'title': 'Алхимик', 'author': 'Пауло Коэльо', 'file': 'C:/Users/User/Documents/book/books/.note/Алхимик.pdf'},
    {'title': 'Книга 3', 'author': 'Автор 3', 'file': 'path/to/book3.pdf'}
]

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать! Напишите название книги, чтобы я мог её найти.")

# Поиск книги по названию
@bot.message_handler(func=lambda message: True)
def search_book(message):
    query = message.text.lower()
    results = [book for book in books if query in book['title'].lower()]
    
    if results:
        for book in results:
            markup = types.InlineKeyboardMarkup()
            btn_download = types.InlineKeyboardButton(text='📥 Скачать', callback_data=f"download_{book['title']}")
            markup.add(btn_download)
            bot.send_message(message.chat.id, f"📚 Название: {book['title']}\n✍ Автор: {book['author']}", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Книга не найдена. Попробуйте другое название.")

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith('download_'))
def send_book(call):
    book_title = call.data[len('download_'):]
    book = next((b for b in books if b['title'] == book_title), None)
    
    if book:
        try:
            with open(book['file'], 'rb') as file:
                bot.send_document(call.message.chat.id, file)
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, "Извините, файл книги не найден.")
    else:
        bot.send_message(call.message.chat.id, "Книга не найдена.")

# Запуск бота
bot.polling()
