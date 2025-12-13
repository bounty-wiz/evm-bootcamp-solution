# run_demo.py
from sign import create_and_sign_batch
from aggregate import build_merkle_root, build_merkle_proofs
from batch import BatchExecutor


def main():
    signed_txs = create_and_sign_batch()

    root = build_merkle_root(signed_txs)
    proofs = build_merkle_proofs(signed_txs)

    executor = BatchExecutor()
    executor.set_batch_root(root)

    executor.execute_batch(signed_txs, proofs)


if __name__ == "__main__":
    main()