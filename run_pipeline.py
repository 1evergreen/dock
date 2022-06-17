'''
This protocol is used for auto zdock for rosetta antibody results
Usage python run_pipeline --pattern pattern
>>> 
'''
from absl import flags,app, logging
from pipeline import DockPipeline, ZRankPipeline


#
flags.DEFINE_string('pattern', default=None, help='Filename pattern', required=True)
flags.DEFINE_string('path', default='.', help='pdb file directory path')
flags.DEFINE_string('binary', default='.', help='zdock and zrank binary path')
#pdb parse options
flags.DEFINE_bool('ignore_H', default=True, help='Whether to remove hydrogen')
flags.DEFINE_bool('ignore_water', default=True, help='Whether to remove water in the structure')
#TODO flags.DEFINE_bool('ignore_nonstandard', default=False, help='Whether to remove non-standard amino acids')
flags.DEFINE_string('mode', 'all', 'dock or analysis')
flags.DEFINE_bool('block', default=False, help='Whether to block the antigen')
FLAGS = flags.FLAGS

def main(argv):
    if FLAGS.mode in ['all', 'dock']: 
        dock_pipeline = DockPipeline(FLAGS)
        dock_pipeline.process()
    if FLAGS.mode in ['all', 'analysis']:
        analyse_pipeline = ZRankPipeline(FLAGS)
        analyse_pipeline.process()
    logging.info('%s DONE', FLAGS.mode.upper())
    
    
if __name__ == '__main__':
    app.run(main)