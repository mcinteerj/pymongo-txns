#!/usr/bin/env python3
import pymongo
from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern
import time
import settings
import sys

def main():
    # Define the MongoDB Connection
    conn=pymongo.MongoClient(settings.URI)

    use_txns = True if ((len(sys.argv) > 1) and (sys.argv[1].strip().lower() == 'txns')) else False

    if use_txns:
        print("Transactions set to TRUE")
    else:
        print("Transactions set to FALSE (provide comand line arg 'txns' to use transactions)")

    db = conn["banking_txns"]
    collection = db["accounts"]
    coll_a = db["accts_a"]
    coll_b = db["accts_b"]
    coll_c = db["accts_c"]
    coll_d = db["accts_d"]
    
    colls_list = [ coll_a, coll_b, coll_c, coll_d ]

    while True:
        total_balance = 0
        
        if use_txns:
            balances_list = get_balances_in_txn(conn, colls_list)
        else:
            balances_list = get_balances(colls_list)
        
        #print(balances_list)
        print("Total of Bals: " + str(sum(balances_list)))

        time.sleep(0.05)

def get_balances(colls_list):
    balances_list = []

    for coll in colls_list:
        cursor = coll.find({})
        for acct in cursor:
            balances_list.append(acct['balance'])

    return balances_list

def get_balances_in_txn(conn, colls_list):
    balances_list = []
    
    session = conn.start_session()
    session.start_transaction(read_concern=ReadConcern('snapshot'))

    for coll in colls_list:
        cursor = coll.find({},session=session)
        for acct in cursor:
            balances_list.append(acct['balance'])

    session.commit_transaction()

    return balances_list

if __name__ == "__main__":
    try:
        main()
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)