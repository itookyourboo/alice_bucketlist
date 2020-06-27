from base_skill.skill import CommandHandler, BaseSkill, button
from .strings import TEXT, WORDS, txt
from .state import State

handler = CommandHandler()


class BucketListSkill(BaseSkill):
    name = 'bucketlist_skill'
    command_handler = handler


"""-----------------State.ALL-----------------"""


@handler.hello_command
def hello(req, res, session):
    res.text = txt(TEXT['hello'])
    session['state'] = State.MENU


@handler.command(words=WORDS['help'], states=State.ALL)
def help_(res, req, session):
    res.text = txt(TEXT['help'])


@handler.command(words=WORDS['ability'], states=State.ALL)
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
def repeat_(res, req, session):
    pass


"""-----------------State.MENU-----------------"""


@handler.command(words=WORDS['list'], states=State.MENU)
def get_list(res, req, session):
    if WORDS['my']:
        session['state'] = State.USERS_LIST
    else:
        session['state'] = State.OTHERS_LIST


"""-----------------State.OTHERS_LIST-----------------"""


@handler.command(words=WORDS['next'], states=State.OTHERS_LIST)
def next_desire(res, req, session):
    pass


"""-----------------State.USERS_LIST-----------------"""


@handler.command(words=WORDS['add'], states=State.USERS_LIST)
def go_add_desire(res, req, session):
    pass


@handler.command(words=WORDS['complete'], states=State.USERS_LIST)
def complete_desire(res, req, session):
    pass


@handler.command(words=WORDS['search'], states=State.USERS_LIST)
def search_desire(res, req, session):
    pass


"""-----------------State.ADD-----------------"""


@handler.undefined_command(states=State.ADD)
def add_desire(res, req, session):
    pass
