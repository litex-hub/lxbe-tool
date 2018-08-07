#!/usr/bin/env python3

import abc

class ToolNotFoundError(OSError):
    """Tool is not found in environment."""
    pass


class ToolWrongVersionError(OSError):
    """Tool is found but provides wrong version."""
    pass


class Provider(abc.ABC):
    """Base class for all providers."""

    @abc.abstractmethod
    def install_module(self, module_name, module_path=None, module_version=None):
        """Install a Python module into the Python environment.

        module_path or module_version should be provided.


        """
        pass

    @abc.abstractmethod
    def find_tool(self, tool_name, tool_version):
        """Find a tool inside the provider environment.


        Raises:
            ToolNotFoundError: Raised when the requested tool is not found.
            ToolWrongVersionError: Raised when the requested tool is found but
                is providing the wrong version.

        Returns:
            ????

        """
        pass

    @abc.abstractmethod
    def install_tool(self, tool_name, tool_version):
        """Installs a tool inside the provider environment.

        Raises:
            SystemError: The provider is unable to install the tool.

        """
        pass

