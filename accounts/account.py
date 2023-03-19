from web3 import Web3


class Transaction():
    def __init__(self, no, _from, _to, _hash, _amount, trans):
        self._from = _from
        self._to = _to
        self._hash = _hash
        self._amount = _amount
        self.trans = trans
        self.no = no
    
    def to_html(self):
         
        return """
        <div> Transaction {}
        <ul>
            <li>Transcation Hash: {}</li>
            <li>From: {}</li>
            <li>To: {}</li>
            <li>To: value</li>
        </ul>
        """.format(self.no, self._hash, self._from, self._to, self._amount)
        
# Initialize web3 provider
class Account():
    def __init__(self, _web3: Web3):
        self.wb3 = _web3
        self.address =  ""
        self.private_key = ""
        self.balance = 0
        self.transactions = []

    def restore_account(self, private_key):
        account = self.wb3.eth.account.privateKeyToAccount(private_key)
        print(account.address)
        if not self.wb3.isAddress(account.address):
            return 'Invalid address!'
        
        self.address = account.address
        self.private_key = private_key
        self.update_account()
        return "Success"

    
    def register_account(self): 
        _account = self.wb3.eth.account.create()
        self.address = _account.address
        self.private_key = _account.key
        self.update_account()
        return 'Create Account Successfully!!!'
    
    def update_account(self):
        self._get_balance()
        self._get_transaction()

    def _get_balance(self):
        # Get the account balance
        self.balance = self.wb3.eth.get_balance(self.address)
        self.balance = self.wb3.fromWei(self.balance, "ether")

    def _get_transaction(self):
        # Get the account balance
        currentBlock = self.wb3.eth.block_number;
        n = self.wb3.eth.getTransactionCount(self.address, currentBlock);
        bal = self.balance
        i = currentBlock
        self.transactions = []
        while (i >= 0 and (n > 0 or bal > 0)):
            block = self.wb3.eth.getBlock(i, True)
            if block and block.transactions:
                j = 0
                for trans in block.transactions:
                    # trans = self.wb3.eth.get_transaction(trans_hash)
                    if self.address == trans['from'] :
                        if trans['from'] != trans['to']:
                            bal = bal + trans.value
                            # self.transactions.append(Transaction(j, trans['from'], trans['to'], trans['hash'], trans['value'], trans).to_html)
                            self.transactions.append("Transaction {}:\n  - Transaction hash: {}\n  - From: {}\n  - To: {}\n  - Amount: {}\n"
                                                     .format(j, trans['hash'], trans['from'], trans['to'], trans['value']))
                            j = j + 1
                    
                    if (self.address == trans.to):
                        if trans['from'] != trans['to']:
                            bal = bal - trans['value']
                            # self.transactions.append(Transaction(j, trans['from'], trans['to'], trans['hash'], trans['value'], trans).to_html())
                            self.transactions.append("Transaction {}:\n  - Transaction hash: {}\n  - From: {}\n  - To: {}\n  - Amount: {}\n"
                                                     .format(j, trans['hash'], trans['from'], trans['to'], trans['value']))
                            j = j + 1
            i = i - 1
