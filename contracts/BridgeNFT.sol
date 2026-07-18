// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BridgeNFT is ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    event NFTMinted(address indexed player, uint256 indexed tokenId, string nftName);

    constructor() ERC721("Bridge Achievement NFT", "BANFT") Ownable(msg.sender) {}

    /**
     * @dev Mints a new achievement NFT to the player.
     * @param nftName The name of the achievement or NFT to store onchain or metadata.
     */
    function mint(string memory nftName) public {
        uint256 tokenId = _nextTokenId;
        _nextTokenId++;

        _safeMint(msg.sender, tokenId);
        
        // Basit bir örnek olarak isim verisini tokenURI veya event ile zincire işliyoruz.
        _setTokenURI(tokenId, string(abi.encodePacked("data:application/json;utf8,{\"name\":\"", nftName, "\",\"description\":\"Stick Bridge Game Achievement\"}")));

        emit NFTMinted(msg.sender, tokenId, nftName);
    }
}
