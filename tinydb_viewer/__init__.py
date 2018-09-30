from flask import Flask

app = Flask(__name__)

from .main import TinyDB
from .views import index
from .api import create_table, edit_record, delete_record
