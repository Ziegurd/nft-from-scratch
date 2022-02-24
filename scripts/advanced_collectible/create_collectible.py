from urllib import request
from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_breed
import time


def main():
    dev = accounts.add(config['wallets']['from_key'])
    print(f"Using address: {dev}")
    print(f"Advanced Collectible({len(AdvancedCollectible)}): {AdvancedCollectible}")
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    for i in range(len(AdvancedCollectible)):
        print(f"Advanced Collectible-({i}): {AdvancedCollectible[i]}")
    transaction = advanced_collectible.createCollectible('None', {'from': dev})
    # wait for 2nd transaction
    transaction.wait(1)
    requestId = transaction.events['requestedCollectible']['requestId']
    print(f"Transaction requestId: {requestId}")
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    time.sleep(35)
    breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
    print(f'Dog breed of tokenId {token_id} is {breed}')