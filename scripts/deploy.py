from scripts.helpful_scripts import get_accounts,get_contract,fund_with_link
from brownie import Lottery,network,config
import time
def deploy_lottery():
    account = get_accounts()
    lottery = Lottery.deploy(50,
        get_contract("eth_usd_price_feed").address
        ,get_contract("vrf_coordinator").address
        ,get_contract("link_token").address
        ,config["networks"][network.show_active()]["fee"]
        ,config["networks"][network.show_active()]["key-hash"]
        ,{"from":account}
        ,publish_source=config["networks"][network.show_active()].get("verify",False)
    )    
    print("Deployed Lottery")
    return lottery

def start_lottery():
    account = get_accounts()
    lottery = Lottery[-1]
    starting_txn = lottery.startLottery({"from":account})
    starting_txn.wait(1)
    print("Thoe lottery is started")

def enter_lottery():
    account = get_accounts()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee()     
    entry_txn = lottery.enter({"from":account, "value":value})
    entry_txn.wait(1)
    print(f"{lottery.players(0)} is the first player")
    print("You are entered!")

def end_lottery():
    account = get_accounts()
    lottery = Lottery[-1]
    print(lottery.address)
    print(account)
    #print(f"{lottery.winner()}")
    # print(f"{lottery.players()}")
    # print(f"{lottery.players(0)}")
    end_txn = fund_with_link(lottery.address)
    end_txn.wait(1)
    endlottery_txn = lottery.endLottery({"from":account})
    endlottery_txn.wait(1)
    time.sleep(60)
    # print(f"{lottery.players(0)} is the first player")
    print(f"{lottery.winner()} is the winner")
    
    #print(f"{lottery.indexOfSelectedWinner()} is the index od selected winner")
    #print(f"{lottery.players()} is the address of the first index")
    # print(f"{lottery.players()} is the players")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

