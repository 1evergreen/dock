from contextlib import contextmanager
from absl import logging
from time import time
import tempfile
import shutil
from typing import Optional
import os

@contextmanager
def timing(msg: str):
    logging.info(f'Started {msg}')
    tic = time()
    yield
    toc = time()
    logging.info('Finished %s in %.3f s'%(msg, toc-tic))

@contextmanager
def tmpdir_manager(base_dir : Optional[str] = None):
    """Temperory directory manager that deletes the dir on exit
    """    
    tmpdir = tempfile.mkdtemp(dir=base_dir)
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)


def basename(pdb_file: str) -> str:
    return os.path.abspath(pdb_file).rsplit('.', 1)[0]



# if __name__ == '__main__':
#     app.run(main)