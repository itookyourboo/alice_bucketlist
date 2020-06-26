WORDS = {
    'exit': 'выход/хватит/пока/свидания/стоп/выйти/выключи/останови/остановить/отмена/закончить/'
            'закончи/отстань/назад/обратно/верни/вернись',
    'help': 'помощь/помоги/подсказка/подскажи/подскажите/help/правила',
    'ability': 'умеешь/можешь/могёшь/могешь',
    'repeat': 'ещё/еще/повтори/повтори-ка/повтор/понял/слышал/услышал/расслышал/прослушал/скажи/а/сказала',
    'list': 'список/список/списки/лист',
    'my': 'мой/моя/мои/мне/себе/себя',
    'next': 'еще/ещё/дальше/больше/вперед/вперёд/следующая/следующий/'
            'следующее/далее/не/неа/фу/нет/другой/другое/другая/другие',
    'add': 'создать/добавить/сделать/адд/эдд',
    'complete': 'выполнил/выполнено',
    'search': 'найти/поиск'
}
for w in WORDS:
    WORDS[w] = tuple(WORDS[w].split('/'))
