const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying PortfolioMandala contract to Polygon Amoy testnet...");

  // Get the contract factory
  const PortfolioMandala = await ethers.getContractFactory("PortfolioMandala");

  // Contract parameters
  const name = "Portfolio Mandala";
  const symbol = "PMANDALA";
  const baseTokenURI = "http://localhost:5000/api/nft/metadata/"; // Update with your domain
  const contractURI = "http://localhost:5000/api/nft/contract-metadata"; // Update with your domain

  // Deploy the contract
  const portfolioMandala = await PortfolioMandala.deploy(
    name,
    symbol,
    baseTokenURI,
    contractURI
  );

  await portfolioMandala.waitForDeployment();

  const contractAddress = await portfolioMandala.getAddress();
  
  console.log("PortfolioMandala deployed to:", contractAddress);
  console.log("Network: Polygon Amoy (Chain ID: 80002)");
  console.log("Block Explorer: https://www.oklink.com/amoy/address/" + contractAddress);
  
  // Save deployment info
  const deploymentInfo = {
    network: "amoy",
    chainId: 80002,
    contractAddress: contractAddress,
    name: name,
    symbol: symbol,
    baseTokenURI: baseTokenURI,
    contractURI: contractURI,
    deployedAt: new Date().toISOString(),
    blockExplorer: `https://www.oklink.com/amoy/address/${contractAddress}`
  };

  console.log("\nDeployment Info:");
  console.log(JSON.stringify(deploymentInfo, null, 2));

  // Wait for a few block confirmations
  console.log("\nWaiting for block confirmations...");
  await portfolioMandala.deploymentTransaction().wait(5);
  
  console.log("Contract deployed and confirmed!");
  
  return contractAddress;
}

main()
  .then((contractAddress) => {
    console.log(`\n✅ Deployment successful!`);
    console.log(`Contract Address: ${contractAddress}`);
    console.log(`\nNext steps:`);
    console.log(`1. Update your backend with the contract address`);
    console.log(`2. Update the baseTokenURI to point to your API`);
    console.log(`3. Fund the contract if needed`);
    process.exit(0);
  })
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });