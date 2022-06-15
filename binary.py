'''A module that wraps the zrank software for convience'''

import contextlib
from absl import logging
import utils

'''
./zrank 1PPE.zd2.3.fg.out 1 20
'''

class Zrank:
    def __init__(self, config) -> None:
        """Initialize the Python Zdock wrapper

        Parameters
        ----------
        binary_path : directory path of the zdock program
            _description_
        """        
        self.binary_path = config.binary
        self.config = config

    def rank(self, filename) -> str:
        '''input zdock file'''
        outfile = f'{filename}.zr.out'
        try: 
            ending_num = self.config.endnum
        except AttributeError:
            ending_num = 10
        cmd = [f'{self.binary_path}/zrank', filename, '1', str(ending_num)]
        with contextlib.suppress(RuntimeError):
            utils.wrapper(cmd, 'Zrank')
        return outfile
    
class Zdock:
    '''Using zdock to dock antigen and antibody'''
    
    def __init__(self, binary_path) -> None:
        """Initialize the Python Zdock wrapper

        Parameters
        ----------
        binary_path : directory path of the zdock program
            _description_
        """        
        self.binary_path = binary_path
    
    def do_dock(self, receptor, ligands) -> str:
        """Do auto zdock for a batch of ligands

        Parameters
        ----------
        receptor : _type_
            antigen pdb file
        ligands : _type_
            antibody pdb file lists

        Returns
        -------
        str
        """        
        receptor = self._mark_sur(receptor)
        return [self._dock(receptor, ligand) for ligand in ligands]
    
    def _dock(self, receptor, ligand) -> str:
        """Dock the ligand with receptor using zdock

        Parameters
        ----------
        receptor : Receptor pdb file
        ligand : Ligand pdb file
        
        Returns
        ---------
        str : output file name
        """  
        ligand = self._mark_sur(ligand)
        basename = utils.basename(ligand)
        outfile = f'{basename}_zdock.out'
        cmd = [f'{self.binary_path}/zdock', '-R', receptor, \
               '-L', ligand, '-o', outfile ]
        with contextlib.suppress(RuntimeError):
            utils.wrapper(cmd, 'Zdock')
        return outfile
        
    def _mark_sur(self, receptor) -> str:
        """mark surface of the pdb file

        Parameters
        ----------
        receptor : pdb file name
        Returns
        -------
        str
            output file name
        """        
        outfile = f'{utils.basename(receptor)}_m.pdb' 
        cmd = [f'{self.binary_path}/mark_sur', receptor, outfile]
        utils.wrapper(cmd, 'Mark_surface')
        return outfile


class Hydration:
    
    def __init__(self, config=None) -> None:
        """Initialize the Python PDB2PQR wrapper
        Note: should have pdb2pqr installed
        Parameters
        ----------
        config
            _description_
        """        
        self.config = config #TODO
    
    def hydrate(self, filename):
        """Add hydrogen to the pdb file and generate outputfile

        Parameters
        ----------
        filename : _type_
            _description_
        """        
        basename = utils.basename(filename)
        outfile = f'{basename}.pdb'
        #pdb2pqr30 [options] --ff={forcefield} {path} {output-path}
        cmd = ['pdb2pqr30','-ff=CHARMM', filename, f'{outfile}.pqr', '--pdb-output', f'{outfile}']
        utils.wrapper(cmd, 'PDB2PQR - Adding hydrogen')
        return outfile
