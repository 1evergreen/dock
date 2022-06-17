import utils
from binary import Zdock, Zrank, Hydration
from .scripts import block
import pdb_tool
import parse_files
import os
from absl import logging, flags


flags.DEFINE_integer('endnum', 10, 'zrank ending number')


class DockPipeline:
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
        assert len(self.complexes) > 0, 'No Target complexes'

    def process(self):
        antibodies:list = self._get_antibody()
        antigen:str = self._get_antigen()
        if self.flags.block:  # block the antigen
            self.flags.input = antigen
            self.flags.output = antigen
            antigen = self._block()  #blocked antigen file pdb
        return self.zdock.do_dock(antigen, antibodies)
    
    @property
    def basedir(self):
        return os.path.abspath(self.path)
    

    def _get_complex(self):
        logging.info(f'Parsing target complex pdb files from {self.path}...')
        self.complexes = parse_files.parse_pdb(self.path, self.pattern)
        logging.info('Found target complexes: \n%s'%'\n'.join(self.complexes))
        
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
            try:
                antibody = pdb_tool.parse_ab(complex, self.flags)
                antibodys.append(antibody)
                logging.info(f'Parse antibody successfully : {antibody}')
            except IOError:
                print(f'No such pdb file : {complex}')
        return antibodys
    
    def _get_antigen(self):
        # ab_list = self._get_complex()
        path = self.complexes[0]
        antigen = pdb_tool.parse_antigen(path, self.flags)  # abs path 
        logging.info(f'Parse antigen successfully : f{antigen}')
        return antigen
        
    def _block(self):
        '''Block the antigen'''
        logging.info(f'Start Blocking antigen files {self.flags.input}')
        return block.block(self.flags)
            
class ZRankPipeline:
    '''The zrank analysis pipeline'''
    
    def __init__(self, flags) -> None:
        self.flags = flags
        self.path = flags.path # Complex pdbs filepath
        assert os.path.isdir(self.path), 'Not a directory!'
        self.zrank = Zrank(flags)
        self.add_hydro = Hydration()
        self.zdock_outs = self._get_zdocks()
        assert len(self.zdock_outs) > 0, 'No Target zock file'

        
    def hydrate_pdbs(self, pdbfile):
        self.add_hydro.hydrate(pdbfile)
    
    def _get_zdocks(self):
        zdock_outs = parse_files.parse_zdock_out(self.path) 
        return [os.path.join(self.path, file) for file in zdock_outs] #lists of zdock file (abspath)
    
    def get_antigen_antibody(self, zdockfiles):
        antibody_pdbs = [parse_files.get_names(file)[1] for file in zdockfiles]
        antigen_pdb = parse_files.get_names(zdockfiles[0])[0]
        return antigen_pdb, antibody_pdbs
    
    def process(self):
        antigen, antibodies = self.get_antigen_antibody(self.zdock_outs)
        self.hydrate_pdbs(antigen)
        for antibody in antibodies:
            self.hydrate_pdbs(antibody) 
        for file in self.zdock_outs:
            parse_files.correct_zdock(file)
            self.zrank.rank(file)
        logging.info('Done!')
        
