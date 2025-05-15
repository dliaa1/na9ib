import time
import requests
from web3 import Web3

# إعداد API من Alchemy
ALCHEMY_URL = "https://eth-mainnet.g.alchemy.com/v2/F5cp48aOUUiy-Dmsi9Xnwln-xshvii_0"
web3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))

# جلب آخر بلوك
def get_latest_block():
    return web3.eth.block_number

# فحص حسابات في البلوك
def scan_block(block_number):
    block = web3.eth.get_block(block_number, full_transactions=True)
    for tx in block.transactions:
        to_addr = tx.to
        if to_addr:
            try:
                code = web3.eth.get_code(to_addr)
                if code != b'':
                    balance = web3.eth.get_balance(to_addr)
                    eth_balance = web3.from_wei(balance, 'ether')
                    if eth_balance > 0:
                        print(f"=== العقد: {to_addr} === الرصيد: {eth_balance} ETH")
            except Exception as e:
                print(f"خطأ في {to_addr}: {e}")

# المراقبة المستمرة
def monitor():
    print("انطلاق دجاجة النقيب الآلية ... كل دقيقة تفتيش جديد")
    last_block = get_latest_block()
    while True:
        latest_block = get_latest_block()
        if latest_block > last_block:
            for b in range(last_block + 1, latest_block + 1):
                print(f"Scanning block: {b}")
                scan_block(b)
            last_block = latest_block
        time.sleep(60)

if __name__ == "__main__":
    monitor()
