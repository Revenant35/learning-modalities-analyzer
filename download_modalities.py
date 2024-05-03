import requests
from tqdm import tqdm


def download_modalities(filename):
    response = requests.get("https://healthdata.gov/api/views/a8v3-a3m3/rows.csv?accessType=DOWNLOAD", stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024

    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, miniters=True, desc=f"Downloading {filename}")

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")


if __name__ == "__main__":
    download_modalities("data.csv")
