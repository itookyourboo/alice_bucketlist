from base_skill.skill import button
from .strings import btn, BUTTONS


def default_buttons(func):
    def wrapper(req, res, session):
        func(req, res, session)
        if session['state'] not in BUTTONS:
            return

        if len(res.buttons) == 0:
            res.buttons = [button(x) for x in btn(BUTTONS.get(session['state'], []))]
        else:
            for x in btn(BUTTONS.get(session['state'], [])):
                res.buttons.append(button(x))

    return wrapper


def save_res(func):
    def wrapper(req, res, session):
        func(req, res, session)
        session['last_text'] = None
        session['last_tts'] = None

        session['last_text'] = res.text
        session['last_tts'] = res.tts

    return wrapper


def normalize_tts(func):
    def wrapper(req, res, session):
        func(req, res, session)
        res.tts = res.tts.replace('тест', 'т+эст').replace('Гааааааляяяяяяяяя', 'Га а а аля')

    return wrapper
