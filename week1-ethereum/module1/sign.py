# sign.py
from dataclasses import dataclass
from typing import List


@dataclass
class Tx:
    from_addr: str
    to_addr: str
    value: str
    data: str


def sign(tx: Tx) -> bytes:
    """
    Fake signing: serialize the transaction into bytes.
    """
    encoded = f"{tx.from_addr}|{tx.to_addr}|{tx.value}|{tx.data}"
    return encoded.encode("utf-8")


def create_and_sign_batch() -> List[bytes]:
    signed_txs: List[bytes] = []
    for i in range(1, 11):
        tx = Tx(
            from_addr=f"0xSENDER{i}",
            to_addr=f"0xRECEIVER{i}",
            value=str(100 * i),
            data=f"tx-{i}",
        )
        signed_txs.append(sign(tx))
    return signed_txs