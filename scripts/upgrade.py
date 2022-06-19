from brownie import USDF, TransparentUpgradeableProxy, ProxyAdmin, Contract
from scripts.utils import  encode_function_data, get_account, upgrade
from scripts.deploy import deploy_token_proxy,  deploy_token
import time

# Get deployment account & transacting account
deployment_owner_account = get_account(1)
test_account = get_account(0)


def deploy_updates(deployment_account, proxy_admin, existing_proxy_address):

    #Step 1: Deploy logic contracts
    new_token =  deploy_token(deployment_account)
    print("Update new token: ", new_token)

    #Get proxies
    existing_token_proxy = Contract.from_abi("USDF", existing_proxy_address, USDF.abi) 

    #Step 2: upgrade bridge
    upgrade(
        deployment_account,
        existing_token_proxy,
        new_token,
        proxy_admin_contract=proxy_admin
        )

    pass


def main():

    token, admin = deploy_token_proxy(deployment_owner_account)
    token.mint(test_account, 10*10**18, {"from": deployment_owner_account}) 

    assert token.balanceOf(test_account) == 10*10**18

    deploy_updates(deployment_owner_account, admin, token)

    token.mint(test_account, 10*10**18, {"from": deployment_owner_account})

    assert token.balanceOf(test_account) == 20*10**18

    try:
        token.transfer(test_account, 10*10**18, {"from": deployment_owner_account})
    except Exception as e:
        print(e.message)
        assert e.message == "VM Exception while processing transaction: revert ERC20: transfer amount exceeds balance"

    try:
        token.mint(test_account, 10*10**18, {"from": test_account})
    except Exception as e:
        print(e.message)
        assert e.message == "VM Exception while processing transaction: revert AccessControl: account 0x66ab6d9362d4f35596279692f0251db635165871 is missing role 0x9f2df0fed2c77648de5860a4cc508cd0818c85b8b8a1ab4ceeef8d981c8956a6"

    time.sleep(1)
