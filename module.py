import os
from tkinter import*
# from tkinter import filedialog
from cryptography.fernet import Fernet as fer

class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''


codes = dict()

def Calculate_Codes(node, val=''):
    newVal = val + str(node.code)
    if(node.left):
        Calculate_Codes(node.left, newVal)
    if(node.right):
        Calculate_Codes(node.right, newVal)
    if(not node.left and not node.right):
        codes[node.symbol] = newVal
    return codes        

def Calculate_Probability(data):
    symbols = dict()
    for element in data:
        symbols[element] = symbols.get(element,0) + 1     
    return symbols

def get_byte_array(padded_encoded_text):
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b 

def Header_Extractor(file_data):
    temp,file_data=remove_bit(file_data,8)
    n=int(temp,2)
    temp,file_data=remove_bit(file_data,8)
    f1=int(temp,2)
    temp,file_data=remove_bit(file_data,8)
    f2=int(temp,2)
    symbol_with_prob={}
    for i in range(n):
        temp,file_data=remove_bit(file_data,f1)
        k=int(temp,2)
        k=chr(k)
        temp,file_data=remove_bit(file_data,f2)
        v=int(temp,2)
        symbol_with_prob[k]=v
    return symbol_with_prob,file_data

def Header_Generator(symbol_with_probs):
    m1=max(symbol_with_probs,key=lambda x:ord(x))
    m2=max(symbol_with_probs,key=lambda x:symbol_with_probs[x])
    f1=0
    o=ord(m1)
    if o<=127:
        f1=7
    elif o<=255:
        f1=8
    elif o<=1023:
        f1=10
    elif o<=2047:
        f1=11
    elif o<=4095:
        f1=12
    elif o<=8191:
        f1=13
    elif o<=16383:
        f1=14
    elif o<=32767:
        f1=15
    else:
        f1=16
    f2=0
    v=symbol_with_probs[m2]
    if v<=127:
        f2=7
    elif v<=255:
        f2=8
    elif v<=1023:
        f2=10
    elif v<=2047:
        f2=11
    elif v<=4095:
        f2=12
    elif v<=8191:
        f2=13
    elif v<=16383:
        f2=14
    elif v<=32767:
        f2=15
    else:
        f2=16
    header=bin(len(symbol_with_probs))[2:]
    header=header.rjust(8,'0')
    k1=bin(f1)[2:]
    header+=k1.rjust(8,'0')
    k2=bin(f2)[2:]
    header+=k2.rjust(8,'0')
    for i,j in zip(symbol_with_probs.keys(),symbol_with_probs.values()):
        k=bin(ord(i))[2:]
        header+=k.rjust(f1,'0')
        l=bin(j)[2:]
        header+=l.rjust(f2,'0')
    return header

def Huffman_Decoding(file_path):
    file_data=''
    file=open(file_path,'rb')
    byte=file.read(1)
    while(len(byte)>0):
        byte=ord(byte)
        bits=bin(byte)[2:].rjust(8,'0')
        file_data+=bits
        byte=file.read(1)
    file_data=remove_padding(file_data)
    symbol_with_probs,encoded_data=Header_Extractor(file_data)
    file.close()
    symbols = symbol_with_probs.keys()
    nodes = []
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.prob)
        right = nodes[0]
        left = nodes[1]
        left.code = 0
        right.code = 1
        newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
    huffman_tree=nodes[0]
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right   
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol == None and huffman_tree.right.symbol == None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head
    string = ''.join([str(item) for item in decoded_output])
    file_name,extension=os.path.splitext(file_path)
    out_file_path=file_name+'_decompressed'+'.txt'
    final=open(out_file_path,'w')
    final.write(string)
    final.flush()
    final.close()

def Huffman_Encoding(file_path):
    file=open(file_path,'r')
    data=file.read()
    size=len(data)
    file.close()
    filename, file_extension = os.path.splitext(file_path)
    output_path = filename + '.bin'
    out_file=open(output_path,'wb')
    symbol_with_probs = Calculate_Probability(data)
    symbols = symbol_with_probs.keys()
    header=Header_Generator(symbol_with_probs)
    encoded_output=header
    nodes = []
    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))
    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.prob)
        right = nodes[0]
        left = nodes[1]
        left.code = 0
        right.code = 1
        newNode = Node(left.prob+right.prob, left.symbol+right.symbol, left, right)
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)
    huffman_encoding = Calculate_Codes(nodes[0])
    encoded_output += Output_Encoded(data,huffman_encoding)
    paded_encoded_output=pad_encoded_text(encoded_output)
    b=get_byte_array(paded_encoded_output)
    out_file.write(bytes(b))
    out_file.flush()
    out_file.close()
    new_file=open(output_path,'rb')
    lines=new_file.readline()

def Output_Encoded(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])
    string = ''.join([str(item) for item in encoding_output])    
    return string

def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"
    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text

def remove_bit(string,size):
    temp=string[:size]
    string=string[size:]
    return temp,string

def remove_padding(file_data):
    padded_info=file_data[:8]
    extra_padding=int(padded_info,2)
    file_data=file_data[8:]
    encoded_data=file_data[:-1*extra_padding]
    return encoded_data         

def compression(filepath):
    Huffman_Encoding(filepath)

def decompression(filepath):
    Huffman_Decoding(filepath)


#########################################################################################################


def encyption(filepath):
    file=open(filepath,'r')
    data=file.read()
    file.flush()
    file.close()
    k=fer.generate_key()
    f=fer(k)
    data=data.encode()
    encoded_text_byte=f.encrypt(data)
    encoded_text=encoded_text_byte.decode()
    path,extension=os.path.splitext(filepath)
    out_path=path+'_encrypted'+extension
    file=open(out_path,'w')
    file.write(encoded_text)
    file.flush()
    file.close()
    key_path=path+'_key'+extension
    k=k.decode()
    file=open(key_path,'w')
    file.write(k)
    file.flush()
    file.close()

def decrption(filepath,k):
    file=open(filepath,'r')
    data=file.read()
    file.flush()
    file.close()
    data=data.encode()
    k=k.encode()
    path,extension=os.path.splitext(filepath)
    if '_encrypted' in path:
        path=path.replace('_encrypted','')
    outpath=path+'_decrypted'+extension
    f=fer(k)
    decoded_data_bytes=f.decrypt(data)
    decoded_data=decoded_data_bytes.decode()
    file=open(outpath,'w')
    file.write(decoded_data)
    file.flush()
    file.close()