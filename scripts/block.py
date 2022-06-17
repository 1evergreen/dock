'''
This file is used to block residues if you know which domain the antibody interacts with

Usage:
>>> python block.py --input [masked.pdb]--list [list_file] --[no]include --output [output_path]

'''
from absl import logging, flags, app
flags.DEFINE_boolean('include', default=True, help='whether to block the residues in the list file, default True')
flags.DEFINE_string('input', default=None, required=True, help='input pdb file to block')
flags.DEFINE_string('list', default=None, required=True, help='block list file')
flags.DEFINE_string('output', default=None, required=True, help='output pdb file')
FLAGS = flags.FLAGS

def block(config):
    '''Read in the input pdb file and block file
    return the blocked list'''
    output = []
    block_set = _block_file(config.list)  # get the block set
    #Read the list and pdb file to make changes and block atoms
    with open(config.input, 'r') as pdb:
        for line in pdb:
            if line.startswith('ATOM'):
                chain, resi = _chain_resi(line)
                if _is_blocked(chain, resi, block_set, config.include):
                    line = _block_atom(line)
            output.append(line)
    logging.info('Writing blocked pdb into %s', config.output)
    with open(config.output, 'w') as out:
        out.writelines(output)
    return config.output
    

def _chain_resi(line:str ) -> str:
    '''Get the line chain and residue number'''
    assert line.startswith('ATOM'), f'Not an ATOM Line: {line}'
    chain =  line.split()[4] #str
    resi = line.split()[5] # str
    return chain, resi

def _block_atom(line:str) -> str:
    '''change the ATC to 19'''
    return f'{line[:55]}19{line[57:]}'

def _is_blocked(chain, resi, block_set, include):
    '''Return True only if the atom in the block set and include
    or not include and not in the block set'''
    if include:
        if (chain, resi) in block_set:
            return True
        else:
            return False
    elif (chain, resi) in block_set:
        return False
    else:
        return True

def _block_file(filename: str):
    with open(filename, 'r') as file:
        text = file.readlines()
    return {(resi.strip()[0], resi.strip()[1:]) for resi in text}  # set

def main(argv):
    del argv
    block(FLAGS)
if __name__ == '__main__':
    app.run(main)
    