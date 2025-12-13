import hashlib

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def hash_pair(left: bytes, right: bytes) -> bytes:
    return sha256(left + right)

def build_merkle_tree(leaves: list[bytes]) -> list[list[bytes]]:
    """
    Returns all levels of the tree.
    levels[0] = leaf hashes
    levels[-1][0] = merkle root
    """
    if not leaves:
        return []

    levels: list[list[bytes]] = []
    current_level = leaves[:]
    levels.append(current_level[:])    # store copy

    while len(current_level) > 1:
        if len(current_level) % 2 == 1:
            current_level.append(current_level[-1])

        next_level = []
        for i in range(0, len(current_level), 2):
            parent = hash_pair(current_level[i], current_level[i + 1])
            next_level.append(parent)

        levels.append(next_level[:])   # store copy
        current_level = next_level

    return levels

def main():
    # Our leaves: [1, 2, 3, 4, 5, 6]
    values = [1, 2, 3, 4, 5, 6]

    # Encode & hash each leaf. Here we hash the string "1", "2", ...
    leaves = [sha256(str(v).encode()) for v in values]

    # Build Merkle tree
    levels = build_merkle_tree(leaves)

    # Print levels
    for level_idx, level in enumerate(levels):
        if level_idx == 0:
            print(f"leave nodes:")
        else:
            print(f"Level 0x{level_idx}:")
        for node_idx, node in enumerate(level):
            print(f"  Node {node_idx}: 0x{node.hex()}")
        print()

    # Merkle root
    root = levels[-1][0]
    print(f"Merkle Root: 0x{root.hex()}")

if __name__ == "__main__":
    main()