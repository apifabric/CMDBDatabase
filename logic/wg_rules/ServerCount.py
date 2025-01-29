
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
  Sum(Location.server_count, Server.id)
