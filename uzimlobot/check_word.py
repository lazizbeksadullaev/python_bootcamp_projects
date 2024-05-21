from uzwords import words
from difflib import get_close_matches

def check_word(word):
    word = word.lower()
    matches = set(get_close_matches(word, words))
    available = False # bunday so'z mavjudmas
    if word in matches:
        available = True # mavjud word yubordi, yani to'g'ri so'z yuborgan
        matches = word
    elif 'ҳ' in word:
        matches.update(get_close_matches(word.replace('ҳ', 'х'), words))
    elif 'х' in word:
        matches.update(get_close_matches(word.replace('х', 'ҳ'), words))

    return {'available': available, 'matches': matches}

if __name__ == "__main__":
    print(check_word('ҳола'))