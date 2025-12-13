# batch.py
import hashlib
from typing import List


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


class BatchExecutor:
    def __init__(self):
        self.current_batch_root: bytes | None = None
        self.executed: List[bytes] = []

    def set_batch_root(self, root: bytes) -> None:
        if len(root) != 32:
            raise ValueError("Merkle root must be 32 bytes")
        self.current_batch_root = root

    def _verify_one(self, signed_tx: bytes, proof: List[bytes]) -> bool:
        if self.current_batch_root is None:
            raise RuntimeError("No batch root set")

        current = sha256(signed_tx)

        for step in proof:
            if len(step) != 33:
                raise ValueError("Each proof step must be 33 bytes: dir(1) + sibling(32)")

            direction = step[0]
            sibling = step[1:]
            if len(sibling) != 32:
                raise ValueError("Sibling hash must be 32 bytes")

            if direction == 0x00:        # sibling on LEFT
                current = sha256(sibling + current)
            elif direction == 0x01:      # sibling on RIGHT
                current = sha256(current + sibling)
            else:
                raise ValueError(f"Invalid direction byte: {direction}")

        return current == self.current_batch_root

    def execute_batch(self, signed_txs: List[bytes], proofs: List[List[bytes]]) -> None:
        """
        Verify all proofs against current_batch_root.
        If any proof is invalid → drop the whole batch.
        If all are valid → execute all transactions.
        """
        if self.current_batch_root is None:
            raise RuntimeError("No batch root set")

        if len(signed_txs) != 10:
            raise ValueError(f"Expected 10 signed txs, got {len(signed_txs)}")
        if len(proofs) != len(signed_txs):
            raise ValueError("signed_txs and proofs length mismatch")

        # 1) verify everything first (atomic)
        for tx, proof in zip(signed_txs, proofs):
            if not self._verify_one(tx, proof):
                print("❌ Batch rejected: at least one Merkle proof is invalid")
                return

        # 2) all valid -> execute all
        for tx in signed_txs:
            self.executed.append(tx)
            print("Executing:", tx.decode("utf-8", errors="replace"))

        print("✅ Batch executed:", len(signed_txs), "transactions")