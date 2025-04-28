"""
File IO Module for input/output operations related to text files and archive management.
"""

import os
import zipfile


def read_text_file(filename: str) -> str:
    """
    Reads and returns the content of the specified text file.

    Args:
        filename (str): Path to the input text file.

    Returns:
        str: The content of the file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        print('Ошибка открытия файла')
        return None

def write_text_file(filename: str, content: str) -> None:
    """
    Writes the given content to the specified text file.

    Args:
        filename (str): Path to the output file.
        content (str): Text content to write.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def archive_file(file_to_archive: str, archive_name: str) -> None:
    """
    Archives the specified file into a zip archive.
    After archiving, prints information about the archived file.

    Args:
        file_to_archive (str): The file to be archived.
        archive_name (str): Name of the resulting zip archive.
    """
    with zipfile.ZipFile(archive_name, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_to_archive, arcname=os.path.basename(file_to_archive))
    # Print details about the archive
    with zipfile.ZipFile(archive_name, 'r') as zipf:
        print("\nСодержимое архива:")
        for info in zipf.infolist():
            print(f"Имя файла: {info.filename}")
            print(f"Исходный размер: {info.file_size} байт")
            print(f"Сжатый размер: {info.compress_size} байт\n")
