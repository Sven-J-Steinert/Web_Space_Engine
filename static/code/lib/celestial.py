import math

from . import three
from . import orb
from .utils import assign_xyz_vector, calculate_distance, js_time
from .astronomical import calculate_sideral_degree
from .axes import Axes, BODY_FIXED, J2000, ECLIPTIC


class EclipticGrid:

    def __init__(self, scene, radius=1):
        self.scene = scene
        self.grid = three.PolarGridHelper(radius * orb.Const.AU, 16, 8, 64)
        self.scene.scene.add(self.grid)


def create_celestial_object(
        geometry, texture_path, material_type='basic', shadow=True):
    texture = three.TextureLoader().load(texture_path)
    if material_type == 'basic':
        material = three.MeshBasicMaterial(dict(map=texture))
    elif material_type == 'standard':
        material = three.MeshStandardMaterial(dict(map=texture))
    object = three.Mesh(geometry, material)
    if shadow:
        object.castShadow = True
        object.receiveShadow = True
    geometry.computeBoundingSphere()
    return object


class CelestialObject:

    def __init__(
            self, scene, radius, texture, material_type, shadow):
        self.scene = scene
        self.scene.objects.append(self)  # add to list of scene objects
        # create mesh
        self.mesh = create_celestial_object(
            three.SphereGeometry(radius, 100, 100),
            texture, material_type, shadow)
        self.scene.scene.add(self.mesh)
        # additional axes need to be added individually for each class
        self.axes = {BODY_FIXED: Axes(self.scene, self)}
        # create sprite, to be shown instead of mesh when camera is far away
        self.sprite = three.Sprite(three.SpriteMaterial({
            'map': three.TextureLoader().load("static/img/sprite.png"),
            'sizeAttenuation': False}))
        self.sprite.scale.set(0.04, 0.04)
        self.sprite.visible = False
        self.scene.scene.add(self.sprite)

    def update(self, time):
        # position
        self.update_position(time)
        self.axes[BODY_FIXED].update_position()

        # rotation
        e = three.Euler()
        e._z = math.radians(self.INCLINATION_TO_ECLIPTIC)
        e._y = math.radians(self.TEXTURE_OFFSET)
        e._order = 'ZYX'
        self.mesh.setRotationFromEuler(e)
        self.axes[BODY_FIXED].axes.setRotationFromEuler(e)

    def update_position(self, time):
        # calculate position of celestial object from VSOP
        position = self.vsop.xyz(js_time(time))
        self.mesh.position.z = position.x * orb.Const.AU
        self.mesh.position.x = position.y * orb.Const.AU
        self.mesh.position.y = position.z * orb.Const.AU
        assign_xyz_vector(self.sprite.position, self.mesh.position)

    def show_mesh_or_sprite(self):
        # decide whether to show mesh or sprite
        v1, v2 = three.Vector3(), three.Vector3()
        self.scene.camera.camera.getWorldPosition(v1)
        self.mesh.getWorldPosition(v2)
        distance = calculate_distance(v1, v2)
        if distance > 100 * self.mesh.geometry.boundingSphere.radius:
            self.sprite.visible = True
            self.mesh.visible = False
        else:
            self.sprite.visible = False
            self.mesh.visible = True


class Sun(CelestialObject):

    SIDERAL_ROTATION_PERIOD = 24.47  # days
    RADIUS = orb.Const.Sun.radius

    def __init__(self, scene):
        super().__init__(
            scene, self.RADIUS, 'static/img/sun.jpg',
            material_type='basic', shadow=False)
        # increase sprite size for sun
        self.sprite = three.Sprite(three.SpriteMaterial({
            'map': three.TextureLoader().load("static/img/sprite_sun.png"),
            'sizeAttenuation': False}))
        self.sprite.scale.set(0.08, 0.08)
        self.sprite.visible = False
        self.scene.scene.add(self.sprite)
        # add a point light to simulate sun light
        self.point_light = three.PointLight()
        self.scene.scene.add(self.point_light)

    def update(self, time):
        # no need to update, sun rotation is not considered
        pass


