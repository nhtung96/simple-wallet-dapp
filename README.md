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
Contains information and actions regarding user wallet such as address, private key, balance, ... or create, restore wallet, sh 
  * Account Info (List of Wallets):
  
    `localhost:5000/account`
    
  * Create Wallet:
  
    `localhost:5000/create`

  * Restore Wallet:

    `localhost:5000/restore`

  * Wallet Information:

    `localhost:5000/wallet_info`
   
  * Show private key:

    `localhost:5000/backup`

### Transaction
Handles transactions 
  * Handle transactions:

    `localhost:5000/transaction`
  
  * View transactions history:

    `localhost:5000/history`
    
## File Contents
  * account/wallet.py - Implements functionality to generate wallet, address & private key and other security related algorithm or function
  * account/wallet_model.py - Implements functionality related to Wallet's database such as  insert, remove wallet, check wallet is existed, ...
  * user/user_model.py - Implements functionality related to User's database such as  insert, load user info, check user is existed, ...
  * user/schema.sql - Define table schemas 
  * templates/ - Contains HTML files 
  * app.py - Contains all the routes for app
  
## Demo
 * Video Link: 
