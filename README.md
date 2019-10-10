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
-`is_state_variable()`:  Returns a boolean value of whether the current object instance is a local variable. 
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

A `Require` object has:  
* Attributes:  
* Functions:  

A `Require` object has:  
* Attributes:  
* Functions:  

A `Require` object has:  
* Attributes:  
* Functions:  
