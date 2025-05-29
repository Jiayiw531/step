from score_checker import SCORES, WORDS_FILE
import os


# I plan to create counters for each word in the dictionary and also for the input lines, 
# then find the anagrams that could be formed with each input line
# for each anagram found, I will compare its score with the current highest score

def countLetters(word): 
    word = word.lower()
    counter = [0] * 26
    for char in word:
        counter[ord(char) - ord('a')] += 1
    return counter

def getScore(counter): 
    # counter is a list with the count of all alphabets (including the unused ones)
    score = 0
    for index in range(len(counter)): 
        if counter[index] > 0: 
            score += counter[index] * SCORES[index]
    return score

def findBest(word_counter_pairs, input_line):
    # takes in a list of (word, counter) pairs and the input line, 
    # decide if each word in the dictionary could be formed by the letters in input line
    # returns the word with highest score
    input_counter = countLetters(input_line)
    best_score = (0, "")
    for word, counter in word_counter_pairs:
        if isIncluded(counter, input_counter):
            best_score = max(best_score, (getScore(counter), word))
    return best_score[1]

def isIncluded(word_counter, input_counter):
    for i in range(len(word_counter)): 
        if word_counter[i] > input_counter[i]:
            return False
    return True

# input
dictionary = []
with open(WORDS_FILE, 'r') as file:
    for line in file: 
        line = line.strip()
        if not line: 
            continue
        if not line.isalpha():
            print(f"input is not alphabetic: {line}")
            continue
        dictionary.append(line.lower())

input_file = input("Enter file name of target words: (e.g. target.txt) ")
if not os.path.isfile(input_file):
    print(f"File {input_file} does not exist.")
    exit(1)

target_lines = []
with open(input_file, 'r') as file:
    for line in file:
        line = line.strip()
        if not line: 
            continue
        if not line.isalpha():
            print(f"input is not alphabetic: {line}")
            continue
        target_lines.append(line.lower())

# to avoid recounting the dictionary counters for each input line,
# word_counter_pairs is storing a list of tuples (word, counter)
word_counter_pairs = [(word, countLetters(word)) for word in dictionary]

# output
base, ext = os.path.splitext(input_file)
output_file = f"{base}_ans{ext}"

with open(output_file, 'w') as out_file:
    for word in target_lines:
        result = findBest(word_counter_pairs, word)
        out_file.write(result + '\n')