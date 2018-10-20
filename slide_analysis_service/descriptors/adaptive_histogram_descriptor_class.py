from concurrent.futures import ThreadPoolExecutor

import numpy
from PIL import Image

from slide_analysis_service.descriptors.constants import *


class AdaptiveHistogramDescriptor:
    def __init__(self, settings=None):
        self.settings = settings

        """
        Palette extraction process can be found in adaptive-color-palette.ipynb
        """
        palette_raw = [250, 247, 245, 115, 70, 114, 245, 231, 234, 234, 199, 210, 148, 103, 140,
                       206, 166, 184, 103, 58,
                       105, 199, 152, 177, 180, 136, 167, 215, 183, 199, 168, 119, 151, 239, 214,
                       216, 80, 40, 86, 137,
                       89, 133, 241, 217, 229, 229, 185, 202, 134, 86, 122, 185, 149, 173, 210, 170,
                       196, 216, 198, 207,
                       91, 52, 101, 176, 132, 154, 154, 116, 146, 122, 83, 119, 212, 180, 187, 171,
                       123, 163, 89, 50, 91,
                       164, 107, 144, 85, 44, 99, 100, 54, 91, 244, 227, 219, 196, 139, 170, 69, 28,
                       76, 131, 76, 117,
                       123, 84, 131, 219, 211, 215, 142, 99, 123, 185, 164, 180, 58, 24, 73, 120,
                       75, 130, 238, 203, 227,
                       228, 182, 188, 218, 214, 229, 228, 171, 198, 203, 155, 195, 228, 170, 185,
                       155, 119, 163, 133, 76,
                       131, 181, 147, 156, 197, 136, 154, 214, 202, 227, 154, 131, 152, 184, 167,
                       197, 98, 45, 88, 186,
                       181, 200, 109, 67, 92, 55, 20, 59, 198, 148, 156, 155, 133, 165, 92, 66, 106,
                       198, 122, 169, 124,
                       99, 134, 171, 106, 164, 165, 91, 139, 214, 194, 188, 61, 33, 79, 184, 153,
                       195, 187, 178, 185, 197,
                       121, 150, 98, 46, 100, 47, 11, 55, 231, 195, 188, 229, 153, 179, 152, 107,
                       162, 122, 98, 122, 166,
                       102, 122, 68, 24, 60, 220, 226, 236, 251, 242, 220, 165, 89, 120, 50, 13, 67,
                       230, 154, 198, 155,
                       149, 171, 236, 187, 227, 205, 138, 196, 212, 186, 227, 150, 114, 124, 131,
                       60, 109, 169, 115, 124,
                       91, 65, 92, 188, 194, 210, 180, 138, 195, 134, 70, 91, 196, 107, 145, 76, 35,
                       60, 111, 60, 130,
                       226, 139, 178, 150, 91, 163, 154, 146, 154, 204, 163, 156, 131, 58, 88, 124,
                       115, 140, 71, 29, 97,
                       182, 162, 156, 221, 225, 220, 166, 92, 163, 181, 123, 196, 136, 83, 92, 228,
                       151, 154, 237, 210,
                       189, 234, 170, 226, 194, 109, 166, 186, 196, 229, 116, 82, 93, 60, 32, 61,
                       185, 186, 226, 162, 76,
                       114, 157, 162, 180, 154, 151, 197, 196, 125, 194, 61, 36, 97, 227, 141, 196,
                       29, 4, 48, 156, 164,
                       200, 92, 82, 111, 207, 170, 228, 61, 29, 96, 227, 138, 151, 220, 209, 189,
                       65, 14, 56, 130, 61,
                       131, 104, 38, 59, 232, 162, 156, 151, 137, 197, 199, 116, 124, 92, 57, 131,
                       194, 106, 125, 161, 76,
                       136, 119, 115, 122, 44, 3, 28, 206, 154, 226, 189, 192, 187, 94, 65, 130,
                       173, 130, 124, 185, 168,
                       226, 220, 241, 250, 165, 86, 93, 125, 117, 163, 188, 211, 231, 151, 128, 125,
                       226, 125, 163, 133,
                       76, 161, 186, 177, 157, 196, 178, 155, 98, 31, 75, 83, 52, 62, 67, 14, 67,
                       130, 45, 80, 157, 117,
                       194, 100, 25, 56, 143, 98, 94, 119, 92, 163, 127, 110, 165, 198, 129, 124,
                       94, 82, 132, 31, 14, 66,
                       127, 135, 158, 123, 129, 163, 65, 17, 31, 225, 121, 154, 61, 53, 90, 128, 45,
                       101, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.palette = Image.new('P', (16, 16))
        self.palette.putpalette(palette_raw)

    def calc(self, tile):
        img_conv = tile.data.convert('RGB').quantize(palette=self.palette)
        value = numpy.histogram(numpy.array(img_conv).flatten(), bins=numpy.arange(0, COLOR_RANGE + 1))[0]
        value = value / numpy.sum(value)
        return value

    def get_descriptor_object(self, tile_stream):
        with ThreadPoolExecutor() as executor:
            descr_arr = list(executor.map(self.calc, tile_stream))
            return {
                "descriptor_array": descr_arr
            }

    @staticmethod
    def name():
        return 'Adaptive Intensity histogram'
