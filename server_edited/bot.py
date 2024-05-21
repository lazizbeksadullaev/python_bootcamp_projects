import telebot

token = '5142087260:AAEZRe6ZUP3Ng9vDiUoIF5PI7zEnJsFd1eQ'
bot = telebot.TeleBot(token=token)
habar1 = "Ha Nodirbek nega kulyapsan? Seni o\'zing qachon kelasan unda uyga, pilla ishlari ham ko'payib ketibdi deb eshitdim, bugun onagiz Nargizaxon juda mazali ovqat qilaman deyapti"
#message = bot.send_message('-586074579', habar1)
#print(message.id)
bot.forward_message('-586074579', '-586074579', 10)