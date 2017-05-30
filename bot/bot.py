# coding: utf-8

import os
import recastai

from flask import jsonify

from .krakenData import KrakenPublic

def createMessage():
	kraken=KrakenPublic()
	message="Server Time: "+kraken.getTime()+"\n\n"
	currency=[kraken.getBitcoin(), kraken.getEther()]

	for c in currency:
		pct=(c['high']/c['low'])-1
		message += c['symbol'] + " (" + str(c['nb']) + " trades today)" + "\tH: " + str(c['high']) + "€; L: " + str(c['low']) + "€; "
		message += "Volatility: " + str(int((c['high']-c['low'])*100)/100) + "€ (" + str(int(pct*10000)/100) + "%); "
		pct=(c['current']/c['opening'])-1
		message+= "Openning: "+ str(c['opening']) + "€ (00:00 UTC); Current: " + str(c['current']) + "€ (" + str(int(pct*10000)/100) + "%)" + "\n" 

	return message

def bot(payload):
  connect = recastai.Connect(token=os.environ['REQUEST_TOKEN'], language=os.environ['LANGUAGE'])
  request = recastai.Request(token=os.environ['REQUEST_TOKEN'])

  message = connect.parse_message(payload)

  message.content=createMessage()

  response = request.converse_text(message.content, conversation_token=message.sender_id)

  replies = [{'type': 'text', 'content': r} for r in response.replies]
  connect.send_message(replies, message.conversation_id)

  return jsonify(status=200)
