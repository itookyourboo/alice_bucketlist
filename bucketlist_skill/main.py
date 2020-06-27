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


@handler.command(words=WORDS['list'], states=State.MENU)
@save_res
@default_buttons
def get_list(req, res, session):
    if any(word in req.tokens for word in WORDS['my']):
        session['state'] = State.USERS_LIST
        completed_desires = Desire.get_completed_desires(req.user_id)
        uncompleted_desires = Desire.get_uncompleted_desires(req.user_id)
        if len(completed_desires) == 0 and len(uncompleted_desires) == 0:
            res.text = txt(TEXT['empty_list'])
        elif len(completed_desires) == 0:
            res.text = txt(TEXT['users_list']).format(len(completed_desires), len(uncompleted_desires))
            res.text = res.text + '\nВы не выполнили:\n' + '\n'.join(x[1] for x in uncompleted_desires)
        elif len(uncompleted_desires) == 0:
            res.text = txt(TEXT['users_list']).format(len(completed_desires), len(uncompleted_desires))
        else:
            res.text = txt(TEXT['users_list']).format(len(completed_desires), len(uncompleted_desires))
            res.text = res.text + '\nВы не выполнили:\n' + '\n'.join(x[1] for x in uncompleted_desires)
        session['users_list_count'] = 0
        session['users_desire_list'] = Desire.get_desires(req.user_id, local=True)
    else:
        session['state'] = State.CHOOSE_TAG
        desire_tags = Desire.get_tags()
        res.buttons = [button(x) for x in desire_tags]
        res.text = txt(TEXT['other_list'])
        res.tts += "sil <[300]>" + "sil <[400]>".join(desire_tags)


@handler.undefined_command(states=State.CHOOSE_TAG)
@save_res
@default_buttons
def choose_tag(req, res, session):
    if 'все' in req.tokens:
        session['users_list_count'] = 0
        session['users_desire_list'] = Desire.get_desires(req.tokens, local=False)
        session['state'] = State.VIEW
        res.text = session['users_desire_list'][session['users_list_count']][1]
    else:
        result = Desire.find_by_tags(req.user_id, req.tokens)
        if len(result) == 0:
            res.text = 'Извините, я ничего не нашла.'
        else:
            session['users_list_count'] = 0
            session['users_desire_list'] = result
            session['state'] = State.VIEW
            res.text = session['users_desire_list'][session['users_list_count']][1]


"""-----------------State.LIST-----------------"""


@handler.command(words=WORDS['next'], states=(State.VIEW, State.USERS_LIST))
@save_res
@default_buttons
def next_desire(req, res, session):
    if State.VIEW:
        res.text = Desire.get_random_desire(req.user_id)[1]
    else:
        session['users_list_count'] += 1
        session['users_list_count'] %= session['users_desire_list']
        res.text = session['users_desire_list'][session['users_list_count']][1]


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
    users_desires = Desire.get_desires(req.user_id, local=True)
    for desire in users_desires:
        if 0.5 < sequence(None, req.command, desire.text).ratio():
            Desire.complete_desire(req.user_id, desire.id)
            break
    res.text = txt(TEXT['completed_desire'])


@handler.command(words=WORDS['search'], states=State.USERS_LIST)
@save_res
@default_buttons
def search_desire(req, res, session):
    session['state'] = State.CHOOSE_TAG
    desire_tags = Desire.get_tags()
    res.buttons = [button(x) for x in desire_tags]
    res.text = txt(TEXT['other_list'])
    res.tts += " ".join(desire_tags)


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


@handler.undefined_command(states=State.ALL)
@save_res
@default_buttons
def wtf(req, res, session):
    res.text = HELP[session['state']]
    # TODO: write to wtf.txt
