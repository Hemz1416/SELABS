"""Inventory Management System Module.

This module provides clean, secure, and robust management of stock data,
including adding, removing, loading, saving, and reporting on inventory items
with full validation and defensive resource management.
"""

import ast
from datetime import datetime
import json
import logging
from typing import Any, Dict, List, Optional

# Structured logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class InventoryManager:
    """Manages store inventory stock items and transaction logs."""

    def __init__(self) -> None:
        """Initialize empty stock dictionary and transaction log."""
        self.stock_data: Dict[str, int] = {}
        self.transaction_logs: List[str] = []

    def add_item(
        self,
        item: str = "default",
        qty: int = 0,
        logs: Optional[List[str]] = None,
    ) -> None:
        """Add an item quantity to stock and log transaction."""
        if not item:
            logger.warning("Attempted to add empty item name.")
            return

        if logs is None:
            logs = self.transaction_logs

        self.stock_data[item] = self.stock_data.get(item, 0) + max(0, qty)
        timestamp = datetime.now().isoformat()
        logs.append(f"{timestamp}: Added {qty} of {item}")
        logger.info("Added %d units of '%s' to stock.", qty, item)

    def remove_item(self, item: str, qty: int) -> bool:
        """Safely deduct quantity from stock."""
        try:
            if item in self.stock_data:
                self.stock_data[item] -= qty
                if self.stock_data[item] <= 0:
                    del self.stock_data[item]
                logger.info("Removed %d units of '%s'.", qty, item)
                return True
            logger.warning("Item '%s' not present in stock.", item)
            return False
        except (KeyError, TypeError) as err:
            logger.error("Error removing item '%s': %s", item, err)
            return False

    def get_qty(self, item: str) -> int:
        """Retrieve current in-stock quantity for specified item."""
        return self.stock_data.get(item, 0)

    def load_stock(self, filepath: str = "stock.json") -> None:
        """Load inventory records from JSON file using context manager."""
        try:
            with open(filepath, "r", encoding="utf-8") as file_in:
                loaded_data = json.load(file_in)
                if isinstance(loaded_data, dict):
                    self.stock_data = {
                        str(k): int(v) for k, v in loaded_data.items()
                    }
                    logger.info(
                        "Successfully loaded stock from '%s'.", filepath
                    )
        except (FileNotFoundError, json.JSONDecodeError, OSError) as err:
            logger.warning("Could not load stock from '%s': %s", filepath, err)

    def save_stock(self, filepath: str = "stock.json") -> None:
        """Serialize current stock to JSON file."""
        try:
            with open(filepath, "w", encoding="utf-8") as file_out:
                json.dump(self.stock_data, file_out, indent=2)
            logger.info("Saved stock to '%s'.", filepath)
        except OSError as err:
            logger.error("Failed to write stock to '%s': %s", filepath, err)

    def calculate_total(self) -> int:
        """Sum total units across all stock items."""
        return sum(self.stock_data.values())

    @staticmethod
    def execute_command(cmd: str) -> Any:
        """Safely parse literals without arbitrary code execution."""
        try:
            # Replaced dangerous eval with ast.literal_eval
            result = ast.literal_eval(cmd)
            logger.info("Safely evaluated command literal.")
            return result
        except (ValueError, SyntaxError) as err:
            logger.info(
                "Command '%s' treated as safe string expression (%s).",
                cmd,
                err,
            )
            return cmd


# Global instance and legacy alias functions for compatibility
_GLOBAL_INVENTORY = InventoryManager()
stock_data = _GLOBAL_INVENTORY.stock_data


def add_item(
    item: str = "default",
    qty: int = 0,
    logs: Optional[List[str]] = None,
) -> None:
    """Module-level add item function."""
    _GLOBAL_INVENTORY.add_item(item, qty, logs)


def addItem(  # pylint: disable=C0103
    item: str = "default",
    qty: int = 0,
    logs: Optional[List[str]] = None,
) -> None:
    """Legacy camelCase alias for add_item."""
    add_item(item, qty, logs)


def remove_item(item: str, qty: int) -> bool:
    """Module-level remove item function."""
    return _GLOBAL_INVENTORY.remove_item(item, qty)


def removeItem(item: str, qty: int) -> bool:  # pylint: disable=C0103
    """Legacy camelCase alias for remove_item."""
    return remove_item(item, qty)


def get_qty(item: str) -> int:
    """Module-level get quantity function."""
    return _GLOBAL_INVENTORY.get_qty(item)


def getQty(item: str) -> int:  # pylint: disable=C0103
    """Legacy camelCase alias for get_qty."""
    return get_qty(item)


def load_stock(file: str = "stock.json") -> None:
    """Module-level load stock function."""
    _GLOBAL_INVENTORY.load_stock(file)


def loadStock(file: str = "stock.json") -> None:  # pylint: disable=C0103
    """Legacy camelCase alias for load_stock."""
    load_stock(file)


def save_stock(file: str = "stock.json") -> None:
    """Module-level save stock function."""
    _GLOBAL_INVENTORY.save_stock(file)


def saveStock(file: str = "stock.json") -> None:  # pylint: disable=C0103
    """Legacy camelCase alias for save_stock."""
    save_stock(file)


def calculate_total() -> int:
    """Module-level calculate total function."""
    return _GLOBAL_INVENTORY.calculate_total()


def calculateTotal() -> int:  # pylint: disable=C0103
    """Legacy camelCase alias for calculate_total."""
    return calculate_total()


def execute_command(cmd: str) -> Any:
    """Module-level execute command function."""
    return InventoryManager.execute_command(cmd)


def main() -> None:
    """Demonstrate inventory operations cleanly."""
    add_item("Apple", 10)
    add_item("Banana", 20)
    remove_item("Apple", 5)
    total = calculate_total()
    print(f"Total items in stock: {total}")
    save_stock()
    load_stock()
    eval_result = execute_command("[1, 2, 3]")
    print(f"Evaluated literal safely: {eval_result}")


if __name__ == "__main__":
    main()
