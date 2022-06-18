from brownie import USDF, TransparentUpgradeableProxy, ProxyAdmin, Contract
from scripts.utils import  encode_function_data, get_account
import time

# Get deployment account & transacting account
deployment_owner_account = get_account(0)
test_account = get_account(1)



def deploy_token(deployment_account):
    deployed_token = USDF.deploy(
        {"from": deployment_account}
    )
    
    print("Token deployed...")
    print("Token: ", deployed_token.address)
    print("\n")

    return deployed_token

def deploy_token_proxy(deployment_account):

    #Step 1: Deploy token
    deployed_token = deploy_token(deployment_account)

    #Step  2: Deploy the admin proxy
    proxy_admin = ProxyAdmin.deploy(
       {"from": deployment_account}
    )

    #Step 2: Deploy token proxy
    token_proxy = TransparentUpgradeableProxy.deploy(
        deployed_token.address,
        proxy_admin.address,
        encode_function_data(deployed_token.initialize),
        {"from": deployment_account}
    )

    token_proxy = Contract.from_abi("token", token_proxy.address, deployed_token.abi)

    print("Proxies deployed...")
    print("Admin Proxy: ", proxy_admin.address)
    print("Token Proxy: ", token_proxy.address)
    print("\n")

    return token_proxy, proxy_admin


def main():
    token, admin = deploy_token_proxy(deployment_owner_account)
    time.sleep(1)
    pass