from cryptor import cryptor, decryptor
from generator import generator
import os
import random


currectDirectory = os.getcwd()
textInFile = ''
key = ''
count = 1
save = ''

def checkCount(input_count, type):
    if input_count.isdigit():
        return input_count
    else:
        print('Error: incorrect input data. Please enter again')
        if type == 'e/d':
            return checkCount(input('What is the number of encryption / decryption?: '), 'e/d')
        elif type == 'left_border':
            return checkCount(input('Enter the minimum word length: '), 'left_border')
        elif type == 'rigth_border':
            return checkCount(input('Enter the maximum word length: '), 'rigth_border')


def check(input_user, type):
    input_user = input_user.lower().strip()
    if input_user in ['open', 'create', 'y', 'n', 'enter', 'gen', '1', '2'] \
            or (input_user == '1' and type == 'c/d') or (input_user == '2' and type == 'c/d'):
        return input_user
    else:
        print('Error: incorrect input data. Please enter again')
        if type == 'o/c':
            return check(input('Open file or create new?'), 'o/c')
        elif type == 'c/d':
            return check(input('Encrypt or decrypt data?'), 'c/d')
        elif type == 'y/n(save)':
            return check(input('Encrypt or decrypt data?'), 'y/n(save)')
        elif type == 'y/n(output)':
            return check(input('Do you want to output data?(y/n)'), 'y/n(output)')
        elif type == 'enter/gen':
            return check(input("Enter the key for encryption / decryption or generate key?: "), 'enter/key')



if __name__ == "__main__":
    answerUser = check(input('Open file or create new?(open/create): '), 'o/c')  # question open/create
    if answerUser == 'open':
        currectDirectory = input('Enter the path to the file: ')
        with open(currectDirectory, 'r') as file:
            textInFile = file.read()
    elif answerUser == 'create':
        textInFile = input('Please enter the text' + '\n')
    check_point = answerUser

    answerUser = check(input('Encrypt or decrypt data?\n1.Encrypt\n2.Decrypt\nInput: '), 'c/d')  # question encrypt/decrypt
    count = checkCount(input('What is the number of encryption / decryption?(enter number): '), 'e/d')  # question number of cycless
    key = check(input("Enter the key for encryption / decryption or generate key?(enter/gen): "), 'enter/gen') # question generate or enter key
    if key == 'gen':
        left_border = int(checkCount(input('Enter the minimum word length: '), 'left_border'))
        rigth_border = int(checkCount(input('Enter the maximum word length: '), 'rigth_border'))
        key = generator(random.randint(left_border, rigth_border))
    elif key == 'enter':
        key = input('Enter key for encryption / decryption: ')

    if answerUser == '1':
        textInFile = cryptor(textInFile, key, count)
        print('(⊙ヮ⊙) file is successful encrypted')
    elif answerUser == '2':
        textInFile = decryptor(textInFile, key, count)
        print('(⊙ヮ⊙) file successfully decrypted')

    answerUser = check(input('Do you want to output data?(y/n)'), 'y/n(output)')  # question output data
    if answerUser == 'y':
        print('You text:\n',textInFile)

    answerUser = check(input('Do you want to save text to file?(y/n)'), 'y/n(save)')  # question save text to file
    if answerUser == 'y':
        if check_point == 'open':
            answerUser = check(input('save the file in its original directory?(y/n)'), 'y/n')
            if answerUser == 'y':
                with open(currectDirectory, 'w') as file:
                    file.write(textInFile)
            elif answerUser == 'n':
                currectDirectory = input('Enter save directory: ')
                with open(currectDirectory, 'w') as file:
                    file.write(textInFile)
        elif check_point == 'create':
            currectDirectory = input('Enter save directory: ')
            with open(currectDirectory, 'w') as file:
                file.write(textInFile)

    input('Press enter, that exit programm')
