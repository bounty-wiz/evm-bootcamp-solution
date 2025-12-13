from eth_account import Account
from datetime import datetime
import json
import os

# Optional: enable mnemonic-based wallets (not needed for plain random key)
# Account.enable_unaudited_hdwallet_features()

def generate_geth_wallet(password: str, keystore_dir: str = "./keystore"):
    # 1. Create a new random private key
    acct = Account.create()

    private_key_hex = acct.key.hex()
    address = acct.address  # '0x....'

    print("New wallet generated:")
    print(f"  Address:     {address}")
    print(f"  Private key: {private_key_hex}")
    print("  (Store this private key securely and NEVER commit it to git.)")

    # 2. Encrypt private key to get geth-compatible keystore JSON
    keystore_json = Account.encrypt(private_key_hex, password)

    # 3. Prepare keystore directory
    os.makedirs(keystore_dir, exist_ok=True)

    # 4. Build filename similar to geth:
    #    UTC--YYYY-MM-DDTHH-MM-SSZ--<lowercase-address-no-0x>
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%SZ")
    addr_no_prefix = address.lower().replace("0x", "")
    filename = f"UTC--{timestamp}--{addr_no_prefix}"
    filepath = os.path.join(keystore_dir, filename)

    # 5. Save keystore JSON to file
    with open(filepath, "w") as f:
        json.dump(keystore_json, f)

    print(f"\nKeystore file written to: {filepath}")
    print("You can use this with geth / go-ethereum like any normal keystore file.")

    return {
        "address": address,
        "private_key": private_key_hex,
        "keystore_path": filepath,
    }


if __name__ == "__main__":
    # ⚠️ For real use, don’t hardcode the password; ask from input or env
    password = "change_this_password"

    wallet_info = generate_geth_wallet(password=password, keystore_dir="./keystore")