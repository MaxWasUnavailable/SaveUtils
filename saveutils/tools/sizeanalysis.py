from logging import getLogger, StreamHandler, Formatter
from sys import getsizeof
import json
import math

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
        total_size = SizeAnalysis.get_size(save)
        logger.info(f"Total save file size (APPROX): {total_size} bytes")

        analysed_data: dict = dict()
        for key, value in save.data.items():
            size = getsizeof(json.dumps(value)) / save.raw_size_conversion_factor
            size = SizeAnalysis.SIG_FIGS(size)
            analysed_data[key] = {
                "size": size,
                "percentage": (size / total_size) * 100
            }

        return analysed_data

    @staticmethod
    def get_size(save: SaveFile) -> float:
        """
        Gets the size of a save file.
        :param save: The save file to get the size of.
        :return: The size of the save file in bytes.
        """
        total_size = 0
        for key, value in save.data.items():
            size = getsizeof(json.dumps(value))
            total_size += size

        return SizeAnalysis.SIG_FIGS(total_size / save.raw_size_conversion_factor)

    @staticmethod
    def SIG_FIGS(val: float, sig_figs:int = 3) -> int:
        figs = math.log10(val)
        if figs < sig_figs:
            return int(val)
        digits_to_remove = int(figs - sig_figs) + 1
        if digits_to_remove == 0:
            logger.info(f"{digits_to_remove} -> {val}")
        val = int(val / 10**digits_to_remove)
        val = val * 10**digits_to_remove
        if digits_to_remove == 0:
            logger.info(f"{digits_to_remove} -> {val}")
        return int(val)

def register_subparser(main_subparser) -> None:
    """
    Registers the player migration subparser.
    :param main_subparser: The main parser's subparser
    """
    sizeanalysis = main_subparser.add_parser("sizeanalysis", description=description, help=description)
    sizeanalysis.add_argument('-r', '--report', action='store_true',
                              help='Saves a report of the size analysis in report.html')


def handle_subparser(args) -> None:
    """
    Handles the player migration subparser.
    :param args: The arguments
    """
    if args.tool == "sizeanalysis":
        save = args.save
        analysed_data = SizeAnalysis.analyse_size(save)

        sorted_data = sorted(analysed_data.items(), key=lambda x: x[1]["size"], reverse=True)

        if args.report:
            with open("report.html", "w") as report:
                report.write("<html><body><table><tr><th>Key</th><th>Size</th><th>Percentage</th></tr>")
                for key, value in sorted_data:
                    report.write(
                        f"\n<tr><td>{key}</td><td>{value['size']}</td><td>{round(value['percentage'], 3)}</td></tr>")
                report.write("</table></body></html>")
        else:
            for key, value in sorted_data:
                logger.info(f"{key}: {value['size']} bytes ({value['percentage']}%)")
