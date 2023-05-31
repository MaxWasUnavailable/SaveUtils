from logging import getLogger, StreamHandler, Formatter
from sys import getsizeof

from savefile.savefile import SaveFile

description = "A tool for analysing the size of a save file."

logger = getLogger(__name__)
logger.setLevel("INFO")
handler = StreamHandler()
handler.setFormatter(Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s"))
logger.addHandler(handler)


class SizeAnalysis:
    """
    A tool for analysing the size of a save file.
    """

    @staticmethod
    def analyse_size(save: SaveFile) -> dict:
        """
        Analyses the size of a save file.
        :param save: The save file to analyse.
        :return: A dictionary containing the percentage and absolute size of each key-value pair in the save file.
        """
        logger.info("Analysing save file size...")
        data: dict = save.data
        total_size = getsizeof(data)
        logger.info(f"Total save file size: {total_size} bytes")

        analysed_data: dict = dict()
        for key, value in data.items():
            analysed_data[key] = {
                "size": getsizeof(value),
                "percentage": (getsizeof(value) / total_size) * 100
            }

        return analysed_data


def register_subparser(main_subparser) -> None:
    """
    Registers the player migration subparser.
    :param main_subparser: The main parser's subparser
    """
    sizeanalysis = main_subparser.add_parser("sizeanalysis", description=description, help=description)
    sizeanalysis.add_argument('-r', '--report', action='store_true',
                              help='Saves a report of the size analysis in report.txt')


def handle_subparser(args) -> None:
    """
    Handles the player migration subparser.
    :param args: The arguments
    """
    if args.tool == "sizeanalysis":
        save = args.save
        analysed_data = SizeAnalysis.analyse_size(save)
        if args.report:
            with open("report.txt", "w") as report:
                report.write(f"Total save file size: {getsizeof(save.data)} bytes\n")
                for key, value in analysed_data.items():
                    report.write(f"{key}: {value['size']} bytes ({value['percentage']}%)\n")
        else:
            for key, value in analysed_data.items():
                logger.info(f"{key}: {value['size']} bytes ({value['percentage']}%)")
