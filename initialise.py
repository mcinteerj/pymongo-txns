#!/usr/bin/env python3
import pymongo
import settings 

def main():
    # Define the MongoDB Connection
    conn = pymongo.MongoClient(settings.URI)
    num_of_accts = settings.num_of_accts
    starting_balance = settings.starting_balance

    db = conn["banking_txns"]
    coll_a = db["accts_a"]
    coll_b = db["accts_b"]
    coll_c = db["accts_c"]
    coll_d = db["accts_d"]
    
    conn.drop_database("banking_txns")

    for i in range (num_of_accts):
            coll_a.insert_one({ "cust_id": i, "balance": starting_balance })
            coll_b.insert_one({ "cust_id": i, "balance": starting_balance })
            coll_c.insert_one({ "cust_id": i, "balance": starting_balance })
            coll_d.insert_one({ "cust_id": i, "balance": starting_balance })

    print("Complete")

if __name__ == "__main__":
    try:
        main()
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s" % e)