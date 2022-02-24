import numbers
from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path


def main():
    print('Working on ' + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print(f"The number of tokens you've deployed is {number_of_tokens}")
    write_metadata(number_of_tokens, advanced_collectible)

def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        breed = get_breed(nft_contract.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{str(token_id) + '-' + breed + '.json'}/"
        )
        # ./metadata/rinkeby/0-SHIBA_INU.json
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already found!")
        else:
            print(f'Creating metadata file {metadata_file_name}')
            collectible_metadata['name'] = get_breed(nft_contract.tokenIdToBreed(token_id))
            collectible_metadata['description'] = f'An adorable {collectible_metadata["name"]} pup!'
            print(collectible_metadata)