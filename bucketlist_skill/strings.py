from random import choice

from .state import State

TEXT = {
    'hello': 'Привет! Добавим желание? Или откроем ваш список желаний? Может быть, Список всех желаний.',
    'ability': 'Этот навык поможет разнообразить твою фантазию и вовлечёт в планирование и визуализацию своих желаний!',
    'bye': 'Пока!/До свидания!/Бай-бай!/Удачи!',
    'back': 'Ты находишься в меню, откроем список? Можем ещё открыть ваш список. Добавить желание./'
            'Чем займёмся дальше? Откроем ваш список желаний или список всех желаний? Или добавим желание?',
    'go_add': 'Скажи желание./Такс, говори желание',
    'else_add': 'Не подходит, попробуй переформулировать./Без плохих слов, пожалуйста/Попробуйте снова',
    'ok_add': 'Всё хорошо./Сохранила!/Сделано.',
    'other_list': 'Скажите "Все" или выберите "Тег"',
    'text_desire': 'Если вы хотите добавить теги назовите их. Если нет - скажите "Нет"',
    'users_list': 'Вы выполнили {} желаний, осталось {}',
    'completed_desire': 'Отлично! Зафиксировала./Круто! Фиксирую.',
    'empty_list': 'Ого. Похоже ваш список пуст. Воспользуйтесь командой "Добавить желание"',
    'add_tag': 'Назовите теги, чтобы другие пользователи смогли найти ваше желание.',
    'ne_ponel': 'Извините, я не расслышала желание. Попробуйте ещё раз.'
}
for t in TEXT:
    TEXT[t] = tuple(TEXT[t].split('/'))

HELP = {
    State.MENU: 'Скажите "Список желаний", чтобы посмотреть все желания. Скажите "Мои желания",'
                ' чтобы посмотреть ваши желания. Чтобы добавить желание, скажите "Добавить желание"',
    State.USERS_LIST: 'Скажите "Далее", чтобы посмотреть следующее желание. Скажите "Назад", чтобы '
                      'посмотреть предыдущее желание ',
    State.VIEW: 'Скажите "Далее", чтобы посмотреть следующее желание.',
    State.ADD_DESIRE: 'Скажи своё желание, и я его добавлю. Если хочешь отменить создание, скажи "Отмена"',
    State.ADD_TAGS: 'Назови теги или скажи "Нет"',
    State.CHOOSE_TAG: 'Назови теги или скажи "Нет"'
}

WORDS = {
    'exit': 'выход/хватит/пока/свидания/стоп/выйти/выключи/останови/остановить/отмена/закончить/'
            'закончи/отстань/назад/обратно/верни/вернись',
    'help': 'помощь/помоги/подсказка/подскажи/подскажите/help/правила',
    'ability': 'умеешь/можешь/могёшь/могешь',
    'repeat': 'ещё/еще/повтори/повтори-ка/повтор/понял/слышал/услышал/расслышал/прослушал/скажи/а/сказала',
    'list': 'список/список/списки/лист/желания/желание/желанию/желаний',
    'my': 'мой/моя/мои/мне/себе/себя',
    'next': 'еще/ещё/дальше/больше/вперед/вперёд/следующая/следующий/'
            'следующее/далее/не/неа/фу/нет/другой/другое/другая/другие',
    'add': 'создать/добавить/сделать/адд/эдд/добавим/сделаем',
    'complete': 'выполнил/выполнено',
    'search': 'найти/поиск',
    'tags': 'теги/тег',
    'no': 'нет/ноу/отмена',
    'all': 'все/всё/остальные'
}

for w in WORDS:
    WORDS[w] = tuple(WORDS[w].split('/'))

BUTTONS = {
    State.MENU: ('Список желаний', 'Мои желания', 'Помощь', 'Что ты умеешь?'),
    State.USERS_LIST: ('Добавить желание', 'Найти идею', 'Назад', 'Помощь'),
    State.VIEW: ('Далее', 'Назад', 'Помощь'),
    State.ADD_DESIRE: ('Отмена', 'Помощь'),
    State.ADD_TAGS: ('Отмена', 'Помощь')
}


def txt(string):
    return choice(string)


def btn(string):
    if isinstance(string, tuple):
        return list(map(lambda x: txt(x.split('/')), string))
    return txt(string.split('/')),
