# NAME: Casey Olsen,Kenna Wang
# ID: 004938486,
# EMAIL: casey.olsen@gmail.com

import csv

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

with open('trivial.csv', newline='') as csvfile:
    info = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in info:
        row = row[0].split(',')
        if row[0] == "SUPERBLOCK":
            total_blocks = row[1]
            total_inodes = row[2]
            block_size = row[3]
            inode_size = row[4]
            blocks_per_group = row[5]
            first_non_reserved_inode = row[7]
        if row[0] not in input_dict.keys():
            input_dict[row[0]] = []
        if row[0] == "BFREE" or row[0] == "IFREE":
            input_dict[row[0]].append(','.join(row[1:]))
        else:
            input_dict[row[0]].append(row[1:])
        #print(row)
        #print(', '.join(row))
    print(input_dict)




def isLegalBlock(b):
    if b < 0 or b >= total_blocks: #or b < first_legal_block):
        return False
    else:
        return True

