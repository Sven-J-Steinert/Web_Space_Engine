from browser import document, window

from . import three


class Camera:
    FOV = 75
    FRUSTRUM_NEAR = 0.1
    FRUSTRUM_FAR = 3e8

    def __init__(self, scene, type='perspective', control='orbit'):
        self.scene = scene
        self.camera = three.PerspectiveCamera(
            Camera.FOV,
            window.innerWidth / window.innerHeight,
            Camera.FRUSTRUM_NEAR, Camera.FRUSTRUM_FAR)
        scene.camera = self  # refer to this class from scene class

        self.fake_camera = self.camera.clone()
        self.controls = three.OrbitControls(self.fake_camera)

        self.renderer = three.WebGLRenderer({'antialias': True})
        self.renderer.capabilities.logarithmicDepthBuffer = True
        self.renderer.shadowMap.enabled = True
        self.renderer.shadowMap.type = 2
        self.renderer.setPixelRatio(window.devicePixelRatio)
        self.renderer.setSize(window.innerWidth, window.innerHeight)
        self.renderer.setClearColor(0x000000, 1)
        document <= self.renderer.domElement
        self.renderer.render(self.scene.scene, self.camera)

    def render_scene(self):
        self.camera.copy(self.fake_camera)
        self.controls.update()
        self.renderer.render(self.scene.scene, self.camera)

    def window_resize(self):
        self.fake_camera.aspect = window.innerWidth / window.innerHeight
        self.fake_camera.updateProjectionMatrix()
        self.renderer.setSize(window.innerWidth, window.innerHeight)
        self.renderer.render(self.scene.scene, self.camera)

    def go_to(self, element):
        element.mesh.add(self.camera)
        self.scene.selected_object = element
        if hasattr(element.mesh, 'geometry'):
            self.fake_camera.position.x =\
                element.mesh.geometry.boundingSphere.radius * 1.5
            self.fake_camera.position.y =\
                element.mesh.geometry.boundingSphere.radius * 1.5
            self.fake_camera.position.z =\
                element.mesh.geometry.boundingSphere.radius * 1.5
        elif hasattr(element, 'scale'):
            self.fake_camera.position.x = element.scale * 500
            self.fake_camera.position.y = element.scale * 500
            self.fake_camera.position.z = element.scale * 500

    def set_reference_axes(self, axes):
        axes.axes.add(self.camera)
