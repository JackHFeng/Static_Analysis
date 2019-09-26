from slither import Slither
import globals
from utils import *


def main():
    contract_dir = '/Users/jackfeng/Dropbox/Dropbox/CTFuzz/CTFuzz/ContractStudyCases/DocumentationExamples/Ballot.sol'
    globals.slither = Slither(contract_dir)

    createContract()


if __name__ == '__main__':
    main()