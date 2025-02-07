from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import pickle
from pathlib import Path


@dataclass
class CoinInfo:
    date: str
    denomination: str
    variety: str = ""
    designation: str = ""

    def __str__(self) -> str:
        base = f"{self.date} {self.denomination}"
        if self.variety:
            base += f" {self.variety}"
        if self.designation:
            base += f" {self.designation}"
        return base.strip()

class PCGSRegistry:
    def __init__(self):
        self.number_to_coin: Dict[int, CoinInfo] = {}
        self.coin_to_number: Dict[str, int] = {}
    
    def get_coin_info(self, pcgs_number: int) -> Optional[CoinInfo]:
        """Look up coin information by PCGS number."""
        return self.number_to_coin.get(pcgs_number)
    
    def search_coins(self, date: str = "", denomination: str = "", variety: str = "", designation: str = "") -> List[Tuple[int, CoinInfo]]:
        """Search for coins matching the given criteria."""
        results = []
        for pcgs_number, coin in self.number_to_coin.items():
            if date and date not in coin.date:
                continue
            if denomination and denomination.lower() not in coin.denomination.lower():
                continue
            if variety and variety.lower() not in coin.variety.lower():
                continue
            if designation and designation.lower() not in coin.designation.lower():
                continue
            results.append((pcgs_number, coin))
        return results

def main():
    registry = PCGSRegistry()
    
    # Load from cache file in the same directory as this script
    cache_path = Path(__file__).parent / 'pcgs_registry_cache.pkl'
    with open(cache_path, 'rb') as f:
        registry.number_to_coin, registry.coin_to_number, _ = pickle.load(f)
    print("Loaded from cache successfully!")
    
    # Test direct PCGS number lookup
    print("\nTesting direct PCGS number lookup:")
    coin = registry.get_coin_info(14018)
    if coin:
        print(f"Found coin: {coin}")
    else:
        print("Coin not found")
        
    # Test reverse lookup by coin details
    print("\nTesting reverse lookup by coin details:")
    matches = registry.search_coins(date="1926", denomination="25C")
    if matches:
        print(f"Found {len(matches)} matching coins:")
        for pcgs_number, coin in matches:
            print(f"PCGS# {pcgs_number}: {coin}")
    else:
        print("No matches found")

    # # Write to output file
    # output_path = Path(__file__).parent / 'pcgs_registry_output.txt'
    # with open(output_path, 'w') as f:
    #     f.write("PCGS Registry Contents:\n")
    #     f.write("-" * 50 + "\n\n")
    #     for pcgs_number in sorted(registry.number_to_coin.keys()):
    #         coin = registry.number_to_coin[pcgs_number]
    #         f.write(f"PCGS# {pcgs_number}: {coin}\n")
    #     f.write(f"\nTotal entries: {len(registry.number_to_coin)}")
    
    # print(f"Registry contents written to {output_path}")
    

if __name__ == "__main__":
    main()
