import numpy
import matplotlib.cm as cm
from PIL import Image

from slide_analysis_service.descriptor_database_service.descriptor_database_read_service_class \
    import DescriptorDatabaseReadService
from slide_analysis_service.utils.functions import get_tile_from_coordinates, \
    get_similarity_map_shape, get_tiles_coords_from_indexes


class SearchService:
    def __init__(self, dbpath, imagepath):
        ddrs = DescriptorDatabaseReadService(dbpath)
        self.descriptor = ddrs.descriptor_class(ddrs.descriptor_params)
        self.info_obj = ddrs.info_obj
        self.descriptors_array = ddrs.descriptors_array
        self.imagepath = imagepath

    def convert_to_tile_coords(self, indexes):
        return get_tiles_coords_from_indexes(indexes,
                                             self.info_obj['step'],
                                             self.info_obj['img_width'],
                                             self.info_obj['img_height'])

    def find_similar(self, rect_top_left_width_height_tuple, n, similarity):
        (top, left, width, height) = rect_top_left_width_height_tuple
        tile = get_tile_from_coordinates(self.imagepath, *(top, left), *(width, height))
        descriptor = self.descriptor.calc(tile)
        distances = similarity.compare(self.descriptors_array,
                                       descriptor)
        indexes = numpy.argsort(distances)

        return {
            "top_n": self.convert_to_tile_coords(indexes[-n:]),
            "sim_map": Image.fromarray(self.create_img_map(self.get_map(distances)), 'RGB')
        }

    def get_map(self, sims):
        return sims.reshape(get_similarity_map_shape(self.info_obj['img_width'],
                                                     self.info_obj['img_height'],
                                                     self.info_obj['step']))

    @staticmethod
    def create_img_map(sim_map):
        map = cm.ScalarMappable(cmap='jet').to_rgba(sim_map, bytes=True)
        shape = map.shape
        map = map.reshape([shape[1], shape[0], shape[2]])
        return map
