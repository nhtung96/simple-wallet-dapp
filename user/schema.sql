drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);


drop table if exists wallets;
    create table wallets (
    id integer primary key autoincrement,
    username text not null,
    wallet_address text not null,
    encrypt_str text not null,
    account_name text not null
);
