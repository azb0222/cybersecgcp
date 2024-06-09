from os.path import dirname, realpath, join

BASE_PATH = dirname(realpath(__file__))

TEMPLATE_PATH = join(BASE_PATH, "template")
TERRAFORM_PATH = join(BASE_PATH, "../terraform")

BANNER = "\n\n#" + "=" * 10 + " AUTO GENERATED " + "=" * 10

PROJECT_ID_PREFIX = "umass-cybersec"
PROVIDERS = [
    {
        "alias": "general",
        "project": "general",
        "credentials": "general"
    }, 
    {
        "alias": "training",
        "project": "training",
        "credentials": "training"
    }, 
]