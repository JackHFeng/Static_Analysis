A `DDGs` (Data Dependency Graphs) object has:  
* Attributes:  
-`contracts (dict(Contract))`: A dictionary of contract objects, with their name as key value.  
* Functions:  
-`__init__(dir: str)`: This is the constructor interface, this creates a DDGs object from the solidity contract directory.  
-`get_contract_by_name(name: str)`: Returns a contract object from its name.  
    
A `Contract` object has:  
* Attributes:  
-`name (str)`: Name of the smart contract.  
-`functions (dict(Function))`: A dictionary of function objects, with their name as key value.  
-`state_variables (dict(StateVariable))`: A dictionary of state variable objects, with their name as key value.  
-`modifiers (dict(Modifiers))`: A dictionary of modifier objects, with their name as key value.  
* Functions:  
-`get_function_by_name(name: str)`: Returns a function object from its name.  
-`get_modifier_by_name(name: str)`: Returns a modifier object from its name.  
-`get_state_variable_by_name(name: str)`: Returns a state variable object from its name.  
 
A `Function` object has:  
* Attributes:  
-`name (str)`: Name of the function.  
-`signature (str)`: Signature of the function.  
-`visibility (str)`: Visibility of the function.  
-`from_contract (Contract)`: The contract object where the current function is from.  
-`modifiers (list(Modifier))`: A list of modifiers used in the current function.  
-`requires (list(Require))`: A list of requires appeared in the current function, including requires appeared in the modifiers.  
-`parameters (list(Variable))`: A list of parameters for the current function.  
-`state_variables_read (list(StateVariable))`: A list of state variables read by the current function, including the ones read by the modifiers.  
-`state_variables_written (list(StateVariable))`: A list of state variables written by the current function, including the ones written by the modifiers.   
-`local_variables_read (list(Variable))`: A list of local variables read by the current function.  
-`local_variables_written (list(Variable))`: A list of local variables written by the current function.  
* Functions:  
None at the moment, let me know if you need any.  

A `Modifier` object has:
* Attributes:  
Modifier inherits Function class. So they are only slightly different in what attributes they have.  
Modifier DOES NOT have the `modifiers (list(Modifier))` attribute from Function class.  
In addition to attributes exists in Function, Modifier also have `functions_used (list(Functions))` attribute.  
-`functions_used (list(Functions))`: A list of functions that uses the current modifier. 
* Functions: 
None at the moment, let me know if you need any.  

A `Variable` (local variable) object has:  
* Attributes:  
-`name (str)`: Name of the variable.  
-`type (slither.core.solidity_types.*)`: Data type of the variable, using str(type) can get the string value of the data type. 
* Functions:  
-`is_state_variable()`:  Returns a boolean value of whether the current object instance is a state variable.  
-`is_local_variable()`:  Returns a boolean value of whether the current object instance is a local variable. 
None at the moment, let me know if you need any.  

A `StateVariable` object has:  
* Attributes:  
StateVariable inherits Variable class. In addition to attributes exists in Variable, StateVariable also have:  
-`visibility (str)`: Visibility of the state variable.  
-`functions_read (list(Function))`: A list of functions that read the current state variable.  
-`functions_written (list(Function))`: A list of functions that write the current state variable.  
-`modifiers_read (list(Modifier))`: A list of modifiers that read the current state variable.  
-`modifiers_written (list(Modifier))`: A list of modifiers that write the current state variable.  
-`requires_read (list(Require))`: A list of requires that read the current state variable.  
* Functions:  
Same as Variable due to inheritance.  

A `Require` object has:
* Attributes:  
-`code (str)`: The line of code of the require statement.  
-`from_function (Function / Modifier)`: The function or modifier object where the current require is from.  
-`IRs (list(slither.slithir.operations.*))`: A list of intermediate representations for the requrie statement given by slither.    
-`state_variables_read (list(StateVariable))`: A list of state variables read by the current require.  
-`local_variables_read (list(Variable))`: A list of local variables read by the current require.  
-`operation (list(slither.core.expressions.binary_operation.BinaryOperation / slither.core.expressions.identifier.Identifier))`: The AST expression of the boolean evaluation within the require statement. 
The `slither.core.expressions.binary_operation.BinaryOperation` type is a binary expression that evaluates to a boolean value. The `slither.core.expressions.identifier.Identifier` type is a boolean variable literal.
* Functions:  
None at the moment, let me know if you need any.  

A `slither.core.expressions.binary_operation.BinaryOperation` object has:  
* Attributes:  
-`expressions (list(slither.core.expressions.*))`: A list of length equals to 2. Index 0 contains the left expression, index 1 contains the right expression.  
-`expression_left (slither.core.expressions.*)`: The left expression of the current operation.  
-`expression_right (slither.core.expressions.*)`: The left expression of the current operation.  
-`type (slither.core.expressions.binary_operation.BinaryOperationType)`: A type object representing the current binary operation.  
-`type_str (str)`: The string representation of the current binary operation. (e.g. '+', '-', '>', etc.)  
* Function:  
None at the moment, let me know if you need any.  

A `slither.core.expressions.unary_operation.UnaryOperation` object has:  
* Attributes:  
-`expression (slither.core.expressions.expression.Expression)`: Contains the expression of the current unary operation.  
-`type (slither.core.expressions.unary_operation.UnaryOperationType)`: A type object representing the current unary operation.  
-`type_str (str)`: The string representation of the current unary operation. (e.g. '!', '-', '~', etc.)  
* Function:  
None at the moment, let me know if you need any.  

A `slither.core.expressions.identifier.Identifier` object has:  
* Attributes:  
-`value (slither.solc_parsing.variables.state_variable.StateVariableSolc / slither.solc_parsing.variables.local_variable.LocalVariableSolc / slither.core.declarations.solidity_variables.SolidityVariableComposed)`: Returns the object of the variable, the object can be either a state variable, local variable or a Solidity Variable(e.g. msg.sender, msg.value, etc). All object return by this attribute also have the attribute `name`, you can use the `name ` attribute to get the name of the variable. 


Example:
```
from core.data_dependency_graph import DDGs


def main():
    contract_dir = './Ballot.sol'
    data_dependency_graphs = DDGs(contract_dir)
    contract = data_dependency_graphs.get_contract_by_name('Ballot')
    print(contract)


if __name__ == '__main__':
    main()

```
