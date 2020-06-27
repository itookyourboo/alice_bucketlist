from base_skill.skill import CommandHandler, BaseSkill, button
from .strings import TEXT, WORDS, txt, HELP
from .state import State
from .ui_helper import default_buttons, save_res
from .desire_helper import Desire, User

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
@default_buttons
def help_(res, req, session):
    res.text = txt(HELP[session['state']])


@handler.command(words=WORDS['ability'], states=State.ALL)
@default_buttons
def ability_(res, req, session):
    res.text = txt(TEXT['ability'])


@handler.command(words=WORDS['exit'], states=State.ALL)
def exit_(res, req, session):
    if session['state'] == State.MENU:
        res.end_session = True
        session.clear()
        res.text = txt(TEXT['bye'])
    else:
        session['state'] = State.MENU
        res.text = txt(TEXT['back'])


@handler.command(words=WORDS['repeat'], states=State.ALL)
@default_buttons
def repeat_(res, req, session):
    res.text = session['last_text']
    res.tts = session['last_tts']


"""-----------------State.MENU-----------------"""


@handler.command(words=WORDS['list'], states=State.MENU)
@save_res
@default_buttons
def get_list(res, req, session):
    if any(word in req.tokens for word in WORDS['my']):
        session['state'] = State.USERS_LIST

    else:
        session['state'] = State.OTHERS_LIST


"""-----------------State.OTHERS_LIST-----------------"""


@handler.command(words=WORDS['next'], states=State.OTHERS_LIST)
@save_res
@default_buttons
def next_desire(res, req, session):
    pass


@handler.command(words=WORDS['tags'], states=State.OTHERS_LIST)
@save_res
@default_buttons
def tags(res, req, session):
    pass


"""-----------------State.USERS_LIST-----------------"""


@handler.command(words=WORDS['add'], states=State.USERS_LIST)
@save_res
@default_buttons
def go_add_desire(res, req, session):
    res.text = txt(TEXT['go_add'])
    session['state'] = State.ADD


@handler.command(words=WORDS['complete'], states=State.USERS_LIST)
@save_res
@default_buttons
def complete_desire(res, req, session):
    pass


@handler.command(words=WORDS['search'], states=State.USERS_LIST)
@save_res
@default_buttons
def search_desire(res, req, session):
    session['state'] = State.OTHERS_LIST
    res.text = txt(TEXT['other_list'])


"""-----------------State.ADD_DESIRE-----------------"""


@handler.undefined_command(states=State.ADD)
@save_res
@default_buttons
def add_desire(res, req, session):
    if req.dangerous:
        res.text = txt(TEXT['add_tag'])
        session['text_desire'] = req.command.capitalize()

    else:
        res.text = txt(TEXT['else_add'])


"""-----------------State.ADD_TAGS-----------------"""


@handler.undefined_command(states=State.ADD_TAGS)
@save_res
@default_buttons
def add_tags(res, req, session):
    res.text = txt(TEXT['ok_add'])
    Desire.add_desire(session['text_desire'], ','.join(req.tokens).strip(','), req.user_id)

