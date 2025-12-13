# aggregate.py
import hashlib
from typing import List, Tuple


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def build_merkle_root(leaves: List[bytes]) -> bytes:
    """
    Given signed transactions, build a Merkle tree and return its root.
    """
    _, root = build_merkle_tree(leaves)
    return root


def build_merkle_tree(leaves: List[bytes]) -> Tuple[List[List[bytes]], bytes]:
    """
    Returns (levels, root):
      - levels[0] = leaf hashes
      - levels[-1][0] = root
    """
    if len(leaves) != 10:
        raise ValueError(f"Expected 10 leaves, got {len(leaves)}")

    level = [sha256(x) for x in leaves]
    levels: List[List[bytes]] = [level]

    while len(level) > 1:
        next_level: List[bytes] = []
        # duplicate last if odd
        if len(level) % 2 == 1:
            level = level + [level[-1]]

        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1]
            next_level.append(sha256(left + right))

        level = next_level
        levels.append(level)

    return levels, levels[-1][0]


def build_merkle_proofs(leaves: List[bytes]) -> List[List[bytes]]:
    """
    Returns proofs in the exercise-friendly format:
      proofs[i] is a list of steps for leaf i
      each step is 33 bytes: direction_byte + sibling_hash(32)
        direction_byte: 0x00 => sibling on left, 0x01 => sibling on right
    """
    levels, _ = build_merkle_tree(leaves)
    n = len(levels[0])
    proofs: List[List[bytes]] = [[] for _ in range(n)]

    for leaf_index in range(n):
        idx = leaf_index

        for lvl in range(len(levels) - 1):  # stop before root level
            nodes = levels[lvl]

            # If this level would have been duplicated for odd length during building,
            # emulate the same here:
            if len(nodes) % 2 == 1:
                nodes = nodes + [nodes[-1]]

            is_right_node = (idx % 2 == 1)
            sibling_idx = idx - 1 if is_right_node else idx + 1
            sibling_hash = nodes[sibling_idx]

            # If current node is right, sibling is on left (0x00). Else sibling on right (0x01).
            direction = b"\x00" if is_right_node else b"\x01"
            proofs[leaf_index].append(direction + sibling_hash)

            idx //= 2

    return proofs