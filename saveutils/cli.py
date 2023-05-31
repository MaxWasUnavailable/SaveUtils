import argparse

from savefile.savefile import SaveFile
from tools.cheats import handle_subparser as cheats_handle_subparser
from tools.cheats import register_subparser as cheats_register_subparser
from tools.playermigration import handle_subparser as playermigration_handle_subparser
from tools.playermigration import register_subparser as playermigration_register_subparser

parser = argparse.ArgumentParser(prog='SaveUtils', description='Shadows of Doubt SaveUtils')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging', default=False,
                    required=False)
parser.add_argument('-i', '--input', type=str, help='The input save file path (absolute or relative)', required=True)
tools_subparser = parser.add_subparsers(title="Tools", description="Tools", dest="tool")

cheats_register_subparser(tools_subparser)
playermigration_register_subparser(tools_subparser)

if __name__ == '__main__':
    args = parser.parse_args()

    save = SaveFile(args.input, verbose=args.verbose)

    args.save = save

    if args.cheats:
        cheats_handle_subparser(args)

    if args.playermigration:
        playermigration_handle_subparser(args)
