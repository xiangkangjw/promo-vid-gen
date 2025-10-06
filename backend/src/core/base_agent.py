from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    Base class for all agents in the AI Promo Creator system
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        logger.info(f"Initialized {self.name} agent")
    
    @abstractmethod
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's main functionality
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Dict containing the agent's output
        """
        pass
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> None:
        """
        Validate that required fields are present in input data
        
        Args:
            input_data: Input data to validate
            required_fields: List of required field names
            
        Raises:
            ValueError: If required fields are missing
        """
        missing_fields = [field for field in required_fields if field not in input_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
    
    def log_progress(self, message: str, level: str = "info") -> None:
        """
        Log progress messages
        
        Args:
            message: Message to log
            level: Logging level (info, warning, error)
        """
        log_func = getattr(logger, level, logger.info)
        log_func(f"[{self.name}] {message}")