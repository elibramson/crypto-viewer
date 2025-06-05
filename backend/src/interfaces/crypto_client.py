from abc import ABC, abstractmethod
from typing import Dict, List, Any

class CryptoClientInterface(ABC):
    @abstractmethod
    async def get_listing(self) -> List[Dict[str, Any]]:
        """Get list of all cryptocurrencies"""
        pass
    
    @abstractmethod
    async def get_currency_info(self, currency_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific cryptocurrency"""
        pass 