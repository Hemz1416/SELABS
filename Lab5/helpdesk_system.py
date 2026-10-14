"""IT Helpdesk Ticket Allocation System.

This module provides functionalities to raise, assign, inspect, and manage
IT helpdesk tickets, ensuring data integrity, strict input validation,
and secure file and process management.
"""

from datetime import datetime
import json
import logging
import os
import re
import subprocess  # nosec B404
from typing import Any, Dict, List, Optional

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Default administrator credentials retrieved from environment
ADMIN_TOKEN = os.environ.get("HELPDESK_ADMIN_TOKEN", "helpdesk@123")


class HelpdeskSystem:
    """Encapsulates helpdesk tickets, state, and operations."""

    def __init__(self) -> None:
        """Initialize the ticketing database and audit log."""
        self.tickets: Dict[int, Dict[str, Any]] = {}
        self.ticket_counter: int = 100
        self.audit_log: List[str] = []

    def raise_ticket(
        self,
        user: str,
        issue_type: str,
        urgency: str = "3",
        audit_trail: Optional[List[str]] = None,
    ) -> int:
        """Raise a new ticket with validated urgency level."""
        if audit_trail is None:
            audit_trail = self.audit_log

        # Validate urgency input
        try:
            priority = int(urgency)
            if not 1 <= priority <= 5:
                logger.warning(
                    "Invalid urgency '%s' outside range 1-5; defaulting to 3.",
                    urgency,
                )
                priority = 3
        except (ValueError, TypeError):
            logger.warning(
                "Non-numeric urgency '%s'; defaulting to 3.", urgency
            )
            priority = 3

        self.ticket_counter += 1
        ticket_id = self.ticket_counter

        self.tickets[ticket_id] = {
            "user": user.strip(),
            "issue": issue_type.strip(),
            "priority": priority,
            "tech": None,
            "notes": [],
        }

        timestamp = datetime.now().isoformat()
        log_entry = f"{user} raised #{ticket_id} at {timestamp}"
        audit_trail.append(log_entry)
        logger.info("Created ticket #%d for user '%s'", ticket_id, user)
        return ticket_id

    def assign_ticket(self, ticket_id: int, technician: str) -> bool:
        """Assign an active ticket to a designated technician."""
        if ticket_id not in self.tickets:
            logger.error("Ticket #%d does not exist.", ticket_id)
            return False

        self.tickets[ticket_id]["tech"] = technician.strip()
        logger.info(
            "Ticket #%d assigned to technician '%s'", ticket_id, technician
        )
        return True

    def add_note(self, ticket_id: int, note: str) -> bool:
        """Append a note to an existing ticket."""
        if ticket_id not in self.tickets:
            logger.warning(
                "Failed to add note: ticket #%d not found.", ticket_id
            )
            return False

        self.tickets[ticket_id]["notes"].append(note.strip())
        logger.info("Added note to ticket #%d", ticket_id)
        return True

    def close_ticket(self, ticket_id: int, auth_token: str) -> bool:
        """Authenticate and close/delete a ticket."""
        if auth_token != ADMIN_TOKEN:
            logger.warning(
                "Unauthorized attempt to close ticket #%d.", ticket_id
            )
            return False

        if ticket_id in self.tickets:
            del self.tickets[ticket_id]
            logger.info("Ticket #%d successfully closed.", ticket_id)
            return True

        logger.warning(
            "Cannot close ticket: ticket #%d does not exist.", ticket_id
        )
        return False

    def unresolved_high_priority(self) -> List[int]:
        """Return ticket IDs that are unassigned and urgency >= 4."""
        return [
            ticket_id
            for ticket_id, ticket in self.tickets.items()
            if ticket["priority"] >= 4 and ticket["tech"] is None
        ]

    # Backward compatibility alias
    def unresolvedHighPriority(self) -> List[int]:  # pylint: disable=C0103
        """Alias conforming to legacy camelCase naming."""
        return self.unresolved_high_priority()

    @staticmethod
    def ping_user_machine(hostname: str) -> int:
        """Safely ping target machine without shell invocation."""
        # Sanitize hostname to prevent injection
        clean_host = hostname.strip()
        if not re.fullmatch(r"[a-zA-Z0-9.-]+", clean_host):
            logger.error("Invalid hostname format: %s", clean_host)
            return -1

        command = (
            ["ping", "-n", "1", clean_host]
            if os.name == "nt"
            else ["ping", "-c", "1", clean_host]
        )
        try:
            result = subprocess.run(  # nosec B603
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.returncode
        except (subprocess.SubprocessError, OSError) as err:
            logger.error("Ping operation failed for '%s': %s", clean_host, err)
            return -1

    def save_tickets(self, filepath: str = "tickets.json") -> None:
        """Safely serialize tickets dictionary to JSON file."""
        try:
            with open(filepath, "w", encoding="utf-8") as file_out:
                json.dump(self.tickets, file_out, indent=2)
            logger.info(
                "Saved %d tickets to '%s'", len(self.tickets), filepath
            )
        except OSError as err:
            logger.error("Failed to save tickets to '%s': %s", filepath, err)


# Global instance & convenience wrapper functions for backward compatibility
_GLOBAL_SYSTEM = HelpdeskSystem()
tickets = _GLOBAL_SYSTEM.tickets


def raise_ticket(
    user: str,
    issue_type: str,
    urgency: str = "3",
    audit_trail: Optional[List[str]] = None,
) -> int:
    """Convenience function wrapping system ticket raising."""
    return _GLOBAL_SYSTEM.raise_ticket(user, issue_type, urgency, audit_trail)


def assign_ticket(ticket_id: int, technician: str) -> bool:
    """Convenience function wrapping ticket assignment."""
    return _GLOBAL_SYSTEM.assign_ticket(ticket_id, technician)


def add_note(ticket_id: int, note: str) -> bool:
    """Convenience function wrapping adding notes."""
    return _GLOBAL_SYSTEM.add_note(ticket_id, note)


def close_ticket(ticket_id: int, password: str) -> bool:
    """Convenience function wrapping ticket closing."""
    return _GLOBAL_SYSTEM.close_ticket(ticket_id, password)


def unresolved_high_priority() -> List[int]:
    """Convenience function listing unresolved high priority tickets."""
    return _GLOBAL_SYSTEM.unresolved_high_priority()


def unresolvedHighPriority() -> List[int]:  # pylint: disable=C0103
    """Legacy alias for unresolved_high_priority."""
    return _GLOBAL_SYSTEM.unresolved_high_priority()


def ping_user_machine(hostname: str) -> int:
    """Convenience function for pinging user host."""
    return HelpdeskSystem.ping_user_machine(hostname)


def save_tickets(file: str = "tickets.json") -> None:
    """Convenience function for saving tickets."""
    _GLOBAL_SYSTEM.save_tickets(file)


def main() -> None:
    """Execute main helpdesk workflow simulation."""
    t1 = raise_ticket("anil", "printer", "5")
    t2 = raise_ticket("meera", "wifi", "4")
    t3 = raise_ticket("joe", "vpn", "-7")

    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")

    high_pri = unresolved_high_priority()
    print(f"Unassigned high priority: {high_pri}")

    print(f"Recorded ticket #2 for Meera: {t2}")

    # Prompt user or default
    try:
        user_input = input(
            "Urgency for a new laptop ticket (1-5, Enter for 3): "
        )
    except (EOFError, KeyboardInterrupt):
        user_input = ""

    level = user_input.strip() or "3"
    t4 = raise_ticket("sana", "laptop", level)
    print(f"Created ticket #{t4} for Sana with urgency {level}")

    close_ticket(t3, ADMIN_TOKEN)
    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()
