from static_analysis.core.select_solc_compiler import set_version
from static_analysis.core.contracts import Contracts

output = "**The following line must be modified with desired address to be used for contract deployment.\n" \
         "\taccount_used_for_deploying: 0x0000000000000000000000000000000000000000\n\n"
FYI = "**Please feel free to add/remove any representative values for each parameter.\n" \
      "**Account used for deployment is not automatically included.\n\n\n"
ignored_functions = ['constructor', 'slitherConstructorVariables', 'slitherConstructorConstantVariables']
accessible_functions = ['public', 'external']

def main(contract_dir, contract_name):
    set_version(contract_dir)
    contract = Contracts(contract_dir).get_contract_by_name(contract_name)
    contract.set_source_dir(contract_dir)
    contract.load_compiled_info()

    function_ipm = ""
    constructor = ""

    for f in contract.functions:
        pass

    output_path = f'./{contract_name}.ipm'


if __name__ == '__main__':
    c_name = "Ballot"
    c_dir = f'../samples/{c_name}.sol'
    main(c_dir, c_name)