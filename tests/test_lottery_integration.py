from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENT, fund_with_link
from brownie import accounts,network
from scripts.helpful_scripts import get_accounts,get_contract
from scripts.deploy import deploy_lottery
import pytest
import time

def test_can_pick_winner():
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    account=get_accounts()
    lottery = deploy_lottery()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account,"value":lottery.getEntranceFee()})
    lottery.enter({"from":account,"value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    time.sleep(60)
    assert lottery.winner() == account
    assert lottery.balance() == 0