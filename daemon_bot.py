import daemon

from slackbot_cryptocurrencies import main_program

with daemon.DaemonContext():
	main_program()
