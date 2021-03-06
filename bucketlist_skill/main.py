from base_skill.skill import CommandHandler, BaseSkill, button
from .strings import TEXT, WORDS, txt, HELP, btn
from .state import State
from .ui_helper import default_buttons, save_res
from .desire_helper import Desire, User
from difflib import SequenceMatcher as sequence

handler = CommandHandler()


class BucketListSkill(BaseSkill):
    name = 'bucketlist_skill'
    command_handler = handler


"""-----------------State.ALL-----------------"""


@handler.hello_command
@save_res
@default_buttons
def hello(req, res, session):
    res.text = txt(TEXT['hello'])
    User.add_user(req.user_id)
    session['state'] = State.MENU


@handler.command(words=WORDS['help'], states=State.ALL)
@save_res
@default_buttons
def help_(req, res, session):
    res.text = HELP[session['state']]


@handler.command(words=WORDS['ability'], states=State.ALL)
@save_res
@default_buttons
def ability_(req, res, session):
    res.text = txt(TEXT['ability'])


@handler.command(words=WORDS['exit'], states=State.ALL)
@default_buttons
def exit_(req, res, session):
    if session['state'] == State.MENU:
        res.end_session = True
        session.clear()
        res.text = txt(TEXT['bye'])
    else:
        session['state'] = State.MENU
        res.text = txt(TEXT['back'])


@handler.command(words=WORDS['repeat'], states=State.ALL)
@default_buttons
def repeat_(req, res, session):
    res.text = session.get('last_text', 'Нечего повторять')
    res.tts = session.get('last_tts', 'Нечего повторять')


"""-----------------State.MENU-----------------"""


@handler.command(words=WORDS['list'], states=(State.MENU, State.USERS_LIST))
@save_res
@default_buttons
def get_list(req, res, session):
    if any(word in req.tokens for word in WORDS['my']):
        session['state'] = State.USERS_LIST
        completed_desires = Desire.get_completed_desires(req.user_id)
        uncompleted_desires = Desire.get_uncompleted_desires(req.user_id)
        len_compl, len_uncompl = len(completed_desires), len(uncompleted_desires)
        if len_compl == 0 and len_uncompl == 0:
            res.text = txt(TEXT['empty_list'])
        elif len_compl == 0:
            res.text = txt(TEXT['users_list']).format(len_compl, Desire.morph(len_compl), len_uncompl)
            res.text = res.text + '\nВы не выполнили:\n' + '.\n'.join(x[1] for x in uncompleted_desires)
        elif len_uncompl == 0:
            res.text = txt(TEXT['users_list']).format(len_compl, Desire.morph(len_compl), len_uncompl)
        else:
            res.text = txt(TEXT['users_list']).format(len_compl, Desire.morph(len_compl), len_uncompl)
            res.text = res.text + '\nВы не выполнили:\n' + '\n'.join(x[1] for x in uncompleted_desires)
        session['users_list_count'] = 0
        session['users_desire_list'] = Desire.get_desires(req.user_id, local=True)
    else:
        session['state'] = State.CHOOSE_TAG
        desire_tags = Desire.get_tags()
        res.buttons = [button(x) for x in desire_tags]
        res.text = txt(TEXT['other_list'])
        res.tts = res.tts + "Например sil <[300]>" + "sil <[400]>".join(desire_tags)


@handler.undefined_command(states=State.CHOOSE_TAG)
@save_res
@default_buttons
def choose_tag(req, res, session):
    if any(x in req.tokens for x in WORDS['all']):
        session['users_list_count'] = 0
        session['users_desire_list'] = Desire.get_desires(req.tokens, local=False)
        session['state'] = State.VIEW
        res.text = txt(TEXT['intro']) + '\n' + session['users_desire_list'][session['users_list_count']][1]
    else:
        result = Desire.find_by_tags(req.user_id, req.tokens)
        if len(result) == 0:
            res.text = 'Извините, я ничего не нашла.'
        else:
            session['users_list_count'] = 0
            session['users_desire_list'] = result
            session['state'] = State.VIEW
            res.text = txt(TEXT['intro']) + '\n' + session['users_desire_list'][session['users_list_count']][1]


