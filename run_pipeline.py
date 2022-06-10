'''
This protocol is used for auto zdock for rosetta antibody results
Usage python run_pipeline --pattern pattern
>>> 
'''
from absl import flags,app
from pipeline import DataPipeline


#
flags.DEFINE_string('pattern', default=None, help='Filename pattern', required=True)
flags.DEFINE_string('path', default='.', help='pdb file directory path')
flags.DEFINE_string('binary', default='.', help='zdock and zrank binary path')
#pdb parse options
flags.DEFINE_bool('ignore_H', default=True, help='Whether to remove hydrogen')
flags.DEFINE_bool('ignore_water', default=True, help='Whether to remove water in the structure')
#TODO flags.DEFINE_bool('ignore_nonstandard', default=False, help='Whether to remove non-standard amino acids')

FLAGS = flags.FLAGS

def main(argv):
    
    mypipeline = DataPipeline(FLAGS)
    print(mypipeline.process())
    
if __name__ == '__main__':
    app.run(main)