
from brownie import accounts,network,config,MockV3Aggregator,VRFCoordinatorMock,LinkToken,Contract

LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development","ganache-local"]
FORKED_LOCAL_ENVIRONMENT=["mainnet-fork-dev"]
contract_to_mock={"eth_usd_price_feed": MockV3Aggregator,
                    "vrf_coordinator":VRFCoordinatorMock,
                    "link_token":LinkToken}
Decimals = 18
Starting_Value=2000
def get_accounts(index=None,id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT 
        or network.show_active() in FORKED_LOCAL_ENVIRONMENT):
        return accounts[0]    
    return accounts.add(config["wallets"]["from_key"])

def get_contract(contract_name):
    """This function will grab the contract addresses from the brownie config 
    if defined, otherwise, it will deploy a mock version of that contract, and 
    return that mock contract.
    """
    contract_type=contract_to_mock[contract_name]
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        if(len(contract_type)<=0):
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        #address
        #ABI
        contract = Contract.from_abi(contract_type._name,contract_address,contract_type.abi)
    return contract



def deploy_mocks():
    account=get_accounts()
    #MockV3Aggregator.deploy(Decimals,Web3.toWei(Starting_Value,"ether"),{"from":get_accounts()})     
    MockV3Aggregator.deploy(Decimals,Starting_Value,{"from":account})  
    link_token = LinkToken.deploy({"from":account})
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})
    print("Deployed")

def fund_with_link(
    contract_address,
    account=None,
    link_token=None,
    amount = 1000000000000000000
):
    account = account if account else get_accounts()
    link_token = link_token if link_token else get_contract("link_token")
    #Transfer link token to contract with some amount
    txn = link_token.transfer(contract_address,amount,{"from":account})
    txn.wait(1)
    print("Funded contract")
    return txn
