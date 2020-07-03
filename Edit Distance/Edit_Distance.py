# author @ Shreyash Arya 2015097
# References mentioned with line; 
# majorly referenced "Speech and Language Processing by D. Jurafsky and J.H. Martin - Chapter 3 Minimum Edit Distance pg. 76 Algo; edition 2"
import sys

# -------------------------------Printing Matrices Function-----------------------------------------------------------

def print_mat(distance):
	for i in range(len(distance)):
		print ""
		for j in range(len(distance[i])):
			sys.stdout.write(str(distance[i][j])+"  ")
			sys.stdout.flush() # https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
	print ""

# ---------------------------------Minimum Edit Distance Function------------------------------------------------------

def min_edit_distance(target,source):
	
	n = len(target)
	m = len(source)
	
	distance = [ [0 for x in range(n+1)] for y in range(m+1) ] #list comprehension: https://stackoverflow.com/questions/6667201/how-to-define-a-two-dimensional-array-in-python
	distance[0][0] = 0

	ptr = [ [-1 for x in range(n+1)] for y in range(m+1) ]
	ptr[0][0] = -2

	for i in range(1,m+1):
		# print_mat(distance)
		distance[i][0] = distance[i-1][0]+1 # for each row, 1st column
	
	
	for j in range(1,n+1): # for each column
		# print_mat(distance)
		distance[0][j] = distance[0][j-1]+1 # 1st row, for all columns

	for j in range(1,n+1):
		print_mat(distance)
		for i in range(1,m+1):
			if target[j-1]==source[i-1]:
				distance[i][j] = min(distance[i-1][j-1],distance[i-1][j]+1,distance[i][j-1]+1)
				ptr[i][j] = 0
			else:
				distance[i][j] = min(distance[i-1][j-1]+2,distance[i-1][j]+1,distance[i][j-1]+1)
				subs = distance[i-1][j-1]+2
				delt = distance[i-1][j]+1
				insrt = distance[i][j-1]+1
				if subs<=delt and subs<=insrt:
					ptr[i][j] = 2
				elif delt<subs and delt<=insrt:
					ptr[i][j] = 3
				else:
					ptr[i][j] = 1

	print_mat(distance)
	print ""
	print distance[m][n]
	return distance,ptr

# --------------------------------------main driver program-------------------------------------------

# taking target and source string as user input

target = raw_input("Target: ")
source = raw_input("Source: ")

distance,ptr = min_edit_distance(target,source) # calculating cost and pointer matrix

print ""
print "Backtrack Pointer Matrix"
print_mat(ptr)

# -----------------------------------------Backtracking Algo-------------------------------------------

n = len(target)
m = len(source)

tar = []
src = []
act = []
cost = 0
count=101
while(m!=0 and n!=0):
	# if target[n-1] == source[m-1]:
	# 	m = m-1
	# 	n = n-1
	# print count
	# print""
	if (m-1!=0) and (n-1!=0):
		# print "1"
		if ptr[m][n] == 0:
			tar.append(target[n-1])
			src.append(source[m-1])
			act.append(str(' '))
			m=m-1
			n=n-1
			# print "2"
		elif ptr[m][n] == 2:
			tar.append(target[n-1])
			src.append(source[m-1])
			act.append('s')
			m = m-1
			n = n-1
			cost+=2
			# print "3"
		elif ptr[m][n] == 3:
			tar.append(str('*'))
			src.append(source[m-1])
			act.append('d')
			m = m-1
			cost+=1
			# print "4"
		else:
			tar.append(target[n-1])
			src.append(str('*'))
			act.append('i')
			n=n-1
			cost+=1
			# print "5"
	elif m-1==0 and n-1!=0:
		tar.append(target[n-1])
		src.append(str('*'))
		act.append('i')
		n = n-1
		cost+=1
		# print "6"
	elif n-1==0 and m-1!=0:
		tar.append(str('*'))
		src.append(source[m-1])
		act.append('d')
		m = m-1
		cost+=1
		# print "7"
	else:
		if ptr[m][n]==2:
			tar.append(target[n-1])
			src.append(source[m-1])
			act.append('s')
			cost+=2
			# print "8"
		else:
			# cost+=1
			tar.append(target[n-1])
			src.append(source[m-1])
			act.append(str(' '))
			# print "9"
		m=m-1
		n=n-1
	count+=1

# ------------------------------Cost---------------------------------------------

print ""
print "Cost:"+str(cost)
print ""

# --------------------------String Alignment-------------------------------------

for i in reversed(src):
	sys.stdout.write(i+" ")
	sys.stdout.flush()
print ""

for i in reversed(tar):
	sys.stdout.write(i+" ")
	sys.stdout.flush()
print ""

for i in reversed(act):
	sys.stdout.write(i+" ")
	sys.stdout.flush()
print ""

# ----------------------------------------XX--END--XX----------------------------------------------------------