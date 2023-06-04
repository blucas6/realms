from gameclient import GameClient
from gameserver import GameServer

s = GameServer()

g = GameClient(s.sites[0])
