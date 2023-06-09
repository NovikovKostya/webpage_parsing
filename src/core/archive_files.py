import os
import tarfile
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')


def archive_files(archive_path, archive_file_name, files) -> None:
    archive_name = os.path.join(archive_path, f'{archive_file_name}.tar.xz')
    with tarfile.open(archive_name, 'w:xz') as tar_obj:
        for file in files:
            tar_obj.add(file)
    logger.info(f'Saved to "{archive_name}"')