"""
Framework integrations for Aegean consensus.
"""

from aegean.integrations.autogen_adapter import AutoGenAgentAdapter
from aegean.integrations.openclaw_gateway import OpenClawGateway, OpenClawAgentProxy

__all__ = [
    "AutoGenAgentAdapter",
    "OpenClawGateway",
    "OpenClawAgentProxy",
]

