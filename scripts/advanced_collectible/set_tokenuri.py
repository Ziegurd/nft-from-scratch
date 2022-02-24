from brownie import AdvancedCollectible, network, accounts, config
from scripts.helpful_scripts import get_breed


dog_metadata_dic = {
    'SHIBA_INU': 'https://ipfs.io/ipfs/QmZ14zyPFSNjiQT48UYyjULU1bA5YDqoaWCazr7isY5gg8?filename=0-SHIBA_INU.json',
    'PUG': 'https://ipfs.io/ipfs/QmXrt8YnUhAqBWcCPp8c6Uz5yHDRrgVD3hUp3fdgSPKv98?filename=1-PUG.json',
    'ST_BERNARD': 'https://ipfs.io/ipfs/QmfAiGHrPLi7amG2XniHTW5rGGta6SCZ1Gh4duNEnrBuJC?filename=2-ST_BERNARD.json',
}
OPENSEA_FORMAT = 'https://opensea.io/assets/{}/{}'
# https://testnets.opensea.io/assets/0x24ec6cDc29DA44bb7E2f0b3E8f14d636bE89BAA8/0

def main():
    print(f'Working on {network.show_active()}')
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f'The number of tokens you\'ve deployed is {str(number_of_advanced_collectibles)}')

    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith('http://'):
            print(f'Setting tokenURI of {token_id}')
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])
        else:
            print(f"Skipping {token_id}, we've already set that tokenURI!")


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config['wallets']['from_key'])
    nft_contract.setTokenURI(token_id, tokenURI, {'from': dev})
    
    print('Awesome! You can now view your NFT at {}'.format(
        OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )

    print("Please give up to 20 minutes, and hit the 'refresh metadata' button")