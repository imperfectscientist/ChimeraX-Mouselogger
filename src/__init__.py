from chimerax.core.toolshed import BundleAPI

class _MyAPI(BundleAPI):

    api_version = 1

    @staticmethod
    def initialize(session, bundle_info):
        pass

    @staticmethod
    def register_command(bi, ci, logger):
        from . import cmd
        if ci.name == "mouselogger":
            func = cmd.handle_mouselogger
            desc = cmd.mouselogger_desc
        else:
            raise ValueError(f"Unknown command {ci.name}")

        from chimerax.core.commands import register
        register(ci.name, desc, func)

bundle_api = _MyAPI()
