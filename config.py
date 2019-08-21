import os
import sys
from flask import request
from configparser import ConfigParser, NoSectionError


APP_NAME = "acornsgrow/required-labels"


class ConfigException(Exception):
    pass


config_filename = "custom.conf"
config = ConfigParser()
config.read(config_filename)

try:
    if request.GET.get('required_any') or request.GET.get('required_all'):
        required_any = request.GET.get('required_any')
        required_all = request.GET.get('required_all')
        banned = request.GET.get('banned')
        GITHUB_TOKEN = config.get('GitHub', 'token')
        GITHUB_SECRET = config.get('GitHub', 'secret')
    else:
        required_any = config.get('Labels', 'required-labels-any')
        required_all = config.get('Labels', 'required-labels-all')
        banned = config.get('Labels', 'banned-labels')
        GITHUB_TOKEN = config.get('GitHub', 'token')
        GITHUB_SECRET = config.get('GitHub', 'secret')
except NoSectionError:
    required_any = os.environ.get('REQUIRED_LABELS_ANY', None)
    required_all = os.environ.get('REQUIRED_LABELS_ALL', None)
    banned = os.environ.get('BANNED_LABELS', None)
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', None)
    GITHUB_SECRET = os.environ.get('GITHUB_SECRET', None)

REQUIRED_LABELS_ANY = required_any.split(',') if required_any else None
REQUIRED_LABELS_ALL = required_all.split(',') if required_all else None
BANNED_LABELS = banned.split(',') if banned else None


UNIT_TESTING = any([arg for arg in sys.argv if 'test' in arg])


if not UNIT_TESTING:
    labels_configured = any([REQUIRED_LABELS_ANY, REQUIRED_LABELS_ALL, BANNED_LABELS])
    credentials_configured = all([GITHUB_TOKEN])
    if not labels_configured or not credentials_configured:
        raise ConfigException(
            "Please ensure your config file has a [Labels] and [Github] section.\n"
            "Did you forget to create a configuration file?\n"
            "You can do this by running\033[1m cp {0}.template {0} \033[0m\n"
            "You can also add REQUIRED_LABELS_ALL, REQUIRED_LABELS_ANY, or BANNED_LABELS along with "
            "GITHUB_TOKEN as environment variables"
            "".format(config_filename)
        )
