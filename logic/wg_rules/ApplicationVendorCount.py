
from logic_bank.logic_bank import Rule
from database.models import *

def init_rule():
  Sum(Vendor.application_count, Application.id)
