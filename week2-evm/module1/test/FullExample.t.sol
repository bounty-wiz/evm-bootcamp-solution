// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

import "forge-std/Test.sol";
import "../src/FullExample.sol";

contract FullExampleTest is Test {
    MainContract public main;
    TargetContract public target;

    function setUp() public {
        main = new MainContract();
        target = new TargetContract();

        // Fund the main contract with some ETH for payable calls
        // vm.deal(address(main), 10 ether);
        vm.deal(address(this), 10 ether);

        console.log("\n=== DELEGATECALL TEST ===");
        console.log("ADDRESSES:");
        console.log("  Test contract (this):", address(this));
        console.log("  MainContract:", address(main));
        console.log("  TargetContract:", address(target));
        console.log("");
    }

    function testInternalCall() public {
        console.log("\n=== INTERNAL CALL TEST ===");
        console.log("Before: main.myNumber =", main.myNumber());

        main.callInternal(42);

        console.log("After: main.myNumber =", main.myNumber());
        assertEq(main.myNumber(), 42);
    }

    function testExternalCall() public {
        console.log("\n=== EXTERNAL CALL (CALL) TEST ===");
        console.log("Before: target.storedNumber =", target.storedNumber());

        main.callStoreNumber(address(target), 100);

        console.log("After: target.storedNumber =", target.storedNumber());
        assertEq(target.storedNumber(), 100);
    }

    function testPayableCall() public {
        console.log("\n=== PAYABLE CALL TEST ===");
        console.log("Before: target balance =", address(target).balance);

        main.callDeposit{value: 1 ether}(address(target));

        console.log("After: target balance =", address(target).balance);
        assertEq(address(target).balance, 1 ether);
    }

    function testStaticCall() public {
        console.log("\n=== STATICCALL TEST ===");

        // First set a value
        target.storeNumber(777);
        console.log("target.storedNumber =", target.storedNumber());

        // Read using staticcall
        uint256 result = main.staticRead(address(target));
        console.log("Read via staticcall =", result);
        assertEq(result, 777);
    }

    function testDelegateCall() public {
        console.log("Before delegatecall:");
        console.log("  main.myNumber =", main.myNumber());
        console.log("  target.storedNumber =", target.storedNumber());

        // delegatecall executes target's code in main's context
        // So it will modify main.myNumber, NOT target.storedNumber!
        main.delegateStoreNumber(address(target), 999);

        console.log("After delegatecall:");
        console.log("  main.myNumber =", main.myNumber());
        console.log("  target.storedNumber =", target.storedNumber());

        // main.myNumber should change to 999
        assertEq(main.myNumber(), 999);
        // target.storedNumber should remain 0
        assertEq(target.storedNumber(), 0);
    }

    function testRevertBubbling() public {
        console.log("\n=== REVERT BUBBLING TEST ===");

        // This should revert with the message from target contract
        vm.expectRevert("TargetContract: failure");
        main.callFail(address(target));

        console.log("Revert was properly bubbled up!");
    }

    function testReceiveFunction() public {
        console.log("\n=== RECEIVE FUNCTION TEST ===");
        console.log("Before: main balance =", address(main).balance);

        // Send ETH with no calldata triggers receive()
        (bool success, ) = address(main).call{value: 0.5 ether}("");
        require(success, "ETH transfer failed");

        console.log("After: main balance =", address(main).balance);
        assertEq(address(main).balance, 0.5 ether);
    }

    function testFallbackFunction() public {
        console.log("\n=== FALLBACK FUNCTION TEST ===");

        // Call with data that doesn't match any function triggers fallback
        (bool success, ) = address(main).call{value: 0.1 ether}(
            abi.encodeWithSignature("nonExistentFunction()")
        );
        require(success, "fallback call failed");

        console.log("Fallback was triggered!");
    }
}
