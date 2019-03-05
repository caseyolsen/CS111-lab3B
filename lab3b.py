#!/usr/local/bin/python3
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
block_bitmap_block = 0
inode_bitmap_block = 0
inode_block = 0
input_dict = {}

# GLOBAL CONSTANTS
EXT2_ROOT_INO = 2

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
I_NUM_BLOCKS = 10
I_BLOCKS = 11

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
    #print ("filename: " + filename)

    initialize(filename)
    get_block_bitmap()
    get_inode_bitmap()
    check_links()
    check_inodes()
    check_indirect_blocks()
    find_unreferenced_blocks()

    # got help from:
# https://docs.python.org/3/library/csv.html#module-contents



def initialize(filename):
    # got help from:
    # https://docs.python.org/3/library/csv.html#module-contents
    try:
        with open(filename, newline='') as csvfile:
            info = csv.reader(csvfile, delimiter='\n', quotechar='|')
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
                if row[0] == "GROUP":
                    global block_bitmap_block
                    block_bitmap_block = int(row[6])
                    global inode_bitmap_block
                    inode_bitmap_block = int(row[7])
                    global inode_block
                    inode_block = int(row[8])

                if row[0] not in input_dict.keys():
                    input_dict[row[0]] = []
                if row[0] == "BFREE" or row[0] == "IFREE":
                    input_dict[row[0]].append(','.join(row[1:]))
                else:
                    input_dict[row[0]].append(row[1:])
                #print(row)
                #print(', '.join(row))
            #print(input_dict)
    except EnvironmentError:
        print ("ERROR opening file\n")
        exit(1)

def get_block_bitmap():
    last_block = int(input_dict["BFREE"][-1])
    #print(last_block)
    #print(total_blocks)
    for i in range(0, total_blocks):
        if str(i) in input_dict["BFREE"]:
            block_bitmap.append(0)
            #print(i)
        else:
            block_bitmap.append(1)
    #print(block_bitmap)

def get_inode_bitmap():
    for i in range(0, total_inodes):
        if str(i) in input_dict["IFREE"]:
            inode_bitmap.append(0)
            #print(i)
        else:
            inode_bitmap.append(1)
    #print(inode_bitmap)

def check_links():
    link_count = [0] * total_inodes

    # NEW WAY OF DOING IT
    inode_parent = [0] * total_inodes

    for i in range(0, len(input_dict["DIRENT"])):
        #print ("TOTAL: " + str(total_inodes) + ", ind: " + (input_dict["DIRENT"][i][D_INODE_NUM]))
        #link_count[int(input_dict["DIRENT"][i][D_INODE_NUM])] += 1
        #print (isValidInode(int(input_dict["DIRENT"][i][D_INODE_NUM])))
        #print("INODE NUM: " + input_dict["DIRENT"][i][D_INODE_NUM] + " NAME: " + input_dict["DIRENT"][i][D_NAME])
        #if (input_dict["DIRENT"][i][-1] != "\'.\'" and input_dict["DIRENT"][i][-1] != "\'..\'"):
        #    inode_parent[int(input_dict["DIRENT"][i][D_INODE_NUM])] = int(input_dict["DIRENT"][i][D_PARENT_INODE])

        if (isValidInode(int(input_dict["DIRENT"][i][D_INODE_NUM])) != ""):
            print("DIRECTORY INODE " + input_dict["DIRENT"][i][D_PARENT_INODE] + " NAME " + input_dict["DIRENT"][i][D_NAME] + " " + isValidInode(int(input_dict["DIRENT"][i][D_INODE_NUM])) + " INODE " + input_dict["DIRENT"][i][D_INODE_NUM])
        else:
            link_count[int(input_dict["DIRENT"][i][D_INODE_NUM])] += 1
            if (input_dict["DIRENT"][i][-1] != "\'.\'" and input_dict["DIRENT"][i][-1] != "\'..\'" and points_to_directory(input_dict["DIRENT"][i][D_INODE_NUM])):
                inode_parent[int(input_dict["DIRENT"][i][D_INODE_NUM])] = int(input_dict["DIRENT"][i][D_PARENT_INODE])
            #else:
            #    print("HERE: " + input_dict["DIRENT"][i][-1])
            #print(link_count)
    for i in range(0, len(input_dict["INODE"])):
        if int(input_dict["INODE"][i][I_LINK_COUNT]) != link_count[int(input_dict["INODE"][i][I_INODE_NUMBER])]:
            print("INODE " + str(input_dict["INODE"][i][I_INODE_NUMBER]) + " HAS " + str(link_count[int(input_dict["INODE"][i][I_INODE_NUMBER])]) + " LINKS BUT LINKCOUNT IS " + str(input_dict["INODE"][i][I_LINK_COUNT]))

    inode_parent[EXT2_ROOT_INO] = EXT2_ROOT_INO
    for i in range(0, len(input_dict["DIRENT"])):
        if input_dict["DIRENT"][i][-1] == "\'..\'":
            #print ("inode_parent: " + str(inode_parent[int(input_dict["DIRENT"][i][D_INODE_NUM])]))
            #print (input_dict["DIRENT"][i][D_INODE_NUM])
            if inode_parent[int(input_dict["DIRENT"][i][D_INODE_NUM])] == 0:
                continue
            if inode_parent[int(input_dict["DIRENT"][i][D_INODE_NUM])] != int(input_dict["DIRENT"][i][D_INODE_NUM]): # and int(input_dict["DIRENT"][i][2]) != 2:
                print("DIRECTORY INODE " + input_dict["DIRENT"][i][0] + " NAME '..' LINK TO INODE " + input_dict["DIRENT"][i][2] + " SHOULD BE " + str(inode_parent[int(input_dict["DIRENT"][i][D_INODE_NUM])])) 
                
    #print(inode_parent)
