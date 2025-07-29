#!/usr/bin/env python3
"""
Script to update contract configuration after deployment
Usage: python update_contract_config.py <contract_address>
"""
import sys
import os
import json
import re

def update_contract_config(contract_address):
    """Update all contract configuration files with the deployed contract address"""
    
    if not contract_address.startswith('0x') or len(contract_address) != 42:
        print("❌ Invalid contract address format")
        return False
    
    print(f"🔧 Updating contract configuration with address: {contract_address}")
    
    # 1. Update web3/config.py environment variable suggestion
    print("📝 Note: Set CONTRACT_ADDRESS environment variable or update web3/config.py")
    
    # 2. Update JavaScript contract config
    js_config_path = 'web/static/js/web3/contract-config.js'
    if os.path.exists(js_config_path):
        try:
            with open(js_config_path, 'r') as f:
                content = f.read()
            
            # Replace placeholder with actual address
            updated_content = content.replace('CONTRACT_ADDRESS_PLACEHOLDER', contract_address)
            
            with open(js_config_path, 'w') as f:
                f.write(updated_content)
            
            print(f"✅ Updated {js_config_path}")
        except Exception as e:
            print(f"❌ Failed to update {js_config_path}: {e}")
    
    # 3. Create/update .env file
    env_path = '.env'
    env_lines = []
    contract_line = f"CONTRACT_ADDRESS={contract_address}"
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('CONTRACT_ADDRESS='):
                lines[i] = contract_line + '\n'
                updated = True
            
        if not updated:
            lines.append(contract_line + '\n')
        
        env_lines = lines
    else:
        env_lines = [contract_line + '\n']
    
    try:
        with open(env_path, 'w') as f:
            f.writelines(env_lines)
        print(f"✅ Updated {env_path}")
    except Exception as e:
        print(f"❌ Failed to update {env_path}: {e}")
    
    # 4. Display next steps
    print("\n🎉 Contract configuration updated successfully!")
    print("\n📋 Next steps:")
    print("1. Restart your Flask application: python web_app.py")
    print("2. Test wallet connection and NFT minting")
    print("3. Verify contract on block explorer if desired")
    print(f"4. View contract at: https://www.oklink.com/amoy/address/{contract_address}")
    
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_contract_config.py <contract_address>")
        print("Example: python update_contract_config.py 0x1234567890abcdef1234567890abcdef12345678")
        sys.exit(1)
    
    contract_address = sys.argv[1].strip()
    success = update_contract_config(contract_address)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()