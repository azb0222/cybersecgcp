from os.path import dirname, realpath, join
from enum import Enum
from termcolor import colored

BASE_PATH = dirname(realpath(__file__))

TEMPLATE_PATH = join(BASE_PATH, "templates")
TERRAFORM_PATH = join(BASE_PATH, "../terraform")
KEY_PATH = join(TERRAFORM_PATH, "keys")
DATA_PATH = join(BASE_PATH, "data")

PROJECT_DATA_T = dict[str, str | dict[str, dict[str, str]]]

class ActionState(Enum):
    FAILED = f"{colored('\u2717', 'red')} Failed :("
    EXISTS = "🛈 Already exists(check configuration)"
    COMPLTE = f"{colored('\u2714', 'green')} Complete :)"

BANNER = "#" + "=" * 10 + " AUTO GENERATED " + "=" * 10 + "\n\n"