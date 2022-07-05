#1983.69
#0.0252055512706118
from brownie import accounts,Lottery,network,config, web3,accounts,exceptions
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENT, fund_with_link,get_accounts, get_contract
from scripts.deploy import deploy_lottery
import pytest

def test_get_entrance_fees():
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    #Arrange
    lottery = deploy_lottery()
    #Act
    #1 eth => 2000 USD
    #FOr 50 USD, 0.025 eth
    entrance_fee = lottery.getEntranceFee()
    expected_entry_fee = web3.toWei(0.025,"ether")
    #Assert    
    assert entrance_fee == expected_entry_fee

def test_cant_enter_lottery_unless_started():
    account=get_accounts()
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    #Arrange
    lottery=deploy_lottery()
    #Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from":account,"value":lottery.getEntranceFee()})

def test_can_enter_lottery():
    account=get_accounts()
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    #Arrange
    lottery=deploy_lottery()    
    lottery.startLottery({"from":account})
    #Act
    lottery.enter({"from":account,"value":lottery.getEntranceFee()})
    #Assert
    assert lottery.players(0) == account

def test_can_start_and_end_lottery():
    account=get_accounts()
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    #Arrange
    lottery=deploy_lottery()  
    lottery.startLottery({"from":account})
    #Act
    lottery.enter({"from":account,"value":lottery.getEntranceFee()})

    #assert
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    assert lottery.lottery_state() == 2

def test_can_pick_winner_correctly():
    account=get_accounts()
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    #Arrange
    lottery=deploy_lottery() 
    lottery.startLottery({"from":account})
    lottery.enter({"from":account,"value": lottery.getEntranceFee()})
    lottery.enter({"from":get_accounts(index=1),"value": lottery.getEntranceFee()})
    lottery.enter({"from":get_accounts(index=2),"value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from":account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(request_id,STATIC_RNG,lottery.address,{"from":account})
    #777 % 3 = 0
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()

    assert lottery.winner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery