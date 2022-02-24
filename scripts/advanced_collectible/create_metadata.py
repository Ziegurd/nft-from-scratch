import os
import requests
import json
from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_breed
from pathlib import Path


breed_to_image_uri = {
    'PUG': 'https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png',
    'SHIBA_INU': 'https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png',
    'ST_BERNARD': 'https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png',
}


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
            f"./metadata/{network.show_active()}/{str(token_id) + '-' + breed + '.json'}"
        )
        # ./metadata/rinkeby/0-SHIBA_INU.json
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already found!")
        else:
            print(f'Creating metadata file {metadata_file_name}')
            collectible_metadata['name'] = get_breed(nft_contract.tokenIdToBreed(token_id))
            collectible_metadata['description'] = f'An adorable {collectible_metadata["name"]} pup!'
            # print(f'collectible_metadata: {collectible_metadata}')
            image_to_upload = None
            if os.getenv('UPLOAD_IPFS') == 'true':
                image_path = f"./img/{breed.lower().replace('_', '-')}.png"
                image_to_upload = upload_to_ipfs(image_path)            
            image_to_upload = breed_to_image_uri[breed] if not image_to_upload else image_to_upload
            collectible_metadata['image'] = image_to_upload
            with open(metadata_file_name, 'w') as outfile:
                json.dump(collectible_metadata, outfile)
            if os.getenv('UPLOAD_IPFS') == 'true':
                upload_to_ipfs(metadata_file_name)

# http://127.0.0.1:5001/
# curl -X POST -F file=@img/pug.png http://localhost:5001/api/v0/add

def upload_to_ipfs(filepath):
    with Path(filepath).open('rb') as f:
        image_binary = f.read()
        ipfs_url = 'http://localhost:5001'
        ipfs_api = ipfs_url + '/api/v0/add'
        response = requests.post(ipfs_api, files={'file': image_binary})
        ipfs_hash = response.json()['Hash']
        print(f'\nIPFS response: {response.json()}')
        filename = filepath.split('/')[-1]
        uri = f'https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}'
        print(f'URI: {uri}')
        return uri
    return None