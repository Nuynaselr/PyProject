from os import getcwd, listdir, rename, chdir

current_directory = str(getcwd())
current_file_path = ''
file_path = ''
file_name = 'noname'
counter = 1

if __name__ == '__main__':
    print('!!!!Hello, welcome to the file renamer!!!!')
    question_for_path = input('Full path or from the current directory(1 - full, 2 - current): ')
    file_path = input('Enter file path: ')
    if question_for_path == '2':
        current_file_path = current_directory + file_path
    else:
        current_file_path = file_path
    try:
        chdir(file_path)
        file_name = input('Enter file name: ')
        array_file = listdir(file_path)
        if len(array_file) > 0:
            for file in array_file:
                rename(file, str(file_name + str(counter) + '.jpg'), src_dir_fd=None, dst_dir_fd=None)
                counter += 1
    except FileNotFoundError:
        print('Incorrect path')