'''
    if "'.'" not in input_dict["DIRENT"]:
        print (". is not in DIRECNT")
    if "'..'" not in input_dict["DIRENT"]:
        print (".. not in DIRECNT")
   '''         #for i in range(0, total_inodes):
    #    link_count.append(0)

def points_to_directory(num):
OH     for i in range(0, len(input_dict["INODE"])):
        if input_dict["INODE"][i][I_INODE_NUMBER] == num:
            if input_dict["INODE"][i][I_FILE_TYPE] == 'd':
                return True
    return False
    
def isValidInode(inode):
    if inode < 1 or inode > total_inodes:
        return "INVALID"
    #print (inode_bitmap)
    #print(inode_bitmap[inode])
    if inode_bitmap[inode] == 0:
        return "UNALLOCATED"
    else:
        return ""

def check_inodes():
    for i in range(0, len(input_dict["INODE"])):
        if inode_bitmap[int(input_dict["INODE"][i][I_INODE_NUMBER])] == 0: 
            print("ALLOCATED INODE {} ON FREELIST"
                  .format(input_dict["INODE"][i][I_INODE_NUMBER]))
        inode_bitmap[int(input_dict["INODE"][i][I_INODE_NUMBER])] = 2
        for j in range(0, 12):
            check_block(int(input_dict["INODE"][i][I_BLOCKS + j]), 
                        j, 0, input_dict["INODE"][i][I_INODE_NUMBER])
        check_block(int(input_dict["INODE"][i][I_BLOCKS + 12]), 
                    12, 1, input_dict["INODE"][i][I_INODE_NUMBER])
        check_block(int(input_dict["INODE"][i][I_BLOCKS + 13]), 
                    268, 2, input_dict["INODE"][i][I_INODE_NUMBER])
        check_block(int(input_dict["INODE"][i][I_BLOCKS + 14]), 
                    65804, 3, input_dict["INODE"][i][I_INODE_NUMBER])
    for i in range(first_non_reserved_inode, len(inode_bitmap)):
        if inode_bitmap[i] == 1:
            print("UNALLOCATED INODE {} NOT ON FREELIST".format(i))
            return
    return

def check_block(b, offset, level, inode):
    if b == 0:
        return
    if level == 0:
        block_type = ""
    elif level == 1:
        block_type = "INDIRECT "
    elif level == 2:
        block_type = "DOUBLE INDIRECT "
    else:
        block_type = "TRIPLE INDIRECT "
    if b < 0 or b >= total_blocks:
        print("INVALID {}BLOCK {} IN INODE {} AT OFFSET {}"
              .format(block_type, b, inode, offset))
        return
    if is_reserved_block(b):
        print("RESERVED {}BLOCK {} IN INODE {} AT OFFSET {}"
              .format(block_type, b, inode, offset))
        return
    if block_bitmap[b] == 0:
        print("ALLOCATED BLOCK {} ON FREELIST".format(b))
        return
    if block_bitmap[b] != 1:
        print("DUPLICATE {}BLOCK {} IN INODE {} AT OFFSET {}"
              .format(block_type, b, inode, offset))
        if block_bitmap[b] != -1:
            print("DUPLICATE {}BLOCK {} IN INODE {} AT OFFSET {}"\
                      .format(block_bitmap[b][0], \
                              block_bitmap[b][1], \
                              block_bitmap[b][2], \
                              block_bitmap[b][3]))
        block_bitmap[b] = -1
        return
    block_bitmap[b] = [block_type, b, inode, offset]

def check_indirect_blocks():
    for i in range(0, len(input_dict["INDIRECT"])):
        check_block(int(input_dict["INDIRECT"][i][ID_BLOCK_NUM_DIR]), \
                        input_dict["INDIRECT"][i][ID_OFFSET], \
                        input_dict["INDIRECT"][i][ID_INDIR_LEVEL], \
                        input_dict["INDIRECT"][i][ID_INODE_NUM])
    return

def find_unreferenced_blocks():
    for i in range(8, len(block_bitmap)):
        if not is_reserved_block(i) and block_bitmap[i] == 1:
            print("UNREFERENCED BLOCK {}".format(i))
    return

def is_reserved_block(b):
    if b <= 1024/block_size or b <= 1024/block_size + 1 or \
    b == block_bitmap_block or b == inode_bitmap_block or b == inode_block:
        return True
    return False

main()
