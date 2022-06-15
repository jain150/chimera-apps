f = open('matrixdb.csv', 'r')
allLines = f.readlines()

f_ = open('matrixdb__.csv', 'w')

for line in allLines:
	
	tokens = line.split(",", 1)
	f_.write(tokens[0].strip() + "\n")

f.close
f_.close

