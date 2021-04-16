
des_mod = __import__('DES-Modified')

def getDataPoints(msg,msg2,rounds,block_size,seed,mask):
	print("--------------------------------")
	des_o = des_mod.DES_M(block_size,rounds,secret_key,seed,0&mask)
	cypher , cypher_dash = des_o.encrypt(msg)


	print("Encrypt : %r" %cypher)

	m , _ = des_o.decrypt(cypher)
	print("Decrypt :",m)

	des_o2 = des_mod.DES_M(block_size,rounds,secret_key,seed,1&mask)
	cypher2 , cypher_dash2 = des_o2.encrypt(msg2)
	print("Encrypt2 : %r" %cypher2)

	# #For Graph
	x_points = [(i+1) for i in range(rounds)]
	y_points = []
	for i in range(rounds):
	    y_points.append(sum(des_o2.xor(cypher_dash[i],cypher_dash2[i])))
	print("--------------------------------")
	print("-")
	return x_points,y_points


blocks = [16,32,64]

x_points = []
y_points = []

block_size = 64
rounds = 16
secret_key = "secret_k"
seed = 7
msg = "hello wo"

#Change in Key
for i in blocks:
	x,y = getDataPoints(msg,msg,rounds,i,seed,1)
	x_points.append(x)
	y_points.append(y)
#Change in plaintext
msg2 = "eello wo"
for i in blocks:
	x,y = getDataPoints(msg,msg2,rounds,i,seed,0)
	x_points.append(x)
	y_points.append(y)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 10))
for i in range(len(blocks)):
	plt.plot(x_points[i],y_points[i],label = "Change in Key with Block-Size : "+str(blocks[i]))

for i in range(len(blocks)):
	plt.plot(x_points[3+i],y_points[3+i],label = "Change in Plaintext with Block-Size : "+str(blocks[i]),linestyle ="dashed")

plt.xlabel("No. of Rounds")
plt.ylabel("Difference in Bits")
plt.title("DEA Avalanche Effect")

plt.legend()

plt.show()