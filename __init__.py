"""ComfyUI custom-node entrypoint.

The repository root is the directory ComfyUI installs as a custom node. The
actual implementation lives in the fearnworks_nodes package.
"""

from fearnworks_nodes.legacy import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

WEB_DIRECTORY = "web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
