PC_1 = [10, 6, 11, 7, 4, 12, 9, 3, 13, 16, 15, 14, 5, 8]
PC_2 = [11, 10, 14, 3, 12, 5, 8, 4, 6, 7, 9, 13]
IP = [13, 15, 6, 12, 10, 2, 5, 9, 11, 4, 3, 7, 1, 16, 14, 8]
IP_dash = [13, 6, 11, 10, 7, 3, 12, 16, 8, 5, 9, 4, 1, 15, 2, 14]
S_BOX = [[[2, 5, 4, 12, 0, 15, 9, 7, 6, 14, 1, 8, 11, 10, 13, 3], [2, 5, 4, 12, 0, 15, 9, 7, 6, 14, 1, 8, 11, 10, 13, 3], [2, 5, 4, 12, 0, 15, 9, 7, 6, 14, 1, 8, 11, 10, 13, 3], [2, 5, 4, 12, 0, 15, 9, 7, 6, 14, 1, 8, 11, 10, 13, 3]], [[6, 4, 14, 10, 13, 12, 3, 2, 5, 11, 0, 7, 1, 15, 9, 8], [6, 4, 14, 10, 13, 12, 3, 2, 5, 11, 0, 7, 1, 15, 9, 8], [6, 4, 14, 10, 13, 12, 3, 2, 5, 11, 0, 7, 1, 15, 9, 8], [6, 4, 14, 10, 13, 12, 3, 2, 5, 11, 0, 7, 1, 15, 9, 8]]]
P = [3, 6, 4, 2, 1, 5, 7, 8]
E = [8, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 1]

#Matrix that determine the shift for each round of keys
SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]


def char_to_binary(x,sz):
    return num_to_binary(ord(x),sz)

def num_to_binary(x,sz):
    res = bin(x)[2:]
    while len(res) < sz :
        res = '0' + res

    return res

def string_to_binary(s,sz):
    res = ""
    for i in s:
        res += char_to_binary(i,sz)
    arr = [int(i) for i in res]
    return arr

def bit_array_to_string(arr):
    #split into group of 8
    arr = split_array(arr,8)
    fin = ""
    for block in arr:
        block = [str(x) for x in block]
        block = ''.join(block)
        fin += chr(int(block,2))
    return fin

def permutation(arr,box):
    return [arr[i-1] for i in box]

def expand(arr,box):
    return [arr[i-1] for i in box]

def split_array(arr,x):
    return [arr[i:i+x] for i in range(0,len(arr),x)]

def left_shift(arr,x):
    return arr[x:] + arr[:x]

def xor(arr1,arr2):
    return [(arr1[i]^arr2[i]) for i in range(len(arr1))]

def substitution(arr):
    arr = split_array(arr,6)
    fin = []
    for i in range(len(arr)):
        row = int(str(arr[i][0])+str(arr[i][5]),2)
        col = int(''.join([str(i) for i in arr[i][1:5]]),2)

        s_ij = S_BOX[i][row][col]
        s_ij = num_to_binary(s_ij,4)

        s_ij = [int(i) for i in s_ij]

        fin.extend(s_ij)
    return fin

def generate_keys(key,no_of_keys,key_size):
    keys = []
    if(len(key) < key_size//8):
        return []
    key = key[:key_size//8]
    key_arr = string_to_binary(key,8)
    key = permutation(key_arr,PC_1)
    tmp = split_array(key,(key_size-key_size//8)//2)
    c0,d0 = tmp[0], tmp[1]
    for i in range(no_of_keys):
        c0,d0 = left_shift(c0,SHIFT[i]) , left_shift(d0,SHIFT[i])
        keys.append(permutation(c0+d0,PC_2))
    return keys

def DEA(text,keys,no_of_rounds,block_size):
    blocks = split_array(text,block_size//8)

    cryp = []
    for block in blocks:
        block = string_to_binary(block,8)

        #Apply Intial Permuatation
        block = permutation(block,IP)

        #Split the block in two halves
        L,R = split_array(block,block_size//2)

        for i in range(no_of_rounds):
            #Expand the right half to 48 bits
            R_dash = expand(R,E)

            #Take Xor of block bits with key
            R_dash = xor(keys[i],R_dash)

            #S-box
            R_dash = substitution(R_dash)

            R_dash = permutation(R_dash,P)
            

            R_dash = xor(R_dash,L)

            L = R
            R = R_dash
        tmp = R + L
        
        tmp = permutation(tmp,IP_dash)
        cryp.extend(tmp) 
    cryp = bit_array_to_string(cryp)
    return cryp

def encrypt(msg,secret_key,rounds,block_size):
    round_keys = generate_keys(secret_key,rounds,block_size)
    return DEA(msg,round_keys,rounds,block_size)

def decrypt(c,secret_key,rounds,block_size):
    round_keys = generate_keys(secret_key,rounds,block_size)
    round_keys.reverse()
    return DEA(c,round_keys,rounds,block_size)

msg = "Hello wo"
secret_key = "becret_k"


#-------------Set Rounds and Block Size-----------------#

rounds = 16
block_size = 16

#-------------------------------------------------------#

cypher = encrypt(msg,secret_key,rounds,block_size)

print("Encrypt : %r" %cypher)

m = decrypt(cypher,secret_key,rounds,block_size)
print("Decrypt :",m)