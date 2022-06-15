"""
parse the antibodys from results of rosetta antibody designer
"""
import os
import re
from absl import logging

def parse_pdb(path : str, pattern: str):
    """Read all pdb files that match a certain pattern

    Parameters
    ----------
    path : str
    pattern  : str
    Returns
    -------
    List
        list of files
    """    

    pattern = rf'{pattern}_\d+.pdb$'
    pattern = re.compile(pattern)
    return parse_pattern(path, pattern)

def parse_zdock_out(path: str):
    '''parse zdock.out files in the directory'''
    pattern = re.compile(r'.+zdock\.out')
    return parse_pattern(path, pattern)

def parse_pattern(path: str, pattern):
    files = os.listdir(path)
    logging.info(f'Parsing files that matches {pattern}')
    return [file for file in files if os.path.isfile(os.path.join(path, file)) \
         and re.match(pattern, file)]


def get_names(filename):
    """get the zdock out pdbs: antigen and antibody

    Parameters
    ----------
    filename : _type_
        _description_
    """    
    with open(filename, 'r') as f:
        while line := f.readline():
            if line.split()[0].endswith('.pdb'):
                antigen = line.split()[0]
                line = f.readline()
                antibody = line.split()[0]
                return antigen, antibody
    raise RuntimeError('No pdb files')


def correct_zdock(filename : str):
    with open(filename, 'r') as file:
        output = []
        while line := file.readline():
            if line.strip() != '0.000000	0.000000	0.000000':
                output.append(line)
    with open(filename, 'w') as file:
        file.writelines(output)
        
# print(parse('/data/wangww/protein/ab/ccs_ab/round2/results', 'round2start'))

