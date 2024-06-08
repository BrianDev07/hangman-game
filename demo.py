def get_words(filepath):
    word_bank = []

    with open(filepath, "r") as f:
        word_bank = [line.rstrip() for line in f]

    return word_bank


print(get_words("./es_words.txt"))