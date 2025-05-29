def sort_dictionary(dictionary):
    sorted_dict = {}
    for word in dictionary:
        sorted_word = "".join(sorted(word))
        if sorted_word not in sorted_dict:
            sorted_dict[sorted_word] = []
        sorted_dict[sorted_word].append(word)
    return sorted_dict

def findAllAnagrams(word, sorted_dict):
    # returns a list of anagrams of given word
    sorted_word = ''.join(sorted(word))
    for word in sorted_dict:
        if "".join(sorted(word)) == sorted_word:
            return sorted_dict[word]
    return []


dictionary = []
with open('words.txt', 'r') as file:
    for line in file: 
        line = line.strip()
        if not line: 
            continue
        if not line.isalpha():
            print(f"input is not alphabetic: {line}")
            continue
        dictionary.append(line.lower())

sorted_dict = sort_dictionary(dictionary)
words = input("Enter words separated by spaces: ").split()

for word in words:
    anagrams = findAllAnagrams(word, sorted_dict)
    if anagrams:
        print(f"Anagrams of '{word}': {', '.join(anagrams)}")
    else:
        print(f"No anagrams found for {word}.")