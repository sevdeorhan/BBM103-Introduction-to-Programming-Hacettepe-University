import sys
import locale
locale.setlocale(locale.LC_ALL, "en_US")

def word_number(text):
    punctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')',
                                '*', '+', ',',  '.', '/', ':', ';', '<', '=', '>',
                                '?', '@', '[', '\\', ']',
                                '^', '_', '`', '{', '|', '}', '~']
    for character in text:
        if character in punctuation:
            text = text.replace(character, '')
        words= text.split()
    return len(words)

def sentence_number(text):
    sentence_number = 0
    text = text.replace('...', '.')
    for character in text:
       if character in ['!', '?', '.']:
           sentence_number += 1
    return sentence_number

def average_w_per_s(text):
    sentencenumber = sentence_number(text)
    wordnumber = word_number(text)
    if sentencenumber == 0:
        return 0
    average = wordnumber / sentencenumber
    return round(average,2)

def character_number(text):
    return len(text)

def just_words(text):
    total_character = 0
    characters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r',
                   's','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J',
                   'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                   '0','1','2','3','4','5','6','7','8','9','-',"'"]
    words= text.split()
    for word in words:
        if word.endswith("'"):
            total_character += -1

    for character in text:
        if character in characters :
            total_character += 1
    return total_character

def minword_frequency(text):
    punctuations = ['!', '"', '#', '$', '%', '&', "'", '(', ')',
                            '*', '+', ',', '.', '/', ':', ';', '<', '=', '>',
                            '?', '@', '[', '\\', ']',
                            '^', '_', '`', '{', '|', '}', '~']
    for character in text:
        if character in punctuations:
            text = text.replace(character, '')
    words= text.split()
    for i in range(len(words)):
        word = words[i]
        if word:
            words[i] = word[0].lower() + word[1:]

    minword=min(words, key=len)
    minwords = [word for word in words if len(word) == len(minword)]

    wordfrequencies = []
    for word in set(minwords):
        frequency = round(words.count(word) / len(words), 4)
        wordfrequencies.append((word, frequency))

    return wordfrequencies

def maxword_frequency(text):
    punctuations = ['!', '"', '#', '$', '%', '&', "'", '(', ')',
                            '*', '+', ',', '.', '/', ':', ';', '<', '=', '>',
                            '?', '@', '[', '\\', ']',
                            '^', '_', '`', '{', '|', '}', '~']
    for character in text:
        if character in punctuations:
            text = text.replace(character, '')
    words= text.split()
    for i in range(len(words)):
        word = words[i]
        if word:
            words[i] = word[0].lower() + word[1:]
    maxword=max(words, key=len)
    maxwords= [word for word in words if len(word) == len(maxword)]

    wordfrequencies= []
    for word in set(maxwords):
        frequency = round(words.count(word)/len(words),4)
        wordfrequencies.append((word, frequency))

    return wordfrequencies

def word_frequencies(text):
    punctuations = ['!', '"', '#', '$', '%', '&', '(', ')',
                            '*', '+', ',', '.', '/', ':', ';', '<', '=', '>',
                            '?', '@', '[', '\\', ']',
                            '^', '_', '{', '|', '}', '~']
    for character in text:
        if character in punctuations:
            text = text.replace(character, '')
    words = text.split()
    word_count= { }
    for word in words:
        word =word.lower()
        if word.endswith("'"):
            word =word[:-1]
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    frequencies = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
    word_frequencies = []
    for word, frequency in frequencies:
        frequency = round(frequency / len(words), 4)
        word_frequencies.append((word, frequency))
    return word_frequencies

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r") as file:
        text = file.read()

    with open(output_file, "w") as output:

        output.write(f"Statistics about {input_file:7}:\n")
        output.write(f"#Words                  : {word_number(text)}\n")
        output.write(f"#Sentences              : {sentence_number(text)}\n")
        output.write(f"#Words/#Sentences       : {average_w_per_s(text):.2f}\n")
        output.write(f"#Characters             : {character_number(text)}\n")
        output.write(f"#Characters (Just Words): {just_words(text)}\n")

        minwords = minword_frequency(text)
        if len(minwords)==1:
            output.write(f"The Shortest Word       :")
            for word, frequency in sorted(minwords, key=lambda x: (-x[1], x[0])):
                output.write(f" {word:<24} ({frequency:.4f})\n")

        if len(minwords)>1:
            output.write(f"The Shortest Words      :\n")
            minwords = minword_frequency(text)
            for word, frequency in sorted(minwords, key=lambda x: (-x[1], x[0])):
                output.write(f"{word:<24} ({frequency:.4f})\n")

        maxwords= maxword_frequency(text)
        if len(maxwords)==1:
            output.write(f"The Longest Word        :")
            for word, frequency in sorted(maxwords, key=lambda x: (-x[1], x[0])):
                output.write(f" {word:<24} ({frequency:.4f})\n")
        if len(maxwords)>1:
            output.write(f"The Longest Words       :\n")
            for word, frequency in sorted(maxwords, key=lambda x: (-x[1], x[0])):
                output.write(f"{word:<24} ({frequency:.4f})\n")


        output.write("Words and Frequencies   :")
        word_frequency_list = word_frequencies(text)
        for word, frequency in sorted(word_frequency_list, key=lambda x: (-x[1], x[0])):
            output.write(f"\n{word:<24}: {frequency:.4f}")

if __name__ == "__main__":
    main()