import argparse
import os
import sys


class PathManager:

    _sys_var_name = 'LiveLondonBusMapPath'

    def __init__(self):
        self._root = self.test_path_setup()

    @staticmethod
    def test_path_setup():
        root = os.environ.get(PathManager._sys_var_name)
        if not root:
            print('System variable', "'" + PathManager._sys_var_name + "'", 'has not been configured.',
                  'Please run setup_env.bat in the root folder before continuing!',
                  file=sys.stderr)
            sys.exit(-1)
        return root

    def project_root(self):
        return self._root

    def get_credentials_dir(self):
        return os.path.join(self._root, 'data', 'credentials')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test',
                        help='Test whether system path is correctly set up',
                        action='store_true',
                        default=False)

    args = parser.parse_args()
    if args.test:
        PathManager.test_path_setup()


