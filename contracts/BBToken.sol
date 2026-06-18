// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BBToken is ERC20, Ownable {
    // Toplam arz ve diğer ayarlar için gerekirse düzenlenebilir.
    // Herkesin claim() fonksiyonuyla token alabilmesi için basit bir mekanizma.
    
    constructor() ERC20("Base Bridge Token", "BB") Ownable(msg.sender) {
        _mint(msg.sender, 1_000_000 * 10**decimals());
    }

    /**
     * @dev Herkesin veya oyunun kontrat üzerinden token claim edebilmesini sağlar.
     */
    function claim(uint256 amount) public {
        _mint(msg.sender, amount);
    }

    /**
     * @dev Gerekirse sahibinin mint etmesi için
     */
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
