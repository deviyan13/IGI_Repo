from file_io import *
from inputs_check import input_int_with_condition

"""
Text Analysis Module
This module contains the TextAnalyzer class that performs analysis of text.
"""

import re


class TextAnalyzer:
    """
    TextAnalyzer class provides methods to perform various analyses on text.
    """

    def __init__(self, text: str):
        """
        Initializes the TextAnalyzer with the provided text.

        Args:
            text (str): The text to analyze.
        """
        self.text = text

    def count_sentences(self) -> dict:
        """
        Counts the total number of sentences and sentences of each punctuation type.

        Returns:
            dict: Dictionary with keys 'total', 'declarative', 'interrogative', 'imperative'.
        """
        sentences = re.split(r'[.?!]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        total = len(sentences)
        declarative = len(re.findall(r'\.(?:\s|\w)*', self.text))
        interrogative = len(re.findall(r'\?(?:\s|\w)*', self.text))
        imperative = len(re.findall(r'!(?:\s|\w)*', self.text))
        return {
            'total': total,
            'declarative': declarative,
            'interrogative': interrogative,
            'imperative': imperative
        }

    def average_sentence_length(self) -> float:
        """
        Calculates the average sentence length in characters (only word characters are counted).

        Returns:
            float: Average sentence length.
        """
        sentences = re.split(r'[\.?!]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0.0
        total_chars = 0
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence)
            total_chars += sum(len(word) for word in words)
        return total_chars / len(sentences)

    def average_word_length(self) -> float:
        """
        Calculates the average word length in characters.

        Returns:
            float: The average word length.
        """
        words = re.findall(r'\b\w+\b', self.text)
        if not words:
            return 0.0
        return sum(len(word) for word in words) / len(words)

    def count_emoticons(self) -> int:
        """
        Counts the number of emoticons in the text.

        An emoticon is defined as a sequence starting with ':' or ';' exactly once,
        followed by zero or more '-' characters, and ending with at least one identical bracket
        from the set '(', ')', '[' or ']'. No other characters may appear inside.

        Returns:
            int: The count of emoticons.
        """
        pattern = r'[:;]-*([\(\)\[\]])\1*'
        return len(re.findall(pattern, self.text))


    def get_all_words(self) -> list:
        """
        Extracts all words from the text (excluding whitespace).

        Returns:
            list: List of words.
        """
        return re.findall(r'\b\w+\b', self.text)


    def highlight_letter_pairs(self) -> str:
        """
        Encloses every occurrence of a pair of characters, where the first is a lowercase Latin letter
        and the second is an uppercase Latin letter, with markers "_?_" on both sides.

        Returns:
            str: The modified text with highlighted letter pairs.
        """
        pattern = r'([a-z][A-Z])'
        return re.sub(pattern, r'_?_\1_?_ ', self.text)


    def count_words_shorter_than(self, length: int = 7) -> int:
        """
        Counts the number of words in the text with length less than the specified threshold.

        Args:
            length (int): Threshold length for words.

        Returns:
            int: Number of words shorter than the threshold.
        """
        words = self.get_all_words()
        return sum(1 for word in words if len(word) < length)


    def shortest_word_ending_with(self, letter: str = 'a') -> str:
        """
        Finds the shortest word ending with the specified letter.

        Args:
            letter (str): The ending letter (default is 'a').

        Returns:
            str: The shortest word ending with the given letter, or an empty string if none found.
        """
        words = self.get_all_words()
        filtered = [word for word in words if word.endswith(letter)]
        if not filtered:
            return ''
        return min(filtered, key=len)


    def sorted_words_by_length(self) -> list:
        """
        Returns all words sorted in descending order by their length.

        Returns:
            list: List of words sorted from longest to shortest.
        """
        words = self.get_all_words()
        return sorted(words, key=len, reverse=True)


    def generate_report(self) -> str:
        """
        Generates a comprehensive report based on text analysis.

        Returns:
            str: The analysis report.
        """
        sentences_info = self.count_sentences()
        avg_sentence_len = self.average_sentence_length()
        avg_word_len = self.average_word_length()
        emoticon_count = self.count_emoticons()

        report_lines = []
        report_lines.append("Результаты анализа текста:\n")
        report_lines.append("Информация о предложениях:")
        report_lines.append(f"Количество предложений: {sentences_info['total']}")
        report_lines.append(f"Повествовательные: {sentences_info['declarative']}")
        report_lines.append(f"Вопросительные: {sentences_info['interrogative']}")
        report_lines.append(f"Побудительные: {sentences_info['imperative']}\n")
        report_lines.append(f"Средняя длина предложения (учитываются только слова): {avg_sentence_len:.2f}")
        report_lines.append(f"Средняя длина слова: {avg_word_len:.2f}")
        report_lines.append(f"Количество смайликов в тексте: {emoticon_count}\n")

        return "\n".join(report_lines)


def task2():

    print(
        "Task 2 menu:\n"
        "1. Получить список всех слов текста, не включая пробелы\n"
        "2. Выделить пары символов, первый из которых – малая латинская буква, а второй – большая латинская буква, знаками «_?_» с обеих сторон\n"
        "3. Определить число слов, длина которых меньше 7 символов\n"
        "4. Найти самое короткое слово, заканчивающееся на букву 'a'\n"
        "5. Вывести все слова в порядке убывания их длин\n"
        "6. Общее задание - определить и сохранить файл с результатами\n"
        "7. Архивировать файл task2.txt и вывести информацию о нем из архива\n"
        "8. Выход в главное меню\n")


    while True:
        item = input_int_with_condition('Введите пункт меню: ', lambda x: 0 < x < 9)

        text_analyzer = TextAnalyzer(read_text_file('files/task2.txt'))

        all_words = text_analyzer.get_all_words()
        highlighted_text = text_analyzer.highlight_letter_pairs()
        words_less_than = text_analyzer.count_words_shorter_than(7)
        shortest_word = text_analyzer.shortest_word_ending_with('a')
        sorted_words = text_analyzer.sorted_words_by_length()

        match item:
            case 1:
                print(f"Все слова в тексте: {(all_words)}")
            case 2:
                print("\nТекст с выделенными парами (первая буква — малая латинская, вторая — большая):")
                print(highlighted_text)
            case 3:
                print(f" - Слов, длина которых меньше 7 символов: {words_less_than}")
            case 4:
                if shortest_word:
                    print(f" - Самое короткое слово, заканчивающееся на 'a': '{shortest_word}'")
                else:
                    print(" - Нет слов, заканчивающихся на 'a'.")
            case 5:
                print(" - Слова в порядке убывания длины:")
                print(", ".join(sorted_words))
            case 6:
                write_text_file('files/task2_report.txt', text_analyzer.generate_report())
                print('Отчет общего задания сохранен в files/task2_report.txt')
            case 7:
                archive_file('files/task2.txt', 'files/task2_archive.zip')
            case 8:
                break