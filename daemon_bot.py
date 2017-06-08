import daemon, os

from slackbot_cryptocurrencies import main_program

if __name__ == '__main__':
	here = os.path.dirname(os.path.abspath(__file__))
	out = open('/var/log/LogDaemonSlackBot.log', 'w+')
	
	with daemon.DaemonContext():
		main_program()