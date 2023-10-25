from argparse import ArgumentParser, Namespace
from src.updater import Updater
from typing import List
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    
    parser: ArgumentParser = ArgumentParser(description='Attempts to find the updated globals, the more signatures that you use the longer it will take.',)
    parser.add_argument('old', type=str, help='The old script file to read from (this is the file that will be used to generate the signatures)')
    parser.add_argument('new', type=str, help='The new script file to read from (file to search for signatures in)')
    parser.add_argument('globals', type=str, help='The file to read the globals from')
    parser.add_argument('--signatures', '-s', type=int, help='The amount of signatures that will be used (lower this value if -u flag is present)', default=20)
    parser.add_argument('--unique', '-u', type=bool, choices=[True, False], help='Whether or not to check if the signature is unique (this will slow down the process)', default=False)
    parser.add_argument('--padding', '-p', type=int, help='The amount of padding to use when creating signatures (changes to this may increase or decrease accuracy of output)', default=32)

    args: Namespace = parser.parse_args()
    updater: Updater = Updater(args.new, args.old)
    globals: List[str] = updater.load_globals(args.globals)
    updater.search(args.globals, args.padding, args.signatures, args.unique)