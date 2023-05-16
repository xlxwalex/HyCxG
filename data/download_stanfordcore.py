import requests
from tqdm import tqdm
import zipfile

STANFORD_CORE_LINK = 'https://expic.xlxw.org/hycxg/stanfordcore/stanford-corenlp-3.9.2-minimal.zip'

def download_stanfordcore(url: str, fname: str):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))

    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def unzip_stanfordcore(file_name: str, out_path: str=r'.'):
    file_zip = zipfile.ZipFile(file_name, 'r')
    for file in file_zip.namelist():
        file_zip.extract(file, out_path)
    file_zip.close()

if __name__ == '__main__':
    download_stanfordcore(STANFORD_CORE_LINK, 'stanford-corenlp-3.9.2-minimal.zip')
    print('>> stanford-corenlp-3.9.2-minimal.zip is downloaded.')
    unzip_stanfordcore('stanford-corenlp-3.9.2-minimal.zip')
    print('>> Stanford Core files are ready.')
