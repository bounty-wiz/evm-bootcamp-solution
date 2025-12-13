// // SPDX-License-Identifier: MIT
// pragma solidity 0.8.13;

// contract TargetContract {
//     uint256 public storedNumber;

//     event Received(address sender, uint256 amount);
//     event Stored(uint256 number);

//     // Payable function that accepts ETH
//     function deposit() external payable {
//         emit Received(msg.sender, msg.value);
//     }

//     // Store a number (state-changing)
//     function storeNumber(uint256 num) external {
//         storedNumber = num;
//         emit Stored(num);
//     }

//     // View function used for staticcall testing
//     function readNumber() external view returns (uint256) {
//         return storedNumber;
//     }

//     // Function that always reverts
//     function fail() external pure {
//         revert("TargetContract: failure");
//     }
// }

// contract MainContract {
//     event Log(string message, bytes data);
//     event Received(address sender, uint256 amount);

//     uint256 public myNumber;

//     // ===== RECEIVE FUNCTION =====
//     receive() external payable {
//         emit Received(msg.sender, msg.value);
//     }

//     // ===== FALLBACK FUNCTION =====
//     fallback() external payable {
//         emit Log("fallback triggered", msg.data);
//     }

//     // ===== INTERNAL CALL =====
//     function _setInternal(uint256 x) internal {
//         myNumber = x;
//     }

//     function callInternal(uint256 x) external {
//         _setInternal(x);
//         emit Log("internal call executed", "");
//     }

//     // ===== EXTERNAL CALL (CALL) =====
//     function callStoreNumber(address target, uint256 x) external {
//         (bool ok, bytes memory data) =
//             target.call(abi.encodeWithSignature("storeNumber(uint256)", x));

//         if (!ok) revert("callStoreNumber failed");
//         emit Log("CALL storeNumber()", data);
//     }

//     // ===== PAYABLE CALL =====
//     function callDeposit(address target) external payable {
//         (bool ok, ) = target.call{value: msg.value}(
//             abi.encodeWithSignature("deposit()")
//         );
//         require(ok, "deposit via call failed");
//     }

//     // ===== STATICCALL =====
//     function staticRead(address target) external view returns (uint256) {
//         (bool ok, bytes memory data) =
//             target.staticcall(abi.encodeWithSignature("readNumber()"));

//         require(ok, "staticcall failed");
//         return abi.decode(data, (uint256));
//     }

//     // ===== DELEGATECALL =====
//     function delegateStoreNumber(address target, uint256 x) external {
//         (bool ok, ) =
//             target.delegatecall(abi.encodeWithSignature("storeNumber(uint256)", x));

//         require(ok, "delegatecall failed");
//         // Notice: storedNumber in target != affected
//         // myNumber in THIS CONTRACT *changes* instead.
//     }

//     // ===== REVERT BUBBLING =====
//     function callFail(address target) external {
//         (bool ok, bytes memory data) =
//             target.call(abi.encodeWithSignature("fail()"));

//         if (!ok) {
//             // bubble up the revert reason
//             assembly {
//                 revert(add(data, 32), mload(data))
//             }
//         }
//     }
// }