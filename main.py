from adapters.cli import CLI
from entities.errors import CasinoError

if __name__ == "__main__":
    try:
        CLI.hello()
    except CasinoError:
        print("")
