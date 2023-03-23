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
            <li>To: {} ETH</li>
        </ul>
        """.format(self.no, self._hash, self._from, self._to, '%.2f' % (self._amount))
        
# Initialize web3 provider
class Wallet():
    def __init__(self, _web3: Web3):
        self.wb3 = _web3
        self.address =  ""
        self.account_name = ""
        self.private_key = ""
        self.balance = 0
        self.transactions = []

    def restore_wallet(self, private_key, account_name):
        account = self.wb3.eth.account.privateKeyToAccount(private_key)
        # print("After decrypt: ", account.address)
        print(account.address)
        if not self.wb3.isAddress(account.address):
            return 'Invalid address!'
        
        self.address = account.address
        self.private_key = private_key
        self.account_name = account_name
        self.update_wallet()
        return "Success"

    
    def create_wallet(self): 
        _account = self.wb3.eth.account.create()
        self.address = _account.address
        self.private_key = self.wb3.toHex(_account.key)
        self.update_wallet()
        print("New address: ", self.address)
        return 'Create Account Successfully!!!'
    
    def update_wallet(self):
        self._get_balance()
        self._get_transaction()

    def getPKHex(self):
        try:
            pk = self.wb3.toHex(self.private_key)
            return pk
        except:
            return self.private_key
    
    def _get_balance(self):
        # Get the account balance
        self.balance = self.wb3.eth.get_balance(self.address)
        self.balance = self.wb3.fromWei(self.balance, "ether")

    def _get_transaction(self):
        # Get the account transactions
        currentBlock = self.wb3.eth.block_number;
        n = self.wb3.eth.getTransactionCount(self.address, currentBlock);
        bal = self.balance
        i = currentBlock
        self.transactions = []
        while (i >= 0 and (n > 0 or bal > 0)):
            block = self.wb3.eth.getBlock(i, True)
            if block and block.transactions:
                j = len(self.transactions)
                for trans in block.transactions:
                    # trans = self.wb3.eth.get_transaction(trans_hash)
                    if self.address == trans['from'] :
                        if trans['from'] != trans['to']:
                            bal = bal + trans.value
                            transaction = Transaction(j, trans['from'], trans['to'], self.wb3.toHex(trans['hash']), \
                                                      self.wb3.fromWei(trans['value'], "ether"), trans)
                            self.transactions.append(transaction)
                            # self.transactions.append("Transaction {}:\n  - Transaction hash: {}\n  - From: {}\n  - To: {}\n  - Amount: {}\n"
                            #                          .format(j, trans['hash'], trans['from'], trans['to'], trans['value']))
                            j = j + 1
                    
                    if (self.address == trans.to):
                        if trans['from'] != trans['to']:
                            bal = bal - trans['value']
                            transaction = Transaction(j, trans['from'], trans['to'], self.wb3.toHex(trans['hash']), \
                                                      self.wb3.fromWei(trans['value'], "ether"), trans)
                            self.transactions.append(transaction)
                            # self.transactions.append("Transaction {}:\n  - Transaction hash: {}\n  - From: {}\n  - To: {}\n  - Amount: {}\n"
                            #                          .format(j, trans['hash'], trans['from'], trans['to'], trans['value']))
                            j = j + 1
            i = i - 1

    def get_keystore(self, password):
        return self.wb3.eth.account.encrypt(self.private_key, password)

    def restore_by_keystore(self, keystore, password, account_name):
        private_key = self.wb3.eth.account.decrypt(keystore, password)
        return self.restore_wallet(private_key, account_name=account_name)

    def update_account_name(self, account_name):
        self.account_name = account_name