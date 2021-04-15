import random

#Cryptographer Dhruv > > Cryptographer Bharat
def random_shuffle(iter,arr):
	sz = len(arr)
	for i in range(iter):
		x = random.randint(0,sz)%sz
		y = random.randint(0,sz)%sz
		arr[x],arr[y] = arr[y],arr[x]
	return arr

def create_array(n):
	return random_shuffle(50,[i+1 for i in range(n)])

def create_permutation(arr,dont_take):
	for i in dont_take:
		arr.remove(i)
	return arr

def inverse_permutation(arr):
	tmp = [0]*len(arr)
	for i in range(len(arr)):
		tmp[arr[i]-1] = i+1
	return tmp



#------------Block Size-------------#

block_size = 16

#-----------------------------------#

ignored = block_size//8

#Permuted Choice for the key
PC_1 = create_permutation(create_array(block_size),create_array(ignored))	
print("PC_1 =",PC_1)

PC_2 = create_permutation(create_array(block_size-ignored),create_array(ignored))	
print("PC_2 =",PC_2)



#Intial Permutation and Inverse Permuation
IP = create_permutation(create_array(block_size),[])
print("IP =",IP)

IP_dash = inverse_permutation(IP)
print("IP_dash =",IP_dash)



#S-boxes
S_BOX = []
for i in range(block_size//8):
	tmp = [x for x in range(16)]
	s_tmp = []
	for j in range(4):
		s_tmp.append(random_shuffle(50,tmp))
	S_BOX.append(s_tmp)
print("S_BOX =",S_BOX)



#P-Box which shuflles the 32bit block
P = create_permutation(create_array(block_size//2),[])
print("P =",P)



#Expansion Box
E_tmp = [i+1 for i in range(block_size//2)]
E = []
for i in range(0,len(E_tmp),4):
	E.append(E_tmp[i-1])
	for j in range(i,i+4,1):
		E.append(E_tmp[j])
	E.append(E_tmp[(i+4)%len(E_tmp)])
print("E =",E)