class Earth(CelestialObject):

    RADIUS = orb.Const.Earth.radius
    INCLINATION_TO_ECLIPTIC = -23.4
    TEXTURE_OFFSET = -90

    def __init__(self, scene):
        super().__init__(
            scene, self.RADIUS, 'static/img/earth.jpg',
            material_type='standard', shadow=True)
        self.axes[ECLIPTIC] = Axes(self.scene, self)
        self.axes[J2000] = Axes(self.scene, self)
        self.vsop = orb.VSOP('Earth')

    def update(self, time):
        # position of earth and axes
        self.update_position(time)
        self.axes[ECLIPTIC].update_position()
        self.axes[BODY_FIXED].update_position()
        self.axes[J2000].update_position()

        # rotation of earth and axes
        e = three.Euler()
        e._z = math.radians(self.INCLINATION_TO_ECLIPTIC)
        self.axes[J2000].axes.setRotationFromEuler(e)
        sideral_degree = calculate_sideral_degree(time)
        e._y = math.radians(sideral_degree + self.TEXTURE_OFFSET)
        e._order = 'ZYX'
        self.mesh.setRotationFromEuler(e)
        self.axes[BODY_FIXED].axes.setRotationFromEuler(e)


class Moon(CelestialObject):

    RADIUS = orb.Const.Moon.radius
    INCLINATION_TO_ECLIPTIC = -1.54
    TEXTURE_OFFSET = 90

    def __init__(self, scene):
        super().__init__(
            scene, self.RADIUS, 'static/img/moon.jpg',
            material_type='standard', shadow=True)
        self.vsop = orb.VSOP('Earth')
        self.luna = orb.Luna()

    def update(self, time):
        # position of moon and axes
        position_earth = self.vsop.xyz(js_time(time))
        position_moon = self.luna.xyz(js_time(time))
        self.mesh.position.z =\
            position_earth.x * orb.Const.AU + position_moon.x
        self.mesh.position.x =\
            position_earth.y * orb.Const.AU + position_moon.y
        self.mesh.position.y =\
            position_earth.z * orb.Const.AU + position_moon.z
        assign_xyz_vector(self.sprite.position, self.mesh.position)
        self.axes[BODY_FIXED].update_position()

        # rotation of moon and axes
        e = three.Euler()
        e._z = math.radians(self.INCLINATION_TO_ECLIPTIC)
        self.axes[BODY_FIXED].axes.setRotationFromEuler(e)
        e._y = math.radians(self.TEXTURE_OFFSET)
        e._order = 'ZYX'
        self.mesh.setRotationFromEuler(e)

        # self.mesh.lookAt(
        #     position_earth.y * orb.Const.AU,
        #     position_earth.z * orb.Const.AU,
        #     position_earth.x * orb.Const.AU)


class Mercury(CelestialObject):

    RADIUS = orb.Const.Mercury.radius
    INCLINATION_TO_ECLIPTIC = -7.00487
    TEXTURE_OFFSET = -90

    def __init__(self, scene):
        super().__init__(
            scene, self.RADIUS, 'static/img/mercury.jpg',
            material_type='standard', shadow=True)
        self.vsop = orb.VSOP('Mercury')


class Venus(CelestialObject):

    RADIUS = orb.Const.Venus.radius
    INCLINATION_TO_ECLIPTIC = -3.395
    TEXTURE_OFFSET = -90

    def __init__(self, scene):
        super().__init__(
            scene, self.RADIUS, 'static/img/venus.jpg',
            material_type='standard', shadow=True)
        self.vsop = orb.VSOP('Venus')


class Mars(CelestialObject):

    RADIUS = orb.Const.Mars.radius
    INCLINATION_TO_ECLIPTIC = -1.85
    TEXTURE_OFFSET = -90

    def __init__(self, scene):
        super().__init__(
            scene, self.RADIUS, 'static/img/mars.jpg',
            material_type='standard', shadow=True)
        self.vsop = orb.VSOP('Mars')


class Jupiter(CelestialObject):

    RADIUS = orb.Const.Mars.radius
    INCLINATION_TO_ECLIPTIC = -1.305
    TEXTURE_OFFSET = -90

    def __init__(self, scene):
        super().__init__(
            scene, self.RADIUS, 'static/img/jupiter.jpg',
            material_type='standard', shadow=True)
        self.vsop = orb.VSOP('Jupiter')
