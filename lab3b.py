# NAME: Casey Olsen,Kenna Wang
# ID: 004938486,604939143
# EMAIL: casey.olsen@gmail.com,kenna.wang6@gmail.com

import csv
import sys

total_blocks = 0
total_inodes = 0
block_bitmap = []
inode_bitmap = []
block_size = 0
inode_size = 0
blocks_per_group = 0
first_non_reserved_inode = 0

input_dict = {}

# GLOBAL CONSTANTS

# INODE SUMMARY
I_INODE_NUMBER = 0
I_FILE_TYPE = 1
I_MODE = 2
I_OWNER = 3
I_GROUP = 4
I_LINK_COUNT = 5
I_LAST_CHANGE = 6
I_MOD_TIME = 7
I_ACCESS_TIME = 8
I_FILE_SIZE = 9 

# DIRECTORY ENTRIES
D_PARENT_INODE = 0
D_OFFSET = 1
D_INODE_NUM = 2
D_ENTRY_LEN = 3
D_NAME_LEN = 4
D_NAME = 5

# INDIRECT BLOCK
ID_INODE_NUM = 0
ID_INDIR_LEVEL = 1
ID_OFFSET = 2
ID_BLOCK_NUM_INDIR = 3
ID_BLOCK_NUM_DIR = 4



def main():
    if (len(sys.argv) != 2):
        print("ERROR: Too many arguements\n")
        exit(1)

    filename = sys.argv[1]
    print ("filename: " + filename)

    initialize(filename)
    get_block_bitmap()
    get_inode_bitmap()
    check_links()
    
    # got help from:
# https://docs.python.org/3/library/csv.html#module-contents

def initialize(filename):
    # got help from:
    # https://docs.python.org/3/library/csv.html#module-contents
    try:
        with open(filename, newline='') as csvfile:
            info = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in info:
                row = row[0].split(',')
                if row[0] == "SUPERBLOCK":
                    global total_blocks
                    total_blocks = int(row[1])
                    global total_inodes
                    total_inodes = int(row[2])
                    global block_size
                    block_size = int(row[3])
                    global inode_size
                    inode_size = int(row[4])
                    global blocks_per_group
                    blocks_per_group = int(row[5])
                    global first_non_reserved_inode
                    first_non_reserved_inode = int(row[7])
                if row[0] not in input_dict.keys():
                    input_dict[row[0]] = []
                if row[0] == "BFREE" or row[0] == "IFREE":
                    input_dict[row[0]].append(','.join(row[1:]))
                else:
                    input_dict[row[0]].append(row[1:])
                #print(row)
                #print(', '.join(row))
            print(input_dict)
    except EnvironmentError:
        print ("ERROR opening file\n")
        exit(1)

def IsFreeBlocks(b):
    if IsLegalBlock(b) == False:
        return False
    else:
        return block_bitmap[b]

def IsFreeInode(i):
    if ( i > 2 and i < reserved_inodes) or i < total_inodes:
        return False
    else:
        return inode_bitmap[i]

def isLegalBlock(b):
    if b < 0 or b >= total_blocks: #or b < first_legal_block):
        return False
    else:
        return True


def get_block_bitmap():
    last_block = int(input_dict["BFREE"][-1])
    print(last_block)
    print(total_blocks)
    for i in range(0, total_blocks):
        if str(i) in input_dict["BFREE"]:
            block_bitmap.append(0)
            print(i)
        else:
            block_bitmap.append(1)
    print(block_bitmap)

def get_inode_bitmap():
    for i in range(0, total_inodes):
        if str(i) in input_dict["IFREE"]:
            inode_bitmap.append(0)
            print(i)
        else:
            inode_bitmap.append(1)
    print(inode_bitmap)

def check_links():
    link_count = [0] * total_inodes
    for i in range(0, len(input_dict["DIRENT"])):
        link_count[int(input_dict["DIRENT"][i][D_INODE_NUM])] += 1
        #print (isValidInode(int(input_dict["DIRENT"][i][D_INODE_NUM])))
        if (not isValidInode(int(input_dict["DIRENT"][i][D_INODE_NUM]))):
            print("DIRECTORY INODE " + input_dict["DIRENT"][i][D_INODE_NUM] + " NAME " + input_dict["DIRENT"][i][D_NAME] + " FIX THIS NOT DONE ")
    #print(link_count)
    for i in range(0, len(input_dict["INODE"])):
        if int(input_dict["INODE"][i][I_LINK_COUNT]) != link_count[int(input_dict["INODE"][i][I_INODE_NUMBER])]:
            print("INODE " + str(input_dict["INODE"][i][I_INODE_NUMBER]) + " HAS " + str(link_count[int(input_dict["INODE"][i][I_INODE_NUMBER])]) + " LINKS BUT LINKCOUNT IS " + str(input_dict["INODE"][i][I_LINK_COUNT]))
    #for i in range(0, total_inodes):
    #    link_count.append(0)

def isValidInode(inode):
    if inode < 1 or inode > total_inodes or inode_bitmap == 0:
        return False
    else:
        return True
    
main()
