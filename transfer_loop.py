#!/usr/bin/env python3
import pymongo
from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern
import time
import random
import settings
import sys

def main():
    # Define the MongoDB Connection
    conn = pymongo.MongoClient(settings.URI)
    num_of_accts = settings.num_of_accts
    
    use_txns = True if ((len(sys.argv) > 1) and (sys.argv[1].strip().lower() == 'txns')) else False

    if use_txns:
        print("Transactions set to TRUE")
    else:
        print("Transactions set to FALSE (provide comand line arg 'txns' to use transactions)")

    db = conn["banking_txns"]
    coll_a = db["accts_a"]
    coll_b = db["accts_b"]
    coll_c = db["accts_c"]
    coll_d = db["accts_d"]
    
    colls_list = [ coll_a, coll_b, coll_c, coll_d ]

    num_transactions = settings.num_transactions
    num_transfers_per_txn = settings.num_transfers_per_txn

    for i in range(num_transactions):
        source_acct_list = []
        destin_acct_list = []

        source_coll_list = []
        destin_coll_list = []
        
        for i in range(num_transfers_per_txn):
            source_acct_list.append(get_random_acct_id(num_of_accts))
            destin_acct_list.append(get_random_acct_id(num_of_accts))
            
            source_coll_list.append(random.choice(colls_list))
            destin_coll_list.append(random.choice(colls_list))

            # Ensure the collections are different 
            while destin_coll_list[i] == source_coll_list[i]:
                destin_coll_list[i] = random.choice(colls_list)

        if use_txns:
            execute_transfers_in_txn(conn, source_acct_list, destin_acct_list, source_coll_list, destin_coll_list, num_transfers_per_txn)
        else:
            execute_transfer(source_acct_list, destin_acct_list, source_coll_list, destin_coll_list, num_transfers_per_txn)

def execute_transfers_in_txn(conn, source_acct_list, destin_acct_list, source_coll_list, destin_coll_list, num_transfers_per_txn):
    session = conn.start_session()
    session.start_transaction(read_concern=ReadConcern('snapshot'),write_concern=WriteConcern('majority', wtimeout=1000))
    
    for i in range(num_transfers_per_txn):
        transfer_amount = random.randint(0,15)

        source_acct = source_acct_list.pop()
        destin_acct = destin_acct_list.pop()
        source_coll = source_coll_list.pop()
        destin_coll = destin_coll_list.pop()

        source_coll.update_one({'cust_id': source_acct}, {'$inc': {'balance': - transfer_amount}}, session=session)
        time.sleep(0.1)
        destin_coll.update_one({'cust_id': destin_acct}, {'$inc': {'balance': transfer_amount}}, session=session)

        print(str(transfer_amount) + " transferred from: " + str(source_coll.name) + "." + str(source_acct) + " to  " + str(destin_coll.name) + "." + str(destin_acct))
    
    session.commit_transaction()

def execute_transfer(source_acct_list, destin_acct_list, source_coll_list, destin_coll_list, num_transfers_per_txn):
    for i in range(num_transfers_per_txn):
        transfer_amount = random.randint(0,15)

        source_acct = source_acct_list.pop()
        destin_acct = destin_acct_list.pop()
        source_coll = source_coll_list.pop()
        destin_coll = destin_coll_list.pop()

        source_coll.update_one({'cust_id': source_acct}, {'$inc': {'balance': - transfer_amount}})
        time.sleep(0.1)
        destin_coll.update_one({'cust_id': destin_acct}, {'$inc': {'balance': transfer_amount}})

        print(str(transfer_amount) + " transferred from: " + str(source_coll.name) + "." + str(source_acct) + " to  " + str(destin_coll.name) + "." + str(destin_acct))


def get_random_acct_id(num_of_accts):
    return random.randint(0, num_of_accts - 1)

if __name__ == "__main__":
    try:
        main()
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)