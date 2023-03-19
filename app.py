from flask import Flask, render_template, request
from web3 import Web3, HTTPProvider
# from eth_account import Account
from accounts import account

app = Flask(__name__)

# Initialize web3 provider
w3 = Web3(HTTPProvider('http://localhost:7545'))
## Global account
main_account = account.Account(w3)   


@app.route('/')
def index():
    return render_template('index.html', account_address = main_account.address)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
def account():
    main_account.update_account()
    return render_template('account.html', address = main_account.address, \
                            balance = main_account.balance, transactions=main_account.transactions)

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/restore_account', methods=['POST'])
def restore():
    private_key = request.form['private_key']
    result = main_account.restore_account(private_key)

    if result == "Success":
        # return render_template('register.html', address = main_account.address, private_key = main_account.private_key)
        return render_template('account.html', address = main_account.address, \
                            balance = main_account.balance, transactions=main_account.transactions)
    else:
        return render_template('login.html', error=result)

@app.route('/register')
def register():
    # Register account
    main_account.register_account()
    return render_template('register.html', address = main_account.address, private_key = main_account.private_key)

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/balance')
def balance():
    return render_template('balance.html')

@app.route('/get_balance', methods=['POST'])
def get_balance():
    # Get address from query parameter
    address = request.form['address']

    # Check if address is valid
    if not w3.isAddress(address):
        return 'Invalid address!', 400

    # Get the account balance
    balance = w3.eth.get_balance(address)
    balance = w3.fromWei(balance, "ether")
    return render_template('balance.html', address=address, balance=balance)

@app.route('/transaction')
def transaction():
    return render_template('transaction.html', sender_address = main_account.address)

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    # Get the user input from the HTML form
    recipient_address = request.form['recipient_address']
    amount = request.form['amount']
    sender_address = request.form['sender_address'] # Replace with your actual private key

    # Create the transaction
    tx_hash = w3.eth.send_transaction({
    'from': sender_address,
    'to': recipient_address,
    'value': w3.toWei(amount, 'ether'),
})
    return render_template('transaction.html', recipient_address=recipient_address, amount=amount, hash = tx_hash, \
                                                                                sender_address=sender_address)

if __name__ == '__main__':
	app.run(debug=True)
