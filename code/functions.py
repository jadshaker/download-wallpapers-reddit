from re import search
from json import dump, load
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
    - Required - iteration : current iteration (int)
    - Required - total : total iterations (int)
    - Optional - prefix : prefix string (str)
    - Optional - suffix : suffix string (str)
    - Optional - decimals : positive number of decimals in percent complete (int)
    - Optional - length : character length of bar (int)
    - Optional - fill : bar fill character (str)
    - Optional - end : end character (str)
    """

    filledLength = length * iteration // total
    percent = f'{(100 * iteration  / float(total)):.{decimals}f}'

    bar = fill * filledLength + '_' * (length - filledLength)

    print(f'\r{prefix} {bar} {percent}% {suffix}', end=end)

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


def adjust_image_name(image_name: str) -> str:
    """
    This function remove extra characters from image name
    - Required - image_name : image name (str)
    """

    # try to delete text between brackets ([])
    try:
        image_name = image_name[
            0:search(r'\[', image_name).span()[0]
        ] + image_name[search(r'\]', image_name).span()[1]:]
    except:
        pass

    # try to remove text between paranthesis (())
    try:
        image_name = image_name[
            0:search(r'\(', image_name).span()[0]
        ] + image_name[search(r'\)', image_name).span()[1]:]

    except:
        pass

    # remove invalid characters
    for char in '\/:*?"<>|':
        image_name = image_name.replace(char, '')

    return image_name


def get_json_data() -> dict:
    """
    This function gets data from data.json file if available, or creates data.json with user defined values
    """

    try:
        download_path, show_browser, subreddits, max_images_in_subreddit, minimum_width, minimum_height = load(
            open('./data.json')
        ).values()

        data = {
            'downloadPath': download_path,
            'showBrowser': show_browser,
            'subreddits': subreddits,
            'maxImagesInSubreddit': max_images_in_subreddit,
            'minimumWidth': minimum_width,
            'minimumHeight': minimum_height
        }

    except:
        download_path = input('Please input the wallpapers folder path: ')

        while True:
            show_browser = input(
                'Would you like to show the browser while dowloading images? (yes/no): '
            ).lower()

            if show_browser == 'yes':
                show_browser = True
                break

            elif show_browser == 'no':
                show_browser = False
                break

            else:
                print('Please try again')

        subreddits = [
            subreddit.strip() for subreddit in input(
                'Enter subreddit names seperated by commas(,):\n'
            ).split(',')
        ]

        while True:
            try:
                max_images_in_subreddit = int(
                    input('Maximum number of images per subreddit: ')
                )
                break

            except:
                print('Please try again')

        while True:
            try:
                minimum_width = int(input('Minimum width of image: '))
                break

            except:
                print('Please try again')

        while True:
            try:
                minimum_height = int(input('Minimum height of image: '))
                break

            except:
                print('Please try again')

        data = {
            'downloadPath': download_path,
            'showBrowser': show_browser,
            'subreddits': subreddits,
            'maxImagesInSubreddit': max_images_in_subreddit,
            'minimumWidth': minimum_width,
            'minimumHeight': minimum_height
        }

        dump(data, open('./data.json', 'w'))

    return data.values()
