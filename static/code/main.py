from browser import document, window, bind, timer
from datetime import datetime

from lib import three
from lib import camera
from lib import scene
from lib.celestial import EclipticGrid, Earth, Sun, Moon, Mercury, Venus,\
    Mars, Jupiter
from lib.satellite import Satellite


scene = scene.Scene()
scene.scene.add(three.AmbientLight(0x404040, 0.5))

camera = camera.Camera(scene)

# ecliptic grid
ecliptic_grid = EclipticGrid(scene)

# sun and planets
sun = Sun(scene)
earth = Earth(scene)
moon = Moon(scene)
mercury = Mercury(scene)
venus = Venus(scene)
mars = Mars(scene)
jupiter = Jupiter(scene)

camera.go_to(earth)

# CubeSat http://www.celestrak.com/NORAD/elements/active.txt
sat = Satellite(
    scene, model="static/model/cluster.obj", texture="static/img/cluster.png")
sat.set_tle({
    'first_line': '1 44533U 19022K   20085.24091529  .00001920  00000-0  76189-4 0  9997',
    'second_line': '2 44533  51.6417  77.1082 0011268   3.5862 356.5215 15.30556777 29242'})


# define a callback for updating satellite orientation
def sat_rotation(self, time):
    import math
    # a full rotation around y axis in 4 seconds
    e = three.Euler()
    t = (time.second + time.microsecond / 1000000) % 4
    e._y = math.radians(t * 360/4)
    self.mesh.setRotationFromEuler(e)


#sat.update_orientation_callbacks.append(sat_rotation)


""" Animation """


class Animation:
    def __init__(self):
        self.running = False
        self.handle = None
        self.last_time = datetime.utcnow()
        self.i = 0

    def run(self):
        if not self.running:
            self.running = True
            self.animate()

    def stop(self):
        if self.running:
            self.running = False
            timer.cancel_animation_frame(self.handle)
            self.handle = None

    def animate(self, *args, **kwargs):
        self.handle = timer.request_animation_frame(self.animate)
        # do calculations only every n frame
        if self.i % 1 == 0:
            for object in scene.objects:
                object.update(scene.get_time())
                object.show_mesh_or_sprite()
                document['display_time'].text = scene.get_time_str()
                sat_pos = sat.get_position()
                if sat_pos != None:
                    document['value_1'].text = "{0:.2f}".format(sat_pos[0])
                    document['value_2'].text = "{0:.2f}".format(sat_pos[1])
                    document['value_3'].text = "{0:.2f}".format(sat_pos[2])

                    if sat_pos[0] > 0:
                        document['value_4'].text = "Online"
                        document['value_4'].style.color = "#4AF626"
                    else:
                        document['value_4'].text = "Offline"
                        document['value_4'].style.color = "red"
            scene.tick()
        self.i += 1
        camera.render_scene()


""" Actions """


# Time

@bind(document['btn_time_faster'], 'click')
def btn_time_faster(e):
    scene.faster()


@bind(document['btn_time_slower'], 'click')
def btn_time_slower(e):
    scene.slower()


@bind(document['btn_time_freeze'], 'click')
def btn_time_freeze(e):
    scene.stop()


@bind(document['btn_time_forward'], 'click')
def btn_time_forward(e):
    scene.play()


@bind(document['btn_time_backward'], 'click')
def btn_time_backward(e):
    scene.play(forward=False)


@bind(document['btn_time_realtime'], 'click')
def btn_time_realtime(e):
    scene.realtime()


@bind(document['btn_time_set'], 'click')
def btn_time_set(e):
    # TODO
    text = input("Enter UTC time in format:\nYYYY-mm-dd HH:MM:SS")
    try:
        time = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
        scene.set_time(time)
    except Exception:
        window.alert("Wrong time format!")


@bind(document['btn_goto_sun'], 'click')
def btn_goto_sun(e):
    camera.go_to(sun)


@bind(document['btn_goto_mercury'], 'click')
def btn_goto_mercury(e):
    camera.go_to(mercury)


@bind(document['btn_goto_venus'], 'click')
def btn_goto_venus(e):
    camera.go_to(venus)


@bind(document['btn_goto_earth'], 'click')
def btn_goto_earth(e):
    camera.go_to(earth)


@bind(document['btn_goto_moon'], 'click')
def btn_goto_moon(e):
    camera.go_to(moon)


@bind(document['btn_goto_mars'], 'click')
def btn_goto_mars(e):
    camera.go_to(mars)


@bind(document['btn_goto_jupiter'], 'click')
def btn_goto_jupiter(e):
    camera.go_to(jupiter)


@bind(document['btn_goto_sat'], 'click')
def btn_goto_sat(e):
    camera.go_to(sat)


@bind(document['btn_change_axes'], 'click')
def btn_change_axes(e):
    if scene.selected_object:
        info = '\n'.join(scene.selected_object.axes.keys())
        axes = input(info).lower()
        if axes in scene.selected_object.axes:
            camera.set_reference_axes(scene.selected_object.axes[axes])


@bind(document['btn_show_orbits'], 'click')
def btn_show_orbits(e):
    scene.faster()


""" Events """


def on_resize(e):
    camera.window_resize()


window.onresize = on_resize
animation = Animation()
animation.run()
