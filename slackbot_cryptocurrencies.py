import os
import time

from slackclient import SlackClient

from KrakenAPI import KrakenPublic

slack_token = os.environ["SLACK_API_TOKEN"]
sc = SlackClient(slack_token)

def createMessage():
	kraken=KrakenPublic()
	message="Server Time: "+kraken.getTime()+"\n\n"
	currency=[kraken.getBitcoin(), kraken.getEther()]

	for c in currency:
		pct=(c['high']/c['low'])-1
		message += "*" + c['symbol'] + "* (" + str(c['nb']) + " trades today)" + "\tH: " + str(c['high']) + "€; L: " + str(c['low']) + "€; "
		message += "Volatility: " + str(int((c['high']-c['low'])*100)/100) + "€ (" + str(int(pct*10000)/100) + "%); "
		pct=(c['current']/c['opening'])-1
		message+= "Openning: "+ str(c['opening']) + "€ (00:00 UTC); *Current: " + str(c['current']) + "€* (" + str(int(pct*10000)/100) + "%)" + "\n" 

	return message

if sc.rtm_connect():
    while True:
        resp = sc.rtm_read()
        
        if len(resp)>0:
        	resp=resp[0]
        	#print(resp)
        	
        	if 'type' in resp:
	        	
	        	if resp['type']=='desktop_notification' and resp['content'].find('@blockbot'):
	        		
	        		msg=createMessage()
	        		sc.rtm_send_message(resp['channel'], msg)
	        		# resp = (sc.rtm_read())[0]
	        		
	        		# while resp['ok'] is not True:
	        		# 	sc.rtm_send_message(resp['channel'], msg)
	        		# 	resp = (sc.rtm_read())[0]
        time.sleep(1)
else:
    print("Connection Failed, invalid token?")