"""Run all of the unittests in rtvPlus
"""

import unittest

if __name__ == "__main__":
    suite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(suite)
