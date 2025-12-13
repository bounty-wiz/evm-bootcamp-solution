import hashlib
from typing import List, Tuple

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def hash_pair(left: bytes, right: bytes) -> bytes:
    return sha256(left + right)

def leaf_hash_from_int(value: int) -> bytes:
    """
    Hash the leaf as SHA-256(str(value)).
    This matches the encoding used in the previous Merkle tree task.
    """
    return sha256(str(value).encode())

def verify_merkle_proof(
    merkle_root_hex: str,
    value: int,
    proof: List[Tuple[str, str]],
) -> bool:
    """
    Verify that `value` is part of the Merkle tree with given `merkle_root_hex`,
    using the provided `proof`.

    merkle_root_hex: hex string of the root (e.g. "abcd1234...")
    value:           the leaf value (int)
    proof:           list of (direction, sibling_hex) tuples, where:
                     - direction is "left" or "right"
                     - sibling_hex is hex string of the sibling node hash

    Example proof format:
        proof = [
            ("right", "aabbcc..."),  # sibling was on the right of the leaf
            ("left",  "ddeeff..."),  # sibling was on the left at next level
        ]
    """
    # 1. Start from the leaf hash
    current = leaf_hash_from_int(value)

    # 2. Rebuild the path up using the proof
    for direction, sibling_hex in proof:
        sibling = bytes.fromhex(sibling_hex)

        if direction == "left":
            current = hash_pair(sibling, current)
        elif direction == "right":
            current = hash_pair(current, sibling)
        else:
            raise ValueError(f"Invalid direction: {direction}, expected 'left' or 'right'")

    # 3. Compare with the given Merkle root
    expected_root = bytes.fromhex(merkle_root_hex)
    return current == expected_root


# Example usage (you would replace these with real values in your assignment)
if __name__ == "__main__":
    # Dummy example values. Replace with real data from your Merkle tree builder.
    example_merkle_root_hex = "42b43629c25f21b4b9cf6870c574a0e219ffe3db506e288e9be411f3008e7b23"
    example_value = 3

    # Example proof: this is just a placeholder; should come from your tree.
    example_proof = [
        ("right", "4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a"),
        ("left",  "4295f72eeb1e3507b8461e240e3b8d18c1e7bd2f1122b11fc9ec40a65894031a"),
        ("right", "79444487c2fe83fce6e3745dec21fa2432e1683c5e2aa2d33f7bc295d0ec3638"),
    ]

    is_valid = verify_merkle_proof(example_merkle_root_hex, example_value, example_proof)
    print("Proof valid?", is_valid)