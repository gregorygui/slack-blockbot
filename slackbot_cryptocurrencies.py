import os
import time

from slackclient import SlackClient

from KrakenAPI import KrakenPublic

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

kraken=KrakenPublic()

def getBotID(path):
	try:
		f=open(os.path.join(path, 'bot.config'), 'r')
	except Exception as e:
		print(e)
	
	try:
		l=f.readline()
		f.close()
		#print((l.split(':'))[1])
		return (l.split(':'))[1]
	except Exception as e:
		print(e)

def getBotName(path):
	try:
		f=open(os.path.join(path, 'bot.config'), 'r')
	except Exception as e:
		print(e)
	
	try:
		l=f.readline()
		f.close()
		#print((l.split(':'))[0])
		return (l.split(':'))[0]
	except Exception as e:
		print(e)

botID=getBotID(os.getcwd())
botname=getBotName(os.getcwd())

vul=['encul', 'fdp', 'ntm', 'fuck']

def getChans():
	chans=dict()
	try:
		f=open('chans.txt', 'r')
	except Exception as e:
		print(e)
	
	l=f.readline()
	
	while l:
		try:
			v=l.split(':')
			chans[v[0]]=v[1]
			l=f.readline()
		except Exception as e:
			print(e)
			break

	f.close()

	return chans

def createMessage():
	message="Server Time: "+kraken.getTime()+"\n\n"
	currency=[kraken.getBitcoin(), kraken.getEther()]

	for c in currency:
		pct=(c['high']/c['low'])-1
		message += "*" + c['symbol'] + "* (" + str(c['nb']) + " trades today)" + "\tH: " + str(c['high']) + "€; L: " + str(c['low']) + "€; "
		message += "Volatility: " + str(int((c['high']-c['low'])*100)/100) + "€ (" + str(int(pct*10000)/100) + "%); "
		pct=(c['current']/c['opening'])-1
		message+= "Openning: "+ str(c['opening']) + "€ (00:00 UTC); *Current: " + str(c['current']) + "€* (" + str(int(pct*10000)/100) + "%)" + "\n" 

	return message

def message_help():
	msg="My aim is to help people enjoying *crypto-trading* ~and fucking the world~.\n\"_Speculation is pejorative_\""
	msg+="\nWhat can I understand for the moment:\n"
	msg+="\n\t- *hey/hello*: welcome message"
	msg+="\n\t- *help*: print this little help"
	msg+="\n\t- *time*: print Time Server"
	msg+="\n\t- *@blockbot* (only): print market informations about Bitcoin and Ehter"

	return msg

def message_time():
	return "Kraken - Time Server "+kraken.getTime()

def message_hello():
	return "Hey, *Welcome* to the *Blockchain Jungle* !"

def message_vulg():
	return "Fais le malin aujourd'hui, tu le feras moins demain quand je serai *millionaire*."

def word_analyze(resp):
	msg=""
	words=(resp['text']).split()

	if ('<@'+botID+'>') in words[0]:
		if len(words)==1:
			words=[]
		else:
			words=words[1:] 

	if len(words)==0:
		msg=createMessage()
	else:
		for w in words:
			if 'help' in w.lower():
				msg=message_help()
				break
			elif 'hey' in w.lower():
				msg=message_hello()
				break
			elif 'hello' in w.lower():
				msg=message_hello()
				break
			elif 'time' in w.lower():
				msg=message_time()
				break

	for w in vul:
		if w in (resp['text']).lower():
			msg=message_vulg()

	if len(msg)>0:
		sc.rtm_send_message(resp['channel'],msg)
	else:
		sc.rtm_send_message(resp['channel'],"Sorry, I can't understand ~yet~")

def handle_message(resp, chans):
	in_chan=0

	for k in chans:
		if resp['channel']==chans[k]:
			in_chan=1

	if in_chan and (('<@'+botID+'>') in (resp['text']).split()):
		word_analyze(resp)
		print("Query in channel "+chans[k]+" by "+resp['user']+": \'"+resp['text']+"\'")
	elif not in_chan:
		word_analyze(resp)
		print("Query direct "+chans[k]+" by "+resp['user']+": \'"+resp['text']+"\'")

def handle_response(resp):
	chans=getChans()

	if 'type' in resp:
		if resp['type']=='error':
			sc.rtm_send_message(chans['testbots'], (resp['error'])['msg'])
		
		elif (resp['type']=='message') and (('text' and 'channel') in resp):
			if 'reply_to' not in resp:
				#print(resp)
				handle_message(resp, chans)	

def main_program():
	if sc.rtm_connect():
	    while True:
        	resp = sc.rtm_read()
        
	        if len(resp)>0:
        		resp=resp[0]
        		handle_response(resp)
	        time.sleep(1)
	else:
	    print("Connection Failed, invalid token?")

def main():
	main_program()

if __name__ == '__main__':
	main()