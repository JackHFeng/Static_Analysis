pragma solidity 0.5.11;
contract Example{
    uint public a_uint = 0;
    bool public a_bool = false;
    function example1(uint a, uint b) external{
        require(a < b);
        uint c = a + b;
    }
    
    function example2(uint a, uint b) external{
        require(a < 10);
        uint c = a + b;
    }
    
    function example3(uint a, uint b) external{
        require(a + b < 10);
        uint c = a + b;
    }
}