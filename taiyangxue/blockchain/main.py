import hashlib as hasher
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode("utf-8"))
        return sha.hexdigest()

def create_genesis_block():
    # 手工创建第一个区块，其索引为 0，且随意取给紧前特征值 '0'
    return Block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)

# 创建一个区块链，并将第一个区块加入
blockchain = [create_genesis_block()]

# 设置产生区块的个数
num_of_blocks_to_add = 20

# 产生区块并加入区块链
for i in range(0, num_of_blocks_to_add):
    previous_block = blockchain[-1]
    block_to_add = next_block(previous_block)
    blockchain.append(block_to_add)
    # 发布当前区块的信息
    print("Block #{} has been added to the blockchain!".format(block_to_add.index))
    print("Hash: {}\n".format(block_to_add.hash))