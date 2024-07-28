from os.path import dirname, realpath, join
from enum import Enum
from termcolor import colored

BASE_PATH = dirname(realpath(__file__))
from_base = lambda path : join(BASE_PATH, path)
from_terraform = lambda path : join(TERRAFORM_PATH, path)


TEMPLATE_PATH = from_base("templates")
TERRAFORM_PATH = from_base("../terraform")
KEY_PATH = from_terraform("keys")
DATA_PATH = from_base("data")

PROJECT_DATA_T = dict[str, str | dict[str, dict[str, str]]]

class ActionState(Enum):
    FAILED = f"{colored('\u2717', 'red')} Failed :("
    EXISTS = "🛈 Already exists(check configuration)"
    COMPLETE = f"{colored('\u2714', 'green')} Complete :)"

BANNER = "#" + "=" * 10 + " AUTO GENERATED " + "=" * 10 + "\n\n"