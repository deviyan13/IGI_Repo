
def string_without_words_starts_with(str, letter):
    words = str.replace(',', '').replace('.','').split()
    for word in words:
        if word.lower().startswith(letter):
            str = str.replace(word, '')
    return str


def first_word_contains_letter(str, letter):
    words = str.replace(',', '').replace('.', '').split()
    for word in words:
        if word.find(letter) != -1:
            return word, words.index(word)
    return None, -1


def get_lower_letters_count(str):
    lower_letters = 0

    for c in str:
        if c.islower():
            lower_letters += 1

    return lower_letters
