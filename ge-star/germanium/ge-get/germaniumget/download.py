import zipfile
import requests
from tqdm import tqdm


BLOCK_SIZE = 32 * 1024
MEGABYTE = 1024 * 1024


def download(url: str,
             file_name: str,
             session=None) -> None:
    """
    Download the given file.
    """
    if session is None:
        session = requests.Session()

    response = session.get(url,
                           allow_redirects=False,
                           stream=True,
                           headers={
                               'Cookie': 'oraclelicense=accept-securebackup-cookie',
                           })

    file_size = int(response.headers.get('content-length', 0))
    total_size = file_size / BLOCK_SIZE

    # we handle the redirect manually, since the requests
    # library is dropping the cookies on redirect atm
    if response.is_redirect:
        return download(response.next.url, file_name, session)  # type: ignore

    with open(file_name, 'wb') as f:
        for data in tqdm(response.iter_content(BLOCK_SIZE),
                         total=total_size + 1,
                         unit='M',
                         unit_scale=BLOCK_SIZE / MEGABYTE,
                         bar_format="{l_bar}{bar}| %0.2fM [{elapsed}<{remaining}, {rate_fmt}]" % (file_size / MEGABYTE),
                         miniters=1):
            f.write(data)


def extract_zip(zip_file: str,
                target_folder: str):
    """
    Extract the given zip file into the target folder.
    """
    if not zip_file:
        raise Exception("You need to specify a zip file to extract.")

    if not target_folder:
        raise Exception("You need to specify a target folder where to extract the zip file.")

    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(target_folder)
