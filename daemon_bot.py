import daemon, os

from slackbot_cryptocurrencies import main_program

if __name__ == '__main__':
	#here = os.path.dirname(os.path.abspath(__file__))
	here = os.getcwd()
	out = open('/tmp/LogDaemonSlackBot.log', 'w+')
	
	with daemon.DaemonContext(working_directory=here, stdout=out):
		main_program()