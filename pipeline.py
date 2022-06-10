import utils
from zdock import Zdock
import split
import parse_files
import os
from absl import logging


class DataPipeline:
    """Runs the Zdock pipeline and assembles the output
    mark_suf -> zdock -> head -> create.pl
    """    
    def __init__(self, flags) -> None:
        self.flags = flags
        self.path = flags.path # Complex pdbs filepath
        assert os.path.isdir(self.path), 'Not a directory!'
        self.pattern = flags.pattern # complex name patterns
        # self.binary = binary  # zdock binary path
        self.zdock = Zdock(flags.binary)
        self._get_complex()

    def process(self):
        antibodies:list = self._get_antibody()
        antigen:str = self._get_antigen()
        return self.zdock.do_dock(antigen, antibodies)
    
    @property
    def basedir(self):
        return os.path.abspath(self.path)
    

    def _get_complex(self):
        logging.info('Parsing target complex pdb files...')
        self.complexes = parse_files.parse(self.path, self.pattern)
        logging.info('Found target complexes: ', '\n'.join(self.complexes))
        
    def _get_antibody(self):
        """get all antibody parts in the list

        Returns
        -------
        antibody pdb list
        """        
        # ab_list = self._get_complex()
        logging.info('Split antibodies from target complex pdb files...')
        antibodys = [] # a list to store the antibodys
        for complex in self.complexes:
            path = os.path.join(self.basedir, complex) # file abspath
            try:
                antibody = split.parse_ab(path, self.flags)
                antibodys.append(antibody)
                logging.info(f'Parse antibody successfully : f{antibody}')
            except IOError:
                print(f'No such pdb file : {path}')
        return antibodys
    
    def _get_antigen(self):
        # ab_list = self._get_complex()
        path = os.path.join(self.basedir, self.complexes[0])
        antigen = split.parse_antigen(path, self.flags)
        logging.info(f'Parse antigen successfully : f{antigen}')
        return antigen
        
            
