import krakenex

from datetime import datetime

Currency=['EUR', 'USD', 'GBP', 'JPY', 'CAD']

class KrakenPublic:

	def __init__(self):
		self.krak=krakenex.API()

	def convertStoF(self, val):
		return round(float(val),2)

	def getCurrency_3(self, pairname):

		# for k in (self.krak.query_public('AssetPairs'))['result']:
		# 	print(k)
		
		xbt=(self.krak.query_public('Ticker',{'pair':pairname})['result'])[pairname]
		info={}

		info['current']=self.convertStoF(xbt['c'][0])
		info['high']=self.convertStoF(xbt['h'][0])
		info['low']=self.convertStoF(xbt['l'][0])
		info['opening']=self.convertStoF(xbt['o'])
		info['nb']=xbt['t'][0]

		return info

	def getCurrency_2(self, first, second):
		pairname='X'+first

		if second in Currency:
			pairname+='Z'
		else:
			pairname+='X'

		pairname+=second

		try:
			
			info = self.getCurrency_3(pairname)
			info['symbol']=first+' '+second
			return info
		
		except:
			return None

		return info

	def getCurrency(self, first, second):

		i=self.getCurrency_2(first, second)

		if i:
			return i
		else:
			return self.getCurrency_2(second, first)

	def getBitcoin(self):
		return self.getCurrency('XBT', 'EUR')

	def getEther(self):
		return self.getCurrency('ETH', 'EUR')

	def getTime(self):
		timestamp=self.krak.query_public('Time')['result']
		return datetime.fromtimestamp(int(timestamp['unixtime'])).strftime('%Y-%m-%d %H:%M:%S')

def main():
	k=KrakenPublic()
	print(k.getBitcoin())

if __name__ == '__main__':
	main()