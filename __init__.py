"""Mosaic: design direction for Hermes.

The plugin is deliberately focused: reference families, a design director,
a deterministic forge, and a measured browser gate. It does not fetch
references or publish anything; the visual gate renders a page the caller
already built and reports its own evidence.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

__version__ = "0.8.1"
TOOLSET = "mosaic"


def register(ctx) -> None:
    from .mosaic_tools import TOOL_SPECS

    for spec in TOOL_SPECS:
        def tool_handler(args: dict, _run=spec["handler"], **_kw) -> str:
            return _run(args or {})

        ctx.register_tool(
            name=spec["name"],
            toolset=TOOLSET,
            schema=spec["schema"],
            handler=tool_handler,
            description=spec["description"],
            emoji=spec.get("emoji", "🎛️"),
        )


__all__ = ["register", "__version__"]
