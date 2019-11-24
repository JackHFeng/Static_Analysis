pragma solidity 0.5.11;
contract Example{
    uint public state_a = 100;

    function example1(uint a, uint b) public returns (uint){
        require(a == b);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example2(uint a, uint b) public returns (uint){
        require(a != b);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example3(uint a, uint b) public returns (uint){
        require(a > b);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }


    function example4(uint a, uint b) public returns (uint){
        require(a < b);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example5(uint a, uint b) public returns (uint){
        require(a >= b);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example6(uint a, uint b) public returns (uint){
        require(a <= b);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example7(bool a, bool b) public returns (uint){
        require(a && b);
        uint a = 1;
        uint b = 1;
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example8(bool a, bool b) public returns (uint){
        require(a || b);
        uint a = 1;
        uint b = 1;
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }


    function example9(bool a) public returns (uint){
        require(!a);
        uint a = 1;
        uint b = 1;
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example10(bool a) public returns (uint){
        require(a);
        uint a = 1;
        uint b = 1;
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example11(uint a, uint b) public returns (uint){
        require(state_a > a);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

    function example12(uint a, uint b) public returns (uint){
        require(state_a > a + b);
        uint c = a + b;
        uint d = c + c * 2;
        uint e = d + d * 2;
        uint f = e + e * 2;
        uint g = f + f * 2;
        uint h = g + g * 2;
        uint i = h + h * 2;
        uint j = i + i * 2;
        uint k = j + j * 2;
        uint l = k + k * 2;
        uint m = l + l * 2;
        uint n = m + m * 2;
        return n;
    }

}