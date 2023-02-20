# imports at top

# Sample Program to earse

# Grab user text using input command
user_input = input("Input text to translate to pig latin: ")

print("User Text: ", user_input)

user_input_list = user_input.split(' ')

translation = ""
for word in user_input_list:
    if len(word) >= 3: # only translate words with more than 3 characters
        word = word + "%say" % (word[0]) 
        word = word[1:]
        translation += word + " "
    else:
        pass

print("Translation: ", translation)