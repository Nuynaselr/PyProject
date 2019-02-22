from os import chdir, getcwd, listdir


class ImageList:
    image_list = []
    file_path = ''
    current_directory = getcwd()

    def __init__(self):
        pass

    def set_path(self, path):
        self.file_path = path
        try:
            file_path_time = self.current_directory + self.file_path
            chdir(file_path_time)
            self.file_path = file_path_time
        except FileNotFoundError:
            chdir(self.file_path)

        self._check_aline()
        self.image_list = listdir(self.file_path)

    def get_file_path(self):
        return self.file_path

    def get_image_list(self):
        return self.image_list

    def _check_aline(self):
        try:
            for word in self.image_list:
                if ('.jpg' not in word) and ('.jpeg' not in word):
                    raise NameError()
        except NameError:
            print('Error: there is a non-image file')
