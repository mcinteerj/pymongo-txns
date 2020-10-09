# Transactions pymongo
This repo contains some basic demo scripts used to illustrate the implementation of transactions with MongoDB in Python.

The `monitor.py` script repeatedly calculates the sum of balances across all account documents in four collections, while the `transfer_loop.py` script transfers random amounts between random accounts across collections.

If the transfers are ACID compliant then the monitor will report a consistent total balance across the entire system (as no money is entering/leaving the system, only internal transfers are taking place). 

However, if the transfers are not ACID compliant then the monitor may report a balance which varies - this is because the monitor may either:
* See data at a point in time when funds have left one account and not yet arrived in another (i.e. the monitor can see inside of a transfer which is not adhering to the principle of **ISOLATION**) OR
* It may read the balances for different collections at different moments in a way which is interleaves with complete transactions (i.e. the monitor is not reading from a data source exhibiting the principle of **CONSISTENCY**)

By default, neither the monitor nor the transfer loop will use transactions and consequently the system will not exhibit either **ISOLATION** or **CONSISTENCY** principles. 

The argument `txns` can be passed to either of the monitor of transfer_loop scripts in order to alter this behaviour. Specifically:

* Providing the `txns` argument to the `monitor.py` script ensures **CONSISTENT** reads
* Providing the `txns` argument to the `transfer_loop.py` script ensures **ISOLATED** write transactions

# Usage
1. Configure your connection string in `./settings.py`
2. Adjust any other config in the settings as you wish
3. Run `initialise.py` to create the DB/Collections/Data
4. Run `monitor.py` to start the monitor
5. Run `transfer_loop.py` to start the transfer loop

The `monitor.py` and `transfer_loop.py` scripts both take an option argument 'txns' which indicates the use of transactions (in order to guarantee consistency/isolation behaviours).

```
python3 initialise.py
python3 monitor.py txns
python3 transfer_loop.py txns