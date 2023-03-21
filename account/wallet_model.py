import sqlite3 as sql
import json

class WalletModel():
    def __init__(self, address, keystore, account_name):
        # self.password_wallet = password_wallet
        self.address = address
        self.keystore = keystore
        self.account_name = account_name

class ListWalletsModel():
    def __init__(self):
        self.database = "user/database.db"
        self.username = ""
        self.listWallet = []
        # self.main_wallet_idx = -1

    def insertWallet(self, username, address, keystore, account_name):
        if self._check_is_exist(username=username, address=address, account_name=account_name):
            return False, "Wallet is exist (Reason: same account_name or same address)"
        
        con = sql.connect(self.database)
        cur = con.cursor() 
        cur.execute("INSERT INTO wallets (username, wallet_address, encrypt_str, account_name) VALUES (?, ?, ?, ?)", \
                    (username, address, json.dumps(keystore), account_name))
        con.commit()
        con.close()
        self.username = username
        walletObj = WalletModel(address=address, keystore=json.dumps(keystore), account_name=account_name)
        self.listWallet.append(walletObj)
        return True, ""
    
    def removeWallet(self, account_name):
        for _wallet in self.listWallet:
            if account_name == _wallet.account_name:
                con = sql.connect(self.database)
                cur = con.cursor()
                print("Contents of the table after delete operation ")
                cur.execute("SELECT * from wallets")
                print(cur.fetchall())

                self.listWallet.remove(_wallet)
                print("Deleting")
                
                cur.execute("DELETE FROM wallets WHERE username='{}' and wallet_address ='{}' and account_name='{}'"\
                            .format(self.username, _wallet.address, account_name))
                con.commit()

                print("Contents of the table after delete operation ")
                cur.execute("SELECT * from wallets")
                print(cur.fetchall())
                cur.close()

    def _check_is_exist(self, username, address, account_name):
        con = sql.connect(self.database)
        cur = con.cursor()
        cur.execute("SELECT username, wallet_address FROM wallets WHERE username='{}' and (wallet_address ='{}' or account_name='{}')"\
                    .format(username, address, account_name))
        # users = cur.fetchall()
        
        if cur.fetchone() is None:
            con.close()
            return False
        else:
            con.close()
            return True

    def retrieveWallet(self, username):
        self.listWallet = []
        con = sql.connect(self.database)
        cur = con.cursor()
        cur.execute("SELECT username, wallet_address, encrypt_str, account_name FROM wallets WHERE username='{}'".format(username))
        wallets = cur.fetchall()
        if  wallets  is None:
            con.close()
            return None, "No wallet"
        else:
            for obj in  wallets:
                walletsObj = WalletModel(address = obj[1] ,keystore=obj[2], account_name=obj[3])
                self.listWallet.append(walletsObj)
            return self.listWallet, ""
        
    def select_account(self, account_name):
        for _wallet in self.listWallet:
            if account_name == _wallet.account_name:
                return _wallet
            
        return None

    