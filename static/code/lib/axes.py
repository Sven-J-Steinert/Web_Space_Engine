from . import three
from .utils import assign_xyz_vector


BODY_FIXED = 'body'
J2000 = 'j2000'
ECLIPTIC = 'ecliptic'


class Axes:

    def __init__(self, scene, element):
        self.scene = scene
        self.element = element

        if 'geometry' in element.mesh:
            self.axes = three.AxesHelper(
                1.5 * element.mesh.geometry.boundingSphere.radius)
        else:
            self.axes = three.AxesHelper(100)
        assign_xyz_vector(self.axes.position, element.mesh.position)
        scene.scene.add(self.axes)

    def update_position(self, time=None):
        # assign the element's position to the axes
        assign_xyz_vector(self.axes.position, self.element.mesh.position)
