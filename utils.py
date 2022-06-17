from contextlib import contextmanager
from absl import logging
from time import time
import tempfile
import shutil
from typing import Optional
import os
import subprocess

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
    '''Get the abspath basename 
    '''
    return os.path.abspath(pdb_file).rsplit('.', 1)[0]


def wrapper(cmd: list, name:str) -> None:
    """A wrapper of bash binary command line excutables

    Parameters
    ----------
    cmd : list
        list of strs
    name : str
        binary name for msg

    """    
    logging.info('Launching subprocess zrank %s', ' '.join(cmd))
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with timing(name):
        stdout, stderr = process.communicate()   
        retcode = process.wait()
        logging.info('%s finished', name)
    if retcode:
        raise RuntimeError('%s failed "%s": "%s"'%(name, stderr.decode('utf-8'), ' '.join(cmd)))
    return 

# if __name__ == '__main__':
#     app.run(main)