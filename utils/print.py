import colorama
from colorama import Fore, Style

colorama.init()


def style_msg(msg, category="info", decorator=False, exit_category='reset') -> str:
    """ Style a text string for printing

        :param msg: string to be formatted
        :type msg: str

        :param category: one of 'success', 'info', 'debug', 'warn', or 'error'
        :type category: str

        :param exit_category: category to switch back to at end of msg. [category options] + 'reset'
        :type category: str

        :param decorator: add funky lines around the msg
        :type decorator: bool

        :returns formatted string with colours!

        """
    categories = {
        'success': Fore.GREEN,
        'info': Fore.BLUE,
        'debug': Fore.CYAN,
        'warn': Fore.YELLOW,
        'error': Fore.MAGENTA
    }
    if not isinstance(msg, str):
        msg = str(msg)

    return categories[category] + \
        (' ----> ' if decorator else '') + \
        msg + \
        (categories[category] + ' <---- ' if decorator else '') + \
        (Style.RESET_ALL if exit_category == 'reset' else categories[exit_category])


def print_msg(msg, category="info", decorator=True, exit_category='reset'):
    """ Print a coloured text string

       :param msg: string to be formatted
       :type msg: str

       :param category: one of 'success', 'info', 'debug', 'warn', or 'error'
       :type category: str

       :param decorator: add funky lines around the msg
       :type decorator: bool

       :param exit_category: category to switch back to at end of msg. [category options] + 'reset'
       :type category: str


    """
    print(style_msg(msg, category, decorator, exit_category))


def multi_style_msg(msg_list, default_category="info", decorator=False):
    msg = ''
    for item in msg_list:
        if isinstance(item, str):
            msg += style_msg(item, category=default_category)
        elif isinstance(item, (tuple, list)) and len(item) > 0:
            cat = item[1] if len(item) == 2 else 'info'
            msg += style_msg(item[0], category=cat)
    return style_msg(msg, category=default_category, decorator=decorator)

