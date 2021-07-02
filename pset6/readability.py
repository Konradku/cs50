text = input("Text: ")

spaces = text.count(" ")
dots = text.count(".")
q_marks = text.count("?")
exclamations = text.count("!")
sentences = dots + q_marks + exclamations
words = spaces + 1
letters = 0
for i in text:
    if (i >= "a" and i <= "z") or (i >= "A" and i <= "Z"):
        letters += 1
    
L = letters * 100 / words
S = sentences * 100 / words
grade = round(0.0588 * L - 0.296 * S - 15.8)

if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print(f"Grade: {grade}")