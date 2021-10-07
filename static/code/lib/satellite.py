from . import three
from . import orb
from .axes import Axes, BODY_FIXED, ECLIPTIC
from .utils import js_time, calculate_distance, assign_xyz_vector


class Satellite:

    def __init__(
            self, scene, mesh=None, model=None, texture=None,
            scale=1, shadow=True):
        self.scene = scene
        self.mesh = mesh
        self.model = model
        self.texture = texture
        self.scale = scale
        self.shadow = shadow

        self.update_position_callbacks = []
        self.update_orientation_callbacks = []
        self.tle = None

        # create sprite, to be shown instead of mesh when camera is far away
        self.sprite = three.Sprite(three.SpriteMaterial({
            'map': three.TextureLoader().load("static/img/sprite_sat.png"),
            'sizeAttenuation': False}))
        self.sprite.scale.set(0.04, 0.04)
        self.sprite.visible = False
        self.scene.scene.add(self.sprite)

        if mesh and model:
            raise ValueError("Either provide a mesh or a model.")

        if model:
            three.OBJLoader().load(model, self._obj_loaded)
        else:
            self.create_axes()

        self.scene.objects.append(self)

    def create_axes(self):
        self.axes = {
            ECLIPTIC: Axes(self.scene, self),
            BODY_FIXED: Axes(self.scene, self)}

    def _obj_loaded(self, obj):
        self.mesh = obj
        self.mesh.scale.set(self.scale, self.scale, self.scale)
        self.mesh.traverse(self._traverse)
        if self.shadow:
            self.mesh.castShadow = True
            self.mesh.receiveShadow = True
        self.scene.scene.add(self.mesh)
        self.create_axes()

    def _traverse(self, node):
        texture = three.TextureLoader().load(self.texture)
        material = three.MeshPhongMaterial({'map': texture})
        node.material = material

    def set_tle(self, tle):
        self.tle = tle
        self.tle_orb = orb.SGP4(self.tle)
        self.vsop = orb.VSOP('Earth')

    def update(self, time):
        if self.mesh is None:
            return  # model not fully loaded yet
        self.update_position(time)
        self.update_orientation(time)

    def update_position(self, time):
        if self.tle:
            pos_earth = self.vsop.xyz(js_time(time))
            pos_tle = self.tle_orb.xyz(js_time(time))
            pos_rel = orb.EquatorialToEcliptic({"equatorial": {
                'x': pos_tle.x, 'y': pos_tle.y, 'z': pos_tle.z}})
            self.mesh.position.z = pos_earth.x * orb.Const.AU + pos_rel.x
            self.mesh.position.x = pos_earth.y * orb.Const.AU + pos_rel.y
            self.mesh.position.y = pos_earth.z * orb.Const.AU + pos_rel.z

        for callback in self.update_position_callbacks:
            callback(self, time)

        assign_xyz_vector(self.sprite.position, self.mesh.position)
        self.axes[BODY_FIXED].update_position()
        self.axes[ECLIPTIC].update_position()

    def update_orientation(self, time):
        for callback in self.update_orientation_callbacks:
            callback(self, time)
        self.axes[BODY_FIXED].axes.rotation.copy(self.mesh.rotation)
        # TODO: set rotation of self.axes[BODY_FIXED]

    def show_mesh_or_sprite(self):
        if self.mesh is None:
            return
        # decide whether to show mesh or sprite
        v1, v2 = three.Vector3(), three.Vector3()
        self.scene.camera.camera.getWorldPosition(v1)
        self.mesh.getWorldPosition(v2)
        distance = calculate_distance(v1, v2)
        if distance > 10000:
            self.sprite.visible = True
            self.mesh.visible = False
        else:
            self.sprite.visible = False
            self.mesh.visible = True
