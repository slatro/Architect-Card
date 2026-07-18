require('dotenv').config();
const fs = require('fs');
const path = require('path');
const solc = require('solc');
const { ethers } = require('ethers');

// Helper to resolve OpenZeppelin imports
function findImports(importPath) {
    if (importPath.startsWith('@openzeppelin/')) {
        const fullPath = path.resolve(__dirname, '..', 'node_modules', importPath);
        return { contents: fs.readFileSync(fullPath, 'utf8') };
    }
    return { error: 'File not found' };
}

async function main() {
    console.log("Compiling contracts...");

    const contractNames = ['BBToken', 'BridgeNFT', 'LeaderboardReferral'];
    const sources = {};

    for (const name of contractNames) {
        const filePath = path.resolve(__dirname, '..', 'contracts', `${name}.sol`);
        sources[`${name}.sol`] = {
            content: fs.readFileSync(filePath, 'utf8')
        };
    }

    const input = {
        language: 'Solidity',
        sources: sources,
        settings: {
            outputSelection: {
                '*': {
                    '*': ['abi', 'evm.bytecode']
                }
            },
            optimizer: {
                enabled: true,
                runs: 200
            }
        }
    };

    const output = JSON.parse(solc.compile(JSON.stringify(input), { import: findImports }));

    if (output.errors) {
        let hasError = false;
        output.errors.forEach(err => {
            console.error(err.formattedMessage);
            if (err.severity === 'error') hasError = true;
        });
        if (hasError) throw new Error("Compilation failed.");
    }

    console.log("Compilation successful!");

    // Set up provider & signer for Base Mainnet (Chain ID 8453)
    const provider = new ethers.JsonRpcProvider("https://mainnet.base.org");
    const privateKey = process.env.PRIVATE_KEY;
    if (!privateKey) throw new Error("PRIVATE_KEY not found in env!");
    
    const wallet = new ethers.Wallet(privateKey, provider);
    const deployerAddress = await wallet.getAddress();
    const balance = await provider.getBalance(deployerAddress);
    console.log(`Deploying from address: ${deployerAddress}`);
    console.log(`Account balance: ${ethers.formatEther(balance)} ETH`);

    // Deploy BBToken
    const bbTokenData = output.contracts['BBToken.sol']['BBToken'];
    const bbTokenFactory = new ethers.ContractFactory(bbTokenData.abi, bbTokenData.evm.bytecode.object, wallet);
    console.log("Deploying BBToken...");
    const bbToken = await bbTokenFactory.deploy();
    await bbToken.waitForDeployment();
    const bbTokenAddress = await bbToken.getAddress();
    console.log(`BBToken deployed to: ${bbTokenAddress}`);

    // Deploy BridgeNFT
    const bridgeNftData = output.contracts['BridgeNFT.sol']['BridgeNFT'];
    const bridgeNftFactory = new ethers.ContractFactory(bridgeNftData.abi, bridgeNftData.evm.bytecode.object, wallet);
    console.log("Deploying BridgeNFT...");
    const bridgeNft = await bridgeNftFactory.deploy();
    await bridgeNft.waitForDeployment();
    const bridgeNftAddress = await bridgeNft.getAddress();
    console.log(`BridgeNFT deployed to: ${bridgeNftAddress}`);

    // Deploy LeaderboardReferral
    const lrData = output.contracts['LeaderboardReferral.sol']['LeaderboardReferral'];
    const lrFactory = new ethers.ContractFactory(lrData.abi, lrData.evm.bytecode.object, wallet);
    console.log("Deploying LeaderboardReferral...");
    const leaderboardReferral = await lrFactory.deploy();
    await leaderboardReferral.waitForDeployment();
    const leaderboardReferralAddress = await leaderboardReferral.getAddress();
    console.log(`LeaderboardReferral deployed to: ${leaderboardReferralAddress}`);

    console.log("\nUpdating web3.js with new addresses...");
    let web3Content = fs.readFileSync(path.resolve(__dirname, '..', 'js', 'web3.js'), 'utf8');

    // Replace the dummy addresses
    web3Content = web3Content.replace(
        /const BB_TOKEN_ADDRESS = "[^"]+";/,
        `const BB_TOKEN_ADDRESS = "${bbTokenAddress}";`
    );
    web3Content = web3Content.replace(
        /const NFT_CONTRACT_ADDRESS = "[^"]+";/,
        `const NFT_CONTRACT_ADDRESS = "${bridgeNftAddress}";`
    );
    web3Content = web3Content.replace(
        /const LEADERBOARD_CONTRACT_ADDRESS = "[^"]+";/,
        `const LEADERBOARD_CONTRACT_ADDRESS = "${leaderboardReferralAddress}";`
    );

    fs.writeFileSync(path.resolve(__dirname, '..', 'js', 'web3.js'), web3Content, 'utf8');
    console.log("web3.js successfully updated!");
}

main().catch(err => {
    console.error("Deployment failed:", err);
    process.exit(1);
});
