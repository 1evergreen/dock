'''
This script is used to split the antibody-antigen complex into two parts
- antibody
- antigen
'''

from Bio import PDB 
import os
import utils


def parse_ab(filename, config):
    """split the pdb structure into two parts

    Parameters
    ----------
    pose : _type_
        _description_
    """   
    basename = utils.basename(filename)
    chains, structure = get_chains(filename)
    antibody = {chain for chain in chains if chain.id.upper() in ['H', 'L']}
    return save_pdb(f'{basename}_antibody.pdb', config, antibody, structure)

def parse_antigen(filename, config):
    """parse the antigen part of the complex

    Parameters
    ----------
    filename : str
        

    Returns
    -------
    _type_
        _description_
    """    
    basename = utils.basename(filename)
    chains, structure = get_chains(filename)
    antigen = {chain for chain in chains if chain.id.upper() not in ['H', 'L']}
    return save_pdb(f'{basename}_antigen.pdb',config, antigen, structure)
     
def get_chains(filename):
    """get pdb chains from pdb file

    Parameters
    ----------
    filename : _type_
        _description_
    """    
    parser = PDB.PDBParser(PERMISSIVE=1, QUIET=True)
    name = os.path.basename(filename).split('.')[0]
    structure = parser.get_structure(name, filename)
    chains = list(structure.get_chains()) 
    return chains, structure

def save_pdb(name :str, config, chain_set: set, structure):
    """Save pdb_file based on selection

    Parameters
    ----------
    name : str
        
    config : _type_
        _description_
    chain_set : set
        chains selected
    structure : _type_
        pdb structure object
    """    
    io = PDB.PDBIO()
    io.set_structure(structure)
    select = ChainSelect(config, chain_set)
    io.save(name, select)
    return name

    
class ChainSelect(PDB.Select):
    """A class to determine which part to select for the output

    Parameters
    ----------
    PDB : _type_
        _description_
    """    
    def __init__(self, flags, chains):
        self.flags = flags 
        self.chains: set = {chain.id for chain in chains}
        
    def accept_chain(self, chain):
        """Determine the chains in the structure
        """        
        return chain.id in self.chains
    
    def accept_residue(self, residue):
        """
        Determine whether to remove water molecules 
        """        
        name = residue.get_resname()
        return not self.flags.ignore_water or name != 'HOH' 
        
    def accept_atom(self, atom):
        """
        Determine whether to remove hydrogen atoms
        """        
        if self.flags.ignore_H and atom.get_name() == 'H':
            return False
        else:
            return True
