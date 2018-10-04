from config import APP_WAVES_ADDRESS

# Replies (handler file)
HELP_MSG = """Отправьте сообщение, чтобы задать вопрос или используйте клавиатуру, чтобы выбрать задание. Нажмите /start, если не видите клавиатуру"""
START_MSG = f"""Привет! Мы хотим сыграть с тобой в игру! Этот бот предназначен для митапов, организуемых амбассадорами, сейчас мы его активно тестируем. Выбирай задания и играй, а если что-то непонятно, то просто напиши мне сюда."""
UNKNOWN_CMD_MSG = """Неизвестная команда. Нажмите /help или используйте клавиатуру"""
ASK_US_MSG = """Вы можете задать свой вопрос боту. Мы ответим. Когда-нибудь."""
ACTIVE_TASK_MSG = "У вас есть выбранное задание:\n%s"
ALREADY_COMPLETED_MSG = "Задание \"%s\" уже было успешно выполнено"
ALL_TASKS_COMPLETED_MSG = "Заданий больше нет. Ты все выполнил"
NOT_AVAILABLE_TASK_MSG = "Задание %s сейчас недоступно"
TASK_REMOVED_MSG = "Задание отменено: \"%s\""

# Menu titles
CANCEL_MENU_TITLE = "Если хотите отменить задание, нажмите:"
TASKS_MENU_TITLE = "Выберите задание:"

# Task names, descriptions and onComplete messages
# Get user address
GET_USER_ADDRESS_NAME = 'Дай мне свой адрес'
GET_USER_ADDRESS_DESCRIPTION = f'Еее, начинаем играть! Начнем с простого - скачай мобильное приложение Waves, зарегистрируй новый аккаунт и пришли мне свой адрес. Вот ссылки на мобильные приложения. \n Android: https://play.google.com/store/apps/details?id=com.wavesplatform.wallet \n iOS: https://itunes.apple.com/us/app/waves-wallet/id1233158971?mt=8'
GET_USER_ADDRESS_ON_COMPLETE_MSG = 'Молодцом! Теперь у меня есть твой адрес и я̶ ̶з̶а̶б̶е̶р̶у̶ ̶в̶с̶е̶ ̶т̶в̶о̶и̶ ̶д̶е̶н̶ь̶г̶и̶ ты можешь выбрать следующее задание.'
# DEX Exchange
DEX_EXCHANGE_NAME = 'Сделай обмен через DEX'
DEX_EXCHANGE_DESCRIPTION = 'Сходи на DEX и поменяй WAVES на Bitcoin. Надеюсь, тебе не понадобится помощь с интерфейсом, а если все-таки будет что-то не совсем понятно, то пиши мне.'
DEX_EXCHANGE_ON_COMPLETE_MSG = 'Мои искренние поздравления! Ты одолел наш DEX'
# Send WAVES
SEND_WAVES_NAME = 'Соверши перевод WAVES'
SEND_WAVES_DESCRIPTION = 'Следующее задание не для жадных. Отправь 0.001 WAVES на адрес:'
SEND_WAVES_ON_COMPLETE_MSG = 'Воу, а ты ничего! Поздравляю тебя с успешной сдачей экзамена на жадность. Мы тебе компенсировали твои токенами. С процентами :)'
# Send selfie
SEND_SELFIE_NAME = 'Селфи'
SEND_SELFIE_DESCRIPTION = 'Это задание для самых общительных. Пришли свою фотографию мне!'
SEND_SELFIE_ON_COMPLETE_MSG = 'О, получил фотографию! А ты красивая (или красивый, извини, я же бот, я не разбираю пол).'
# Find user
FIND_USER_NAME = 'Найди человека'
FIND_USER_DESCRIPTION = 'Найди этого человека и отправь ему 0.01 WAVES. А потом мы вернемся к нашему разговору.'
FIND_USER_ON_COMPLETE_MSG = 'Молодец! Надеюсь тебе было полезно или интересно! Спасибо, что помогаешь нам! Ты мне нравишься :)'

# Additional replies. TaskFactory file
BAD_IMAGE_MSG = """Фотография должна содержать только 1 лицо"""
DO_SELFIE_TASK_FIRST_MSG = f"""Сначала выполни задание \"{SEND_SELFIE_NAME}\""""