import os
import pathlib
import re
from io import TextIOWrapper

import bs4
import requests


def write_to_file(array_of_strings: list[str], output_file: TextIOWrapper) -> None:
    """
    Writes given array of string to the given file line-by-line.

    Args:
        array_of_strings (list[str]): List of string you want to write to the file;
        output_file (TextIOWrapper): The file you want to write data to; Must be already open;
    """
    for string in array_of_strings:
        output_file.write(string + "\n")

def filter_symbols(input_string: str) -> str:
    """
    Filters given string so it doesn't contain unwanted symbols.

    Args:
        input_string (str): String you want to filter;

    Returns:
        str: Filtered string;
    """
    special_symbols: list[str] = ["—", r"!", r"\?", r"\.", ",",
        r"\-", r"\+", r"\=", "@", ";", ":", "'", '"', "_", "«", "»", "*"]

    return re.sub(r"[^a-zA-Z0-9а-яА-ЯёЁ" + "".join(special_symbols) + " " + "]", "", input_string)

def correct_punctuation(input_string: str) -> str:
    """
    Here punctuation symbols are: "!", "?", ".", ",", ":", ";".
    Data is so dirty so it needs to be cleaned. After using this function it will be no spaces
    before punctuation and only one space after.

    Args:
        input_string (str): String witch punctuation you want to correct;

    Returns:
        str: String with corrected punctuation;
    """
    symbol_to_regex_symbol = {".": r"\.", "?": r"\?", "-": r"\-", "+": r"\+", "=": r"\="}

    special_symbols: list[str] = ["!", "?", ".", ",", ":", ";"]

    for symbol in special_symbols:
        input_string = re.sub(symbol_to_regex_symbol.get(symbol, symbol) + r"+", f"{symbol} ", input_string)
        input_string = re.sub(r" *" + symbol_to_regex_symbol.get(symbol, symbol) + r" *", f"{symbol} ", input_string)

    input_string = re.sub(r"—+", "—", input_string)
    input_string = re.sub(r" *— *", " — ", input_string)

    input_string = re.sub(" *«", " «", input_string)
    input_string = re.sub("» *", "» ", input_string)
    
    input_string = input_string.replace("  ", " ")

    return input_string
    
def preprocess(input_string: str) -> str:
    """
    Applies all preprocessing functions to given string; Also uses strit() at the end of preprocessing.

    Args:
        input_string (str): String you want to preprocess;

    Returns:
        str: Preprocessed string;
    """
    return correct_punctuation(filter_symbols(input_string)).strip()


class AnekdotyRuParser:
    """
    Class for parsing content from anekdoty.ru website.
    """
    def __init__(self, path_to_data_file: str):
        self._path_to_website = "https://anekdoty.ru/"
        self._path_to_data_file = path_to_data_file

    def _get_subtopics(self) -> list[str]:
        """
        Returns subtopics from anekdory.ru so it can be parsed much easily.

        Returns:
            list[str]: List of subtopics;
        """
        response: requests.models.Response = requests.get(self._path_to_website)

        try:
            response.raise_for_status()
        except Exception:
            print(f"Sorry, but target site is unreachable: {self._path_to_website}")
            return []
        else:
            subtopics: list[str] = []

            response_html: bs4.element.Tag = bs4.BeautifulSoup(response.text,
                features="html.parser").html
            references: bs4.element.ResultSet = response_html.body.findAll("a")
            
            for reference in references[2:]:
                if reference.get("class") is None and "/p/" not in reference.get("href"):
                    subtopics.append(reference.get("href"))
                else:
                    break

            return subtopics

    def _get_page_content(self, path_to_page: str) -> list[str]:
        """
        Returns pardes anekdots from given page of anekdoty.ru.

        Args:
            path_to_page (str): Page you want to parse;

        Returns:
            list[str]: list of collected anekdots;
        """
        response = requests.get(path_to_page)

        anekdots: list[str] = []

        try:
            response.raise_for_status()
        except Exception:
            print(f"Sorry, but target site is unreachable: {path_to_page}")
            return []
        else:
            page_paragraphs: bs4.element.ResultSet = bs4.BeautifulSoup(response.text,
                features="html.parser").body.findAll("p")
            for paragraph in page_paragraphs:
                if list(paragraph.children) != []:
                    current_anekdot: str = ""
                    for part in list(paragraph.children):
                        text: str = part.text
                        current_anekdot += text
                    anekdots.append(current_anekdot)

            anekdots = [preprocess(anekdot) for anekdot in anekdots]

            return anekdots

    def collect_data(self) -> None:
        """
        Collects data from the target site as stores in to the file line-by-line.
        Also preprocesses the content.
        """
        with open(self._path_to_data_file, "w", encoding="utf-8") as output_file:            
            for topic in self._get_subtopics():
                current_anekdots: list[str] = self._get_page_content(topic)
                write_to_file(current_anekdots, output_file)

                page_number: int = 2
                current_anekdots = self._get_page_content(topic + str(page_number) + "/")
                
                while (current_anekdots != []):
                    write_to_file(current_anekdots, output_file)
                    page_number += 1
                    current_anekdots = self._get_page_content(topic + str(page_number) + "/")


if __name__ == "__main__":
    current_file_path: os.PathLike[str] = pathlib.Path(__file__).parent.parent.parent.resolve()
    path_to_data_file: str = os.path.join(os.path.join(os.path.join(current_file_path, "data"),
        "raw_data"), "anekdoty_ru.txt")

    anekdoty_ru_parser = AnekdotyRuParser(path_to_data_file)
    anekdoty_ru_parser.collect_data()
