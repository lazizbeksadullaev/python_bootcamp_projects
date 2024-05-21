import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuit_testing_bot.settings')
django.setup()

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

TOKEN = '5219475550:AAHCgBmdXctQ-IradRkNIIdGBXdYT08kmHs'
