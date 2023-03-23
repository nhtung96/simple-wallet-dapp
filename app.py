from flask import Flask, render_template, request, redirect
from web3 import Web3, HTTPProvider
# from eth_account import Account
from account import wallet
from user import user_model as dbHandler
from account import wallet_model as dbWallet
import json
import datetime
import pymongo

app = Flask(__name__)

# Initialize web3 provider
w3 = Web3(HTTPProvider('http://localhost:7545'))
## Global account
main_wallet_api = wallet.Wallet(w3)   
main_account = dbHandler.UserAccount()
list_wallet = dbWallet.ListWalletsModel()

@app.route('/account')
def account():
    print("main_account.username", main_account.username)
    list_wallet.retrieveWallet(main_account.username)
    return render_template('account.html', account_address = main_wallet_api.address, \
                           username=main_account.username, list_wallet = list_wallet.listWallet)

@app.route('/about')
def about():
    print(main_account.username)
    if main_account.username != "":
        return render_template('about.html', username = main_account.username)
    else:
        return render_template('about.html')

@app.route('/backup', methods=['POST'])
def backup():
    password = request.form["password"]
    print(password, main_account.password)
    if password == main_account.password:
        return render_template('backup.html', private_key=main_wallet_api.getPKHex())
    else:
        return render_template('backup.html', msg="Wrong passphrase")

@app.route('/restore_by_keystore', methods=['POST'])
def restore_by_keystore():
    account_name = request.form['account_name']
    # print("account_name", account_name)
    _wallet = list_wallet.select_account(account_name=account_name)
    # print(account_name, _wallet.account_name, _wallet.address)
    result = main_wallet_api.restore_by_keystore(json.loads(_wallet.keystore),\
                                                 main_account.password, account_name=account_name) 
    # print(main_wallet_api.address)
    if request.form['action'] == 'Choose':
        ## Restore wallet account 
        if result == "Success":
            list_wallet.insertWallet(main_account.username, main_wallet_api.address, _wallet.keystore, main_wallet_api.account_name)
            return redirect("/wallet_info")
        else:
            list_wallet.removeWallet(account_name=account_name)
            return redirect("/account")
    elif request.form['action'] == 'Remove':
        list_wallet.removeWallet(account_name=account_name)
        return redirect("/account")
    elif request.form['action'] == 'Show Key':
        return render_template('backup.html')

@app.route('/wallet_info')
def wallet_info():
    main_wallet_api.update_wallet()
    return render_template('wallet.html', address = main_wallet_api.address, username=main_account.username,\
                            balance = main_wallet_api.balance, transactions=main_wallet_api.transactions)

@app.route('/restore')
def restore():
	return render_template('restore.html')

@app.route('/restore_wallet', methods=['POST'])
def restore_wallet():
    private_key = request.form['private_key']
    account_name = request.form['account_name']
    result = main_wallet_api.restore_wallet(private_key, account_name)
    keystore = main_wallet_api.get_keystore(main_account.password)
    if result == "Success":
        status, msg = list_wallet.insertWallet(main_account.username, main_wallet_api.address, keystore, main_wallet_api.account_name)
        if status:
            return redirect("/wallet_info")
        else:
            return render_template('restore.html', error=msg)
    else:
        return render_template('restore.html', error=result)

@app.route('/create')
def create():
    # Register account
    main_wallet_api.create_wallet()
    return render_template('create.html', address = main_wallet_api.address, private_key = main_wallet_api.private_key)

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    # Register account
    account_name = request.form["account_name"]
    main_wallet_api.update_account_name(account_name=account_name)
    keystore = main_wallet_api.get_keystore(main_account.password)
    status, msg = list_wallet.insertWallet(main_account.username, main_wallet_api.address, keystore, account_name)
    print("Save DB: ",  main_wallet_api.address)
    if status:
        return redirect("/wallet_info")
    else:
        return render_template('create.html', address = main_wallet_api.address, private_key = main_wallet_api.private_key, msg=msg)



@app.route('/history')
def history():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["simple-dapp-wallet"]
    transactions = db.transactions.find({'$or': [ { 'from': main_wallet_api.address }, { 'to': main_wallet_api.address } ] } )
    return render_template('history.html', address = main_wallet_api.address, transactions=transactions)

@app.route('/transaction')
def transaction():
    return render_template('transaction.html', sender_address = main_wallet_api.address)

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    # Get the user input from the HTML form
    recipient_address = request.form['recipient_address']
    amount = request.form['amount']
    sender_address = request.form['sender_address'] 
    private_key = main_wallet_api.private_key


    # Create the transaction
    nonce = w3.eth.getTransactionCount(sender_address)
    txn_dict = {
        'from': sender_address,
        'to': recipient_address,
        'value': w3.toWei(amount, 'ether'),
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.toWei('50', 'gwei'),
    }

    # Sign transaction
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=private_key)

    # Send transaction
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)


    # Store transaction history to database
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["simple-dapp-wallet"]
    db.transactions.insert_one({
        "hash": tx_hash.hex(),
        "from": sender_address,
        "to": recipient_address,
        "value": amount,
        "timestamp": now,
    })

    return render_template('transaction.html', recipient_address=recipient_address, amount=amount, hash = tx_hash, \
                                                                                sender_address=sender_address)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        status, msg = main_account.retrieveUsers(username=username, password=password)
        if status:
            return redirect("/account") 
        else:
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        status, msg = main_account.insertUser(username=username, password=password)
        if status:
            return redirect("/account") 
        else:
            return render_template('register.html', msg=msg)
    else:
        return render_template('register.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    main_account.logout()
    return render_template("index.html")

if __name__ == '__main__':
	app.run(debug=True)
