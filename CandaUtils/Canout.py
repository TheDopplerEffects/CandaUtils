
import matplotlib.pyplot as mpl # pylint3: disable=import-error
import traceback as tb
import sys

data = {}

def listextend(ls, fksn, par):
	return [fksn(i, par) for i in ls]
def QSNestedList(ls, sortIndex):
	hi = []
	lo = []
	
	if len(ls) > 0:
		p = ls[0]
		
		for i in ls[1:]:
			if i[sortIndex] > p[sortIndex]:
				hi.append(i)
			else:
				lo.append(i)

		return QSNestedList(hi, sortIndex) + [p] + QSNestedList(lo, sortIndex)
	return []								
def sortFrameTrees(tree):
	lsframe = [value for key, value in tree.items()]
	
	return QSNestedList(lsframe, 0)
class Frame():
	def __init__(self, bus = None, ID = None, data = None, length = None):
		'''
		
		'''
		self.messageID = ID 
		self.message = data
		self.busNum = bus
		self.messageLength = length
		
	def getMessageByte(self):
		'''
		returns a list with 2 bites in every element
		'''
		return [hex(self.message>>i*8 & 0xff) for i in range(self.messageLength)]	
	def getBins(self):
		return [bin(self.message>>i*8 & 0xff)[2:].rjust(8,'0') for i in range(self.messageLength)][::-1]
		
	
	def _print(self):	
		pass
def formatBits(num, fmt):
	'''
	Formating:
	start : size : options...
	
	no returns normal number
	b:binary
	x:hex
	-:reverse
	
	ex:
		num = 0b01101 or 13 or 0xd
		
		fmt = '0:4:-' returns 0b1011 or 11 or 0xb
		fmt = '2:3:b-' returns 0b110 or 6 or 0x6
	'''
	
	start,size,*mod = fmt.split(':')
	if fmt == '':
		return num	
	return num>>int(start) & int(''.rjust(int(size), '1'),2)	
def sortCan(f = 'output.csv'):
	activeRank = []
	with open(f, 'r') as f:
		f.readline()
		try:
			while True:
				line = listextend(f.readline().strip().split(','), int, 16)
				
				try:
					data[line[1]][1].append(Frame(line[0], line[1], line[2], line[3]))
					data[line[1]][0] += 1
					
				except:
					data[line[1]] = [1, [Frame(line[0], line[1], line[2], line[3])]]

		except:
			pass


if __name__ == "__main__":
	sortCan()
	
	print(len(data))

	freqent = sortFrameTrees(data)

	print("[Done]\n")
	
	print("""Commands:
   - (number) : display IDs matching that number
   - all : display all IDs
   - top (number) : display the top (number) most requent IDs
   - sift : sift threw by frequency
   - graph : graphs all values from the IDs indicated includes formatting
   - val : desplay specific values of a ID
   - q : quit\n""")
	
	
	while True:
		
		
		inp = input("> ").rjust(1, 'x').split()
		tags = ''
		outFormat ='016x'
		IDFormat = '04x'
		
		
		if '-c' in inp:
			tags += 'c'
			inp.remove('-c')
		if '-b' in inp:
			tags += 'b'
			outFormat ='064b'
			inp.remove('-b')
		if '-i' in inp:
			tags += 'i'
			outFormat =''
			inp.remove('-i')
		
		if inp[0] == 'top': #Top command
			for i in freqent[int(inp[1])::-1]:
				for l in i[1]:
					print(('\t- 0x{:' + outFormat + '} {}bytes').format(l.message, l.messageLength))
				print('\n{}x{}'.format(hex(i[1][0].messageID), i[0]))
					
		elif inp[0] == 'sift': #Sift command
			for i in freqent[::-1]:
				for l in i[1][::-1]:
					print(('\t- 0x{:' + outFormat + '} {}bytes').format(l.message, l.messageLength))
				print(('0x{:' + IDFormat + '} ({})\n').format(i[1][0].messageID, i[0]))
				try:
					input('(enter for the next ID, Ctrl-c to stop)')
				except KeyboardInterrupt:
					break
					
		elif inp[0] == 'all': #All command
			for key, i in data.items():
				for l in i[1]:
					print(('\t- 0x{:' + outFormat + '} {}bytes').format(l.message, l.messageLength))
				print(('0x{:' + IDFormat + '} ({})\n').format(i[1][0].messageID, i[0]))
				
		
		elif inp[0] == 'graph': #Graph command
			missing = ''
			try:
				if 1:
					for i in inp[1:]:
						MID, *fmt = i.split('|')
						
						for o in fmt:
							vals = [formatBits(l.message, o) for l in data[int(MID,16)][1]]
							
							mpl.title( ('0x{:' + IDFormat + '} ({})').format(int(MID, 16), o) )
							mpl.plot(vals)
							if 'c' not in tags:
								mpl.show()
								
						if len(fmt) == 0:
							vals = [l.message for l in data[int(MID,16)][1]]
							
							mpl.title(('0x{:' + IDFormat + '}').format(int(MID, 16)))
							mpl.plot(vals)
							if 'c' not in tags:
								mpl.show()	
						if 'c' in tags:
							mpl.show()
						
			except KeyError:
				missing += ', ' + i 
			except:					
				print("there was a problem with you request:")
			if missing != '':
				print('missing IDs:', missing[2:])
			
		elif inp[0] == 'val': #Val command
			missing = ''
			try:
				for i in inp[2:]:
					mess, *fmt = i.split('|')
					
					for o in fmt:
						vals = formatBits(data[int(inp[1],16)][1][int(mess)].message, o)
						
						print(('0x{} #{} {:' + outFormat + '} ').format(inp[1], mess, vals))
						
			except KeyError:
				missing += ', ' + i
			except:
				print("there was a problem with you request:")
			if missing != '':
				print('missing IDs:', missing[2:])
				
		elif inp[0].lower() in ['q','quit', 'exit']:
			break
		else:
			missing = ''
			for i in inp:
				try:
					for l in data[int(i,16)][1]:
						print(('\t- 0x{:' + outFormat + '} {}bytes').format(l.message, l.messageLength))
					print('\t4   ' + '|   ' * 16)
					print('\t8   ' + '|       ' * 8)
					print('\t16  ' + '|               ' * 4)
					print(('0x{:' + IDFormat + '} ({})\n').format(int(i,16), data[int(i,16)][0])) #----------------------
				except KeyError:
					missing += ', ' + i
				except:
					print("there was a problem with you request")
					break
				if missing != '':
					print('missing IDs:', missing[2:])
					
		
				
			
				

