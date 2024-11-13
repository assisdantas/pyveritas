def IsChainValid(chain):
    for i in range(1, len(chain)):
        current_block = chain[i]
        previous_block = chain[i - 1]
        if current_block.previous_hash != previous_block.hash:
            return False
        if not current_block.hash.startswith('0' * current_block.difficulty):
            return False
    return True
