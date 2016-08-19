from wand.image import Image
from string import ascii_uppercase, digits
from random import choice
import os


class PDFTransformer(object):
    """
    The main purpose of the class is to transform a pdf file into multiple
    png files. The number of the png files is equal with pdf pages.
    (so one page for a png file)
    """
    @staticmethod
    def id_generator(size=6, chars=ascii_uppercase + digits):
        return ''.join(choice(chars) for _ in range(size))

    def __new__(cls, *args, **kwargs):
        _instance = super(PDFTransformer, cls).__new__(cls)
        _instance.random_part = PDFTransformer.id_generator()
        work_directory = kwargs['work_directory']
        _instance.to_search = os.path.join(work_directory,
                                           _instance.random_part)
        filename = os.path.join(
            work_directory, _instance.random_part + ".png")

        with Image(blob=kwargs['pdf']) as img:
            img.save(filename=filename)

        _instance.generated_files = []
        for file in os.listdir(work_directory):
            if file.startswith(_instance.random_part):
                _instance.generated_files.append(
                    os.path.join(work_directory, file))

        _instance.generated_files.sort()

        return _instance

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_val, trace):
        for file in self.generated_files:
            os.remove(file)
