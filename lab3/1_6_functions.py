def reverse_sentence(sentence):
    words = sentence.split()
    reversed_words = words[::-1]
    return ' '.join(reversed_words)

# Example usage:
sentence = input("Enter a sentence: ")
print("Reversed sentence:", reverse_sentence(sentence))
