text = ('So she was considering in her own mind, '
          'as well as she could, '
          'for the hot day made her feel very sleepy and stupid, '
          'whether the pleasure of making a daisy-chain would be worth the trouble '
          'of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.')




def string_without_words_starts_with(str, letter):
    words = str.replace(',', '').replace('.','').split()
    for word in words:
        if word.lower().startswith(letter):
            str = str.replace(word, '')
    return str

print(string_without_words_starts_with(text, 's'))

def word_contains_letter(str, letter):
    for word in str.split(' .,'):
        if word.find(letter) != -1:
            return word, str.find(word)
    return None, -1

def get_upper_letters_count(string):
    upper_letters = 0

    for c in string:
        if c.isupper():
            upper_letters += 1

    return upper_letters


