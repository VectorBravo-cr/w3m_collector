import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

BASIC_LOGIN = os.environ.get('BASIC_LOGIN')
BASIC_PASS = os.environ.get('BASIC_PASS')

MINERS_NETWORK = os.environ.get('MINERS_NETWORK')

MINERS_CONFIGURATION = os.environ.get("MINERS_CONFIGURATION")

REDIS_CONN = os.environ.get('REDIS_CONN')

API_PREFIX = os.environ.get('API_PREFIX')
DEVICE_ROUTER_PREFIX = os.environ.get('DEVICE_ROUTER_PREFIX')
CALC_PROFIT_ROUTER_PREFIX = os.environ.get('CALC_PROFIT_ROUTER_PREFIX')

VERSION = os.environ.get('VERSION')