"""-----------------State.LIST-----------------"""


@handler.command(words=WORDS['next'], states=State.VIEW)
@save_res
@default_buttons
def next_desire(req, res, session):
    session['users_list_count'] += 1
    session['users_list_count'] %= len(session['users_desire_list'])
    res.text = session['users_desire_list'][session['users_list_count']][1]


@handler.command(words=WORDS['add'], states=State.VIEW)
@save_res
@default_buttons
def add_to_my(req, res, session):
    desire = session['users_desire_list'][session['users_list_count']]
    Desire.add_to_user(req.user_id, desire[0])
    res.text = 'Добавила! Скажите дальше, чтобы показать ещё.'


"""-----------------State.USERS_LIST-----------------"""


@handler.command(words=WORDS['add'], states=State.USERS_LIST)
@save_res
@default_buttons
def go_add_desire(req, res, session):
    res.text = txt(TEXT['go_add'])
    session['state'] = State.ADD_DESIRE


@handler.command(words=WORDS['complete'], states=State.USERS_LIST)
@save_res
@default_buttons
def complete_desire(req, res, session):
    found, desire = Desire.find_by_text(req.user_id, req.text)
    if found:
        Desire.complete_desire(req.user_id, desire[0])
        res.text = txt(TEXT['completed_desire'])
    else:
        res.text = txt(TEXT['ne_ponel'])


@handler.command(words=WORDS['delete'], states=State.USERS_LIST)
@save_res
@default_buttons
def delete_desire(req, res, session):
    found, desire = Desire.find_by_text(req.user_id, req.text)
    if found:
        Desire.complete_desire(req.user_id, desire[0])
        res.text = txt(TEXT['deleted_desire'])
    else:
        res.text = txt(TEXT['ne_ponel'])


@handler.command(words=WORDS['search'], states=State.USERS_LIST)
@save_res
@default_buttons
def search_desire(req, res, session):
    session['state'] = State.CHOOSE_TAG
    desire_tags = Desire.get_tags()
    res.buttons = [button(x) for x in desire_tags]
    res.text = txt(TEXT['other_list'])
    res.tts += " ".join(desire_tags)


@handler.command(words=WORDS['more'], states=State.USERS_LIST)
@save_res
@default_buttons
def more(req, res, session):
    res.text = 'Вы выполнили: ' + '\n'.join([x[1] for x in Desire.get_uncompleted_desires(req.user_id)])
    res.text = res.text + '\nВы можете добавить свое желание, найти идею, выполнить или удалить идею.'


"""-----------------State.ADD_DESIRE-----------------"""


@handler.undefined_command(states=State.ADD_DESIRE)
@save_res
@default_buttons
def add_desire(req, res, session):
    if not req.dangerous:
        res.text = txt(TEXT['add_tag'])
        session['text_desire'] = req.text.capitalize()
        session['state'] = State.ADD_TAGS
    else:
        res.text = txt(TEXT['else_add'])


"""-----------------State.ADD_TAGS-----------------"""


@handler.undefined_command(states=State.ADD_TAGS)
@save_res
@default_buttons
def add_tags(req, res, session):
    if any(word in req.tokens for word in WORDS['no']):
        Desire.add_desire(session['text_desire'], 'все', req.user_id)
    else:
        res.text = txt(TEXT['ok_add'])
        Desire.add_desire(session['text_desire'], ','.join(req.tokens).strip(','), req.user_id)
        session['state'] = State.MENU
        res.text += '\n' + txt(TEXT['back'])


@handler.undefined_command(states=State.ALL)
@save_res
@default_buttons
def wtf(req, res, session):
    res.text = HELP[session['state']]
    # TODO: write to wtf.txt
