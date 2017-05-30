import krakenex

from datetime import datetime

class KrakenPublic:

	def __init__(self):
		self.krak=krakenex.API()

	def convertStoF(self, val):
		return int(float(val)*100)/100

	def getCurrency(self, name):
		xbt=(self.krak.query_public('Ticker',{'pair':name})['result'])[name]
		info={}
		info['symbol']=name
		info['current']=self.convertStoF(xbt['c'][0])
		info['high']=self.convertStoF(xbt['h'][0])
		info['low']=self.convertStoF(xbt['l'][0])
		info['opening']=self.convertStoF(xbt['o'])
		info['nb']=xbt['t'][0]
		return info

	def getBitcoin(self):
		return self.getCurrency('XXBTZEUR')

	def getEther(self):
		return self.getCurrency('XETHZEUR')

	def getTime(self):
		timestamp=self.krak.query_public('Time')['result']
		return datetime.fromtimestamp(int(timestamp['unixtime'])).strftime('%Y-%m-%d %H:%M:%S')

def main():
	k=KrakenPublic()
	print(k.getBitcoin())

if __name__ == '__main__':
	main()