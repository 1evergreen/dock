from absl.testing import absltest
from ..pipeline import DataPipeline
FILENAME = 'complexOut_0008.pdb'

class splitTest(absltest.TestCase):
    
    def test_parse(self):