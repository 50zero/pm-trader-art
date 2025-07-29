// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Base64.sol";

/**
 * @title PortfolioMandala
 * @dev NFT contract for Polymarket Portfolio Mandala visualizations
 * Each trader can mint only one NFT representing their portfolio mandala
 */
contract PortfolioMandala is ERC721, ERC721URIStorage, Ownable {
    using Strings for uint256;

    // Counter for token IDs
    uint256 private _tokenIdCounter;
    
    // Mapping from trader address to token ID (each trader can only have one NFT)
    mapping(address => uint256) public traderToTokenId;
    
    // Mapping to check if a trader has minted an NFT
    mapping(address => bool) public hasMinted;
    
    // Base URI for metadata
    string private _baseTokenURI;
    
    // Contract metadata
    string public contractURI;
    
    // Events
    event MandalaCreated(address indexed trader, uint256 indexed tokenId, string metadataURI);
    
    constructor(
        string memory name,
        string memory symbol,
        string memory baseTokenURI,
        string memory _contractURI
    ) ERC721(name, symbol) Ownable(msg.sender) {
        _baseTokenURI = baseTokenURI;
        contractURI = _contractURI;
        _tokenIdCounter = 1; // Start from token ID 1
    }
    
    /**
     * @dev Mint a mandala NFT for the caller's address
     * Only the trader themselves can mint their mandala
     * Each trader can only mint one NFT
     */
    function mintMandala() external {
        address trader = msg.sender;
        
        require(!hasMinted[trader], "Trader has already minted their mandala");
        
        uint256 tokenId = _tokenIdCounter++;
        
        // Mint the NFT to the trader
        _safeMint(trader, tokenId);
        
        // Set the token URI pointing to our API
        string memory tokenMetadataURI = string(abi.encodePacked(_baseTokenURI, tokenId.toString()));
        _setTokenURI(tokenId, tokenMetadataURI);
        
        // Update mappings
        traderToTokenId[trader] = tokenId;
        hasMinted[trader] = true;
        
        emit MandalaCreated(trader, tokenId, tokenMetadataURI);
    }
    
    /**
     * @dev Check if a trader has already minted their NFT
     */
    function hasTraderMinted(address trader) external view returns (bool) {
        return hasMinted[trader];
    }
    
    /**
     * @dev Get the token ID for a specific trader
     */
    function getTraderTokenId(address trader) external view returns (uint256) {
        require(hasMinted[trader], "Trader has not minted an NFT");
        return traderToTokenId[trader];
    }
    
    /**
     * @dev Get the trader address for a specific token ID
     */
    function getTokenTrader(uint256 tokenId) external view returns (address) {
        return ownerOf(tokenId);
    }
    
    /**
     * @dev Get total number of minted tokens
     */
    function totalSupply() external view returns (uint256) {
        return _tokenIdCounter - 1;
    }
    
    /**
     * @dev Set the base URI for token metadata (only owner)
     */
    function setBaseURI(string memory baseTokenURI) external onlyOwner {
        _baseTokenURI = baseTokenURI;
    }
    
    /**
     * @dev Set contract metadata URI (only owner)
     */
    function setContractURI(string memory _contractURI) external onlyOwner {
        contractURI = _contractURI;
    }
    
    /**
     * @dev Get the base URI
     */
    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }
    
    /**
     * @dev Override required by Solidity for ERC721URIStorage
     */
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
    
    /**
     * @dev Override required by Solidity for ERC721URIStorage
     */
    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721URIStorage) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
    
    /**
     * @dev Emergency pause function (only owner)
     * Prevents minting in case of issues
     */
    bool public mintingPaused = false;
    
    function pauseMinting() external onlyOwner {
        mintingPaused = true;
    }
    
    function unpauseMinting() external onlyOwner {
        mintingPaused = false;
    }
    
    modifier whenNotPaused() {
        require(!mintingPaused, "Minting is currently paused");
        _;
    }
    
    /**
     * @dev Update mintMandala to include pause check
     */
    function mintMandalaChecked() external whenNotPaused {
        address trader = msg.sender;
        
        require(!hasMinted[trader], "Trader has already minted their mandala");
        
        uint256 tokenId = _tokenIdCounter++;
        
        // Mint the NFT to the trader
        _safeMint(trader, tokenId);
        
        // Set the token URI pointing to our API
        string memory tokenMetadataURI = string(abi.encodePacked(_baseTokenURI, tokenId.toString()));
        _setTokenURI(tokenId, tokenMetadataURI);
        
        // Update mappings
        traderToTokenId[trader] = tokenId;
        hasMinted[trader] = true;
        
        emit MandalaCreated(trader, tokenId, tokenMetadataURI);
    }
}