"""FokaBot related functions"""
import re

from common import generalUtils
from common.constants import actions
from common.ripple import userUtils
from constants import serverPackets
from objects import glob

# Epic bot part.
import shlex
from bot import mainHandler

# Tillerino np regex, compiled only once to increase performance
npRegex = re.compile("^https?:\\/\\/osu\\.ppy\\.sh\\/b\\/(\\d*)")

def connect():
	"""
	Connect FokaBot to Bancho

	:return:
	"""
	glob.BOT_NAME = userUtils.getUsername(999)
	token = glob.tokens.addToken(999)
	token.actionID = actions.IDLE
	glob.streams.broadcast("main", serverPackets.userPanel(999))
	glob.streams.broadcast("main", serverPackets.userStats(999))

def disconnect():
	"""
	Disconnect FokaBot from Bancho

	:return:
	"""
	glob.tokens.deleteToken(glob.tokens.getTokenFromUserID(999))

def fokabotResponse(fro, chan, message):
	"""
	Check if a message has triggered FokaBot

	:param fro: sender username
	:param chan: channel name (or receiver username)
	:param message: chat mesage
	:return: FokaBot's response or False if no response
	"""
	cmd, vals = None, None
	for (k, v) in mainHandler.store.handlers.items():
		if message.strip().startswith(k):
			cmd, vals = k, v
			break

	if not cmd:
		return False

	if vals['privileges'] and userUtils.getPrivileges(userUtils.getID(fro)) & vals["privileges"] == 0:
		return False

	args = shlex.split(message.strip()[len(cmd):])
	syntaxargs = shlex.split(vals['syntax'])
	if vals['syntax'] != "" and len(args) < len(syntaxargs):
		return f"Wrong syntax: {cmd} {vals['syntax']}"

	return mainHandler.store.call_command(cmd, fro, chan, args)