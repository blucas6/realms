from sites import Sites
from config import *
class GameServer:
    def __init__(self):
        #creating the sites
        self.sites = [Sites("A"), Sites("B"), Sites("C"), Sites("D")]
        