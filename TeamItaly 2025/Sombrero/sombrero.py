#!/usr/bin/env python3

from hash import Hash
import os

flag = os.getenv("FLAG", "TeamItaly{REDACTED}")

MAX_USERS = 5

users = {}

transactions = {}

def menu():
    print("""
1) Register
2) Create transaction
3) Spend transaction""")
    choice = int(input("> "))
    return choice

def register():
    if len(users) == MAX_USERS:
        print("Already too many users")
        return
    user_id = int(input("User id: "))
    assert user_id not in users and 120 <= user_id.bit_length() <= 128
    user_h = Hash(user_id)
    users[user_id] = {"h": user_h, "balance": 100, "spent_transactions": []}

def create_transaction():
    user_from = int(input("From: "))
    user_to = int(input("To: "))
    value = int(input("Value: "))
    transaction_id = int(input("Transaction id: "))

    assert user_from in users and (user_to in users or user_to == 0)
    assert users[user_from]["balance"] >= value and value >= 0
    assert transaction_id.bit_length() >= 128

    users[user_from]["balance"] -= value
    transactions[users[user_from]['h'].h(transaction_id)] = {
        'from': user_from,
        'to': user_to,
        'value': value
    }

def spend_transaction():
    user_from = int(input("From: "))
    transaction_id = int(input("Transaction id: "))

    transaction = transactions[users[user_from]['h'].h(transaction_id)]
    assert user_from in users and transaction_id not in users[user_from]["spent_transactions"]
    assert transaction['from'] == user_from

    users[user_from]["spent_transactions"].append(transaction_id)

    if transaction["to"] == 0 and transaction["value"] >= 1500:
        print(flag)
    else:
        users[transaction["to"]]["balance"] += transaction["value"]

funcs = [register, create_transaction, spend_transaction]

if __name__ == "__main__":
    print("Welcome to the anonymous centralized blockchain.")
    while True:
        choice = menu()
        funcs[choice-1]()