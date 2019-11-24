pragma solidity ^0.5.11;
contract RequireExample {
    
    address public owner;
    
    constructor() public {
        owner = msg.sender;
    }
    
    uint public number = 0;
    bool public a = true;
    bool public b = true;
    bool public c = false;
    bool public d = true;

    modifier checka(){

        c = true;
        _;
        require(a);


    }

    function requireb() public{
        if (d){
            d = false;
        }


        require(b);
    }
    
    function test(uint _n, bool _b) checka public {
        require(msg.sender != address(0));
        requireb();
    }
    
}