from selenium.webdriver import Chrome
from colorama import init, Fore, Back, Style
from selenium.webdriver.chrome.options import Options


def styled(text: str, fore: str = 'white', back: str = 'black', style: str = 'normal') -> None:
    """
    This function returns styled text
    - text     - Required : text to print (str)
    - fore      - Optional : output color (str)
    - back      - Optional : output background (str)
    - style     - Optional : output style (str)
    """

    # from colorama import init, Fore, Back, Style

    fore = fore.upper()
    back = back.upper()
    style = style.upper()

    init(autoreset=True)

    FORE = {
        'RED': Fore.RED,
        'BLUE': Fore.BLUE,
        'CYAN': Fore.CYAN,
        'GREEN': Fore.GREEN,
        'BLACK': Fore.BLACK,
        'RESET': Fore.RESET,
        'WHITE': Fore.WHITE,
        'YELLOW': Fore.YELLOW,
        'MAGENTA': Fore.MAGENTA,
        'LIGHTRED': Fore.LIGHTRED_EX,
        'LIGHTBLUE': Fore.LIGHTBLUE_EX,
        'LIGHTCYAN': Fore.LIGHTCYAN_EX,
        'LIGHTBLACK': Fore.LIGHTBLACK_EX,
        'LIGHTGREEN': Fore.LIGHTGREEN_EX,
        'LIGHTWHITE': Fore.LIGHTWHITE_EX,
        'LIGHTYELLOW': Fore.LIGHTYELLOW_EX,
        'LIGHTMAGENTA': Fore.LIGHTMAGENTA_EX
    }

    BACK = {
        'RED': Back.RED,
        'BLUE': Back.BLUE,
        'CYAN': Back.CYAN,
        'GREEN': Back.GREEN,
        'BLACK': Back.BLACK,
        'RESET': Back.RESET,
        'WHITE': Back.WHITE,
        'YELLOW': Back.YELLOW,
        'MAGENTA': Back.MAGENTA,
        'LIGHTRED': Back.LIGHTRED_EX,
        'LIGHTBLUE': Back.LIGHTBLUE_EX,
        'LIGHTCYAN': Back.LIGHTCYAN_EX,
        'LIGHTBLACK': Back.LIGHTBLACK_EX,
        'LIGHTGREEN': Back.LIGHTGREEN_EX,
        'LIGHTWHITE': Back.LIGHTWHITE_EX,
        'LIGHTYELLOW': Back.LIGHTYELLOW_EX,
        'LIGHTMAGENTA': Back.LIGHTMAGENTA_EX
    }

    STYLE = {
        'DIM': Style.DIM,
        'BRIGHT': Style.BRIGHT,
        'NORMAL': Style.NORMAL,
        'RESET_ALL': Style.RESET_ALL
    }

    return f"{FORE[fore]}{BACK[back]}{STYLE[style]}{text}{STYLE['RESET_ALL']}"


def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', decimals: int = 1, length: int = 100, fill: str = '█', end: str = '\r') -> str:
    """
    This function prints a progress bar and returns the current bar
    iteration   - Required  : current iteration (int)
    total       - Required  : total iterations (int)
    prefix      - Optional  : prefix string (str)
    suffix      - Optional  : suffix string (str)
    decimals    - Optional  : positive number of decimals in percent complete (int)
    length      - Optional  : character length of bar (int)
    fill        - Optional  : bar fill character (str)
    end         - Optional  : end character (str)
    """

    filledLength = length * iteration // total
    percent = f'{(100 * iteration  / float(total)):.{decimals}f}'

    bar = fill * filledLength + '-' * (length - filledLength)

    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=end)

    # Print New Line on Complete
    if iteration == total:
        print()


def initiate_driver(headless: bool = False, logs: bool = True, switches: bool = True, use_profile: bool = False, profile_path: str = '/') -> Chrome:
    """
    This function initiates a chrome driver and returns it
    - Optional - headless       : hide driver (bool)
    - Optional - log            : show logs (bool)
    - Optional - switches       : show switches (bool)
    - Optional - use_profile    : use chrome profile (bool)
    - Optional - profile_path   : profile path from chrome (str)
    """

    # from selenium.webdriver import Chrome
    # from selenium.webdriver.chrome.options import Options

    options = Options()
    if headless:
        options.add_argument('--headless')

    if logs == False:
        options.add_argument('--log-level=3')

    if switches == False:
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

    if use_profile:
        # 'user-data-dir=C:\\Users\\USER\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1'
        options.add_argument(profile_path)

    return Chrome(options=options)
