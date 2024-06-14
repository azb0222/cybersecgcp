# Done!

from os.path import dirname, realpath, join

BASE_PATH = dirname(realpath(__file__))

TEMPLATE_PATH = join(BASE_PATH, "templates")
TERRAFORM_PATH = join(BASE_PATH, "../terraform")
KEY_PATH = join(TERRAFORM_PATH, "keys")
DATA_PATH = join(BASE_PATH, "data")

PROJECT_DATA_T = dict[str, str | bool]


BANNER = "#" + "=" * 10 + " AUTO GENERATED " + "=" * 10 + "\n\n"