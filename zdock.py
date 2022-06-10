'''A module that wraps the zdock software for convience'''
import subprocess
from absl import logging
import utils

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
            _description_
        """        
        receptor = self._mark_sur(receptor)
        ligands = [self._mark_sur(ligand) for ligand in ligands]
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
        receptor = self._mark_sur(receptor)
        ligand = self._mark_sur(ligand)
        basename = utils.basename(receptor)
        outfile = f'{basename}_zdock.out'
        cmd = [f'{self.binary_path}/zdock', '-R', receptor,
               '-L', ligand, '-o', outfile ]   
        logging.info('Launching subprocess zdock "%s"'%(' '.join(cmd))) 
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with utils.timing('Zdock'):
            stdout, stderr = process.communicate()
            retcode = process.wait()
            logging.info('Zdock finished')
        if retcode:
            raise RuntimeError('Zdock failed "%s"'%stderr.decode('utf-8'))
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
        logging.info('Launching subprocess "%s"'%(' '.join(cmd)))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with utils.timing('Mark surface'):
            stdout, stderr = process.communicate()
            retcode = process.wait()
            logging.info('Mark surface completed')
        
        if retcode:
            raise RuntimeError('Mark surface failed: \n%s'%stderr.decode('utf-8'))
        return outfile
    
    
    def zrank(self) -> str:
        pass