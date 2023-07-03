import logging
import os
import tarfile
import typing as t

logger = logging.getLogger(__name__)


def archive_files(archive_path: str, archive_file_name: str, files: t.List[str]) -> None:
    archive_name = os.path.join(archive_path, f'{archive_file_name}.tar.xz')
    with tarfile.open(archive_name, 'w:xz') as tar_obj:
        for file in files:
            tar_obj.add(file)
    logger.info(f'Saved to "{archive_name}"')
