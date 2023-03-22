# Blockchain Wallet dApp
This app allows to manage user accounts and blockchain addresses, handle transactions as well as tracking tracsaction history in Python & Flask & Web3 with Ganache used to run tests and inspect state while controlling how the chain operates.

## Getting Started
1. Download Ganache (https://trufflesuite.com/ganache/) and start Ganache workplace (https://trufflesuite.com/docs/ganache/quickstart/).
2. Clone the directory, then `cd simple-wallet-dapp`
3. Install packages:
  `pip install -r requirements.txt`
 4. Run the following command:
  `python app.py`
  then you will see app is running on http://127.0.0.1:5000 or http://localhost:5000
  
## Description

### Wallet
Contains information regarding user wallet such as address, private key, balance, transaction history
  * Create Wallet:
  
    `localhost:5000/register`

  * Restore Wallet:

    `localhost:5000/login`

  * Wallet Information:

    `localhost:5000/account`

### Transaction

## File Contents
  * accounts/account.py - Implements functionality to generate wallet, address & private key and other security related algorithm or function
  * transactions/transaction.py - ???
  * app.py - Contains all the routes for app
  
## Demo
 * Video Link: 
