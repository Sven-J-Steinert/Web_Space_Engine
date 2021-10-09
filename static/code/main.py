from browser import document, window, bind, timer
from datetime import datetime

from lib import three
from lib import camera
from lib import scene
from lib.celestial import EclipticGrid, Earth, Sun, Moon, Mercury, Venus,\
    Mars, Jupiter
from lib.satellite import Satellite
from lib.groundstation import Groundstation
from lib.antenna import Antenna
from lib.customer import Customer

import math
from lib import orb

# DEBUGGING
#document['title'].text = "1"

camera_item = None
groundstation_selected = None

def setup_run():
    global scene, camera,camera_item, sat
    global sun, earth, moon, mercury, venus, mars, jupiter
    scene = scene.Scene()
    scene.scene.add(three.AmbientLight(0x404040, 0.5))

    camera_item = camera.Camera(scene)

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

    camera_item.go_to(earth)

    # CubeSat http://www.celestrak.com/NORAD/elements/active.txt
    sat = Satellite(
        scene, model="static/model/cluster.obj", texture="static/img/cluster.png")

    #first_line, second_line = document['tle_orbit'].value.split('\n')
    first_line = document['tle_orbit'].value.split('\n')[0]
    second_line = document['tle_orbit'].value.split('\n')[1]
    sat_orbit = Orbit(first_line,second_line)
    sat.set_tle(sat_orbit.json)
    #sat.set_tle({
    #    'first_line': '1 44533U 19022K   20085.24091529  .00001920  00000-0  76189-4 0  9997',
    #    'second_line': '2 44533  51.6417  77.1082 0011268   3.5862 356.5215 15.30556777 29242'})

    camera_item.set_reference_axes(scene.selected_object.axes['ecliptic'])



def convert_lat_lon(lat,lon):
    # make up for shifted axis
    #lat = lat + 90
    #lon = lon + 90

    # convert ° to rad
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    x = math.sin(math.pi/2-lat_rad) * math.cos(lon_rad)
    y = math.sin(math.pi/2-lat_rad) * math.sin(lon_rad)
    z = math.cos(math.pi/2-lat_rad)

    x = x * (orb.Const.Earth.radius + 10)
    y = y * (orb.Const.Earth.radius + 10)
    z = z * (orb.Const.Earth.radius + 10)

    return [x,y,z]

""" Animation """


class Animation:
    def __init__(self):
        self.running = False
        self.handle = None
        self.last_time = datetime.utcnow()
        self.i = 0

        self.gs_sprite = three.Sprite(three.SpriteMaterial({
            'map': three.TextureLoader().load("static/img/sprite_sat.png"),
            'sizeAttenuation': False}))
        self.gs_sprite.scale.set(0.06, 0.06)
        scene.scene.add(self.gs_sprite)

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
                    document['relative_x'].text = "{0:.2f}".format(sat_pos[0])
                    document['relative_y'].text = "{0:.2f}".format(sat_pos[1])
                    document['relative_z'].text = "{0:.2f}".format(sat_pos[2])
                    # norm of vector -> subtract earth radius
                    global altitude
                    altitude = vector_norm(sat_pos) - orb.Const.Earth.radius
                    document['altitude'].text = "{0:.2f}".format(altitude)

                    # display groundstation
                    document['Groundstation_selected'].text =  gs_list[groundstation_selected].name + " ["+ gs_list[groundstation_selected].id +"]"

                    rel_gs_x, rel_gs_y, rel_gs_z = convert_lat_lon(gs_list[groundstation_selected].Lat, gs_list[groundstation_selected].Lon)

                    gs_pos_rel = orb.EquatorialToEcliptic({"equatorial": {
                       'x': rel_gs_x, 'y': rel_gs_y, 'z': rel_gs_z}})

                    pos_earth = sat.get_position_earth()

                    abs_gs_z = pos_earth.x * orb.Const.AU + gs_pos_rel.x
                    abs_gs_x = pos_earth.y * orb.Const.AU + gs_pos_rel.y
                    abs_gs_y = pos_earth.z * orb.Const.AU + gs_pos_rel.z

                    self.gs_sprite.position.set( abs_gs_x, abs_gs_y, abs_gs_z);

                    document['lat_lon'].text = [gs_list[groundstation_selected].Lat, gs_list[groundstation_selected].Lon]

                    # ground station coverage checking

                    # Placeholder
                    if sat_pos[0] > 0 and sat_pos[1] > 0 and sat_pos[2] > 0:
                        document['status'].text = "Online"
                        document['status'].style.color = "#4AF626"
                    else:
                        document['status'].text = "Offline"
                        document['status'].style.color = "red"
            scene.tick()
        self.i += 1
        camera_item.render_scene()


# define a callback for updating satellite orientation
def sat_rotation(self, time):
    import math
    # a full rotation around y axis in 4 seconds
    e = three.Euler()
    t = (time.second + time.microsecond / 1000000) % 4
    e._y = math.radians(t * 360/4)
    self.mesh.setRotationFromEuler(e)


#sat.update_orientation_callbacks.append(sat_rotation)

def calculation(customer):
    global math

    EIRP = customer.EIRP            #Effective Isotropic Radiated Power
    LPolarization = customer.LPolarization  #Polarization Loss
    G_T = customer.G_T              #Gain Rx over Temperature System
    DataRate = customer.DataRate    #Data rate
    Lpoint = customer.Lpoint        #Lpoint Receiver pointing loss
    Lmod_demod = customer.Lmod_demod #Mod_demod loss
    f = customer.f
    d = customer.d

    # convert to dB
    DataRate = 10* math.log10(DataRate*1000)

    FLS = -(20 * math.log10(f*d) + 92.45 )# you need the math library or so for that
    #FIXED VALUES FOR THIS EXAMPLE
    Lrain = -0.04
    Lat = -0.22
    Lscin = -0.38
    k = 228.6
    Required = 13.5

    Lp = FLS + Lrain + Lat + LPolarization + Lscin

    Achived_CNo = G_T + EIRP + k + Lp + Lpoint + Lmod_demod
    Achived_EB = Achived_CNo - DataRate
    LinkMargin = Achived_EB - Required

    return [Achived_CNo, Achived_EB, LinkMargin]


def main_calculation():

    EIRP = document['EIRP'].value
    LPolarization= document['Polarization'].value
    G_T= document['G_T'].value
    DataRate= document['data_rate'].value
    Lpoint= document['Lpoint'].value
    Lmod_demod= document['Lmod_demod'].value
    f = document['Frequency'].value
    d = document['d'].value


    if EIRP == "" or LPolarization == "" or G_T == "" or DataRate == "" or Lpoint == "" or Lmod_demod == "" or f == "" or  d == "":
        document['WARNING'].style.display = "block"
    else:
        document['WARNING'].style.display = "none"
        customer = Customer(
            EIRP = EIRP,
            LPolarization= LPolarization,
            G_T= G_T,
            DataRate= DataRate,
            Lpoint= Lpoint,
            Lmod_demod= Lmod_demod,
            f = f,
            d = d
            )

        # verification
        # customer = Customer(
        #     EIRP = 60,
        #     LPolarization= 2.3,
        #     G_T= -37.99,
        #     DataRate= 48.06,
        #     Lpoint= -0.5,
        #     Lmod_demod= -1,
        #     f = 2.028, # Frequency GHz
        #     d = 2045.53 # highest distance between sat and gs
        #     )

        # expected Result -> 24.40

        #if document['up_down'].text == "Uplink":
        #    result = uplink_calculation(customer)

        #if document['up_down'].text == "Downlink":
        #    result = downlink_calculation(customer)

        result = calculation(customer)

        document['result_container'].style.display = "block"
        document['result_C_N0'].value = "{0:.2f}".format(result[0])
        document['result_Eb_N0'].value = "{0:.2f}".format(result[1])
        document['result_LinkMargin'].value = "{0:.2f}".format(result[2])

        if result[2] >= 3:
            document['result_LinkMargin_info'].style.color = "#4AF626"
            document['result_LinkMargin_info'].text = ">3 dB ECSS"
        else:
            document['result_LinkMargin_info'].style.color = "red"
            document['result_LinkMargin_info'].text = "<3 dB ECSS"


def vector_norm(x):
    result = math.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
    return result

""" Actions """

@bind(document['run'], 'click')
def btn_run(e):
    if document['display_groundstation'].text != "" and document['tle_orbit'].value != "":
        document['WARNING'].style.display = "none"
        setup_run()
        run_simulation()
    else:
        document['WARNING'].style.display = "block"


@bind(document['compute'], 'click')
def btn_compute(e):
    if document['display_groundstation'].text == "Goldstone":
        document['deepspace'].style.display = "Block"
    main_calculation()


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
    camera_item.go_to(sun)


@bind(document['btn_goto_mercury'], 'click')
def btn_goto_mercury(e):
    camera_item.go_to(mercury)


@bind(document['btn_goto_venus'], 'click')
def btn_goto_venus(e):
    camera_item.go_to(venus)


@bind(document['btn_goto_earth'], 'click')
def btn_goto_earth(e):
    camera_item.go_to(earth)


@bind(document['btn_goto_moon'], 'click')
def btn_goto_moon(e):
    camera_item.go_to(moon)


@bind(document['btn_goto_mars'], 'click')
def btn_goto_mars(e):
    camera_item.go_to(mars)


@bind(document['btn_goto_jupiter'], 'click')
def btn_goto_jupiter(e):
    camera_item.go_to(jupiter)


@bind(document['btn_goto_sat'], 'click')
def btn_goto_sat(e):
    camera_item.go_to(sat)


@bind(document['btn_change_axes'], 'click')
def btn_change_axes(e):
    global camera_item
    if scene.selected_object:
        info = '\n'.join(scene.selected_object.axes.keys())
        axes = input(info).lower()
        if axes in scene.selected_object.axes:
            camera_item.set_reference_axes(scene.selected_object.axes[axes])

def show_groundstations(band_number):
    for i in range(len(gs_list)):
        document['groundstation_'+str(i)].text = gs_list[i].id
    # 1     2   3    4    5   6    7  8   9
    # UHF, L ,  S , SGLS, C , X , Ku, K, Ka
    for i in range(len(gs_list)):
        if gs_list[i].bands[band_number-1]:
            document['groundstation_'+str(i)].style.display = "block"
        else:
            document['groundstation_'+str(i)].style.display = "none"

@bind(document['select_UHF'], 'click')
def btn_show_UHF(e):
    document['display_band'].text = "UHF"
    show_groundstations(1) # band_index

@bind(document['select_L'], 'click')
def btn_show_L(e):
    document['display_band'].text = "L"
    show_groundstations(2) # band_index

@bind(document['select_S'], 'click')
def btn_show_S(e):
    document['display_band'].text = "S"
    show_groundstations(3) # band_index

@bind(document['select_SGLS'], 'click')
def btn_show_SGLS(e):
    document['display_band'].text = "SGLS"
    show_groundstations(4) # band_index

@bind(document['select_C'], 'click')
def btn_show_C(e):
    document['display_band'].text = "C"
    show_groundstations(5) # band_index

@bind(document['select_X'], 'click')
def btn_show_X(e):
    document['display_band'].text = "X"
    show_groundstations(6) # band_index

@bind(document['select_Ku'], 'click')
def btn_show_Ku(e):
    document['display_band'].text = "Ku"
    show_groundstations(7) # band_index

@bind(document['select_K'], 'click')
def btn_show_K(e):
    document['display_band'].text = "K"
    show_groundstations(8) # band_index

@bind(document['select_Ka'], 'click')
def btn_show_Ka(e):
    document['display_band'].text = "Ka"
    show_groundstations(9) # band_index

@bind(document['uplink'], 'click')
def btn_show_up(e):
    document['up_down'].text = "Uplink"
    document['G_T_label'].textContent = "Spacecraft G/T"
    document['Lpoint_label'].textContent = "Tx Pointing Loss"
    document['Lmod_demod_label'].textContent = "Rx Mod-Demod Loss"



@bind(document['downlink'], 'click')
def btn_show_down(e):
    document['up_down'].text = "Downlink"
    document['G_T_label'].textContent = "Groundstation G/T"
    document['Lpoint_label'].textContent = "Rx Pointing Loss"
    document['Lmod_demod_label'].textContent = "Tx Mod-Demod Loss"


# Groundstation Database
gs_list = []

gs_list.append(Groundstation(id='ESR',name='Esrange',bands=[True,True,True,False,False,True,False,False,False],Lat=67.88,Lon=21.07,altitude=341))
gs_list.append(Groundstation(id='INU',name='Inuvik',bands=[False,False,True,False,False,True,False,False,False],Lat=68.4,Lon=-133.5,altitude=51))
gs_list.append(Groundstation(id='NP', name='North Pole',bands=[False,False,True,False,False,True,False,False,False],Lat=65.8,Lon=-147.65,altitude=135))
gs_list.append(Groundstation(id='CLE',name='Clewiston',bands=[False,False,True,True,False,True,False,False,False],Lat=26.73,Lon=-82.03,altitude=3))
gs_list.append(Groundstation(id='SPO',name='South Point',bands=[False,False,True,False,False,True,True,False,False],Lat=19.02,Lon=-155.67,altitude=164))
gs_list.append(Groundstation(id='YAT',name='Yatharagga(WASC)',bands=[False,False,True,False,False,False,False,False,False],Lat=-29.08,Lon=115.58,altitude=280))
gs_list.append(Groundstation(id='DON',name='Dongara(WASC)',bands=[False,False,True,False,False,False,False,False,False],Lat=-29.05,Lon=115.35,altitude=280))
gs_list.append(Groundstation(id='STG',name='Santiago',bands=[False,False,True,False,False,False,False,False,False],Lat=-33.13,Lon=-70.67,altitude=698))
gs_list.append(Groundstation(id='PAR',name='Punta Arenas',bands=[False,False,True,False,False,True,False,False,False],Lat=-52.93,Lon=-70.85,altitude=88))
gs_list.append(Groundstation(id='FUC',name='Fucino',bands=[False,True,True,False,True,True,False,False,False],Lat=42,Lon=13.55,altitude=652))
gs_list.append(Groundstation(id='HAR',name='Hartebeesthoek',bands=[False,False,True,False,False,False,False,False,False],Lat=-25.64,Lon=28.08,altitude=1288))
gs_list.append(Groundstation(id='SVA',name='Svalbard',bands=[False,True,True,False,True,True,False,False,False],Lat=78.23,Lon=15.41,altitude=248))
gs_list.append(Groundstation(id='TRO',name='TrollSat',bands=[False,False,True,False,True,True,False,False,False],Lat=-72.02,Lon=2.53,altitude=1270))
gs_list.append(Groundstation(id='TMS',name='Tromso',bands=[False,True,True,False,False,True,False,False,False],Lat=69.39,Lon=18.56,altitude=4))
gs_list.append(Groundstation(id='GRI',name='Grimstad',bands=[False,False,False,False,False,True,False,False,False],Lat=58.34,Lon=8.59,altitude=28))
gs_list.append(Groundstation(id='PLL',name='Puertollano',bands=[False,False,True,False,False,True,False,False,False],Lat=38.69,Lon=-4.11,altitude=703))
gs_list.append(Groundstation(id='SGP',name='Singapore',bands=[False,False,True,False,False,True,False,False,False],Lat=1.35,Lon=103.82,altitude=55))
gs_list.append(Groundstation(id='MAU',name='Mauritius',bands=[False,False,True,False,False,True,False,False,False],Lat=-20.35,Lon=57.55,altitude=579))
gs_list.append(Groundstation(id='PAN',name='Panama',bands=[True,False,True,False,False,False,False,False,False],Lat=8.54,Lon=-80.78,altitude=1057))
gs_list.append(Groundstation(id='FBA',name='Fairbanks',bands=[False,False,True,False,False,True,False,False,False],Lat=64.80,Lon=-147.70,altitude=135))
gs_list.append(Groundstation(id='DUB',name='Dubai',bands=[False,False,True,False,False,True,False,False,False],Lat=25.20,Lon=55.27,altitude=0))
gs_list.append(Groundstation(id='HAR2',name='Hartebeesthoek',bands=[False,False,True,False,False,True,False,False,False],Lat=-25.64,Lon=28.08,altitude=1288))
gs_list.append(Groundstation(id='INU2',name='Inuvik',bands=[False,False,True,False,False,True,False,False,False],Lat=68.40,Lon=-133.50,altitude=51))
gs_list.append(Groundstation(id='DNS',name='Goldstone',bands=[False,False,True,False,False,True,False,False,True],Lat=35.43,Lon=116.89,altitude=900))

# 1     2   3    4    5   6    7  8   9
# UHF, L ,  S , SGLS, C , X , Ku, K, Ka

# map all functions to select groundstation
def addfunc(n):
    @bind(document['groundstation_'+str(n)], 'click')
    def addn(e):
        global groundstation_selected
        document['display_groundstation'].text = gs_list[n].name
        groundstation_selected = n
    return addn

for i in range(len(gs_list)):
    globals()['add{}'.format(i)] = addfunc(i)


antenna_list = []

antenna_list.append(Antenna(id='ESR_A',Gain = 12,Power = 7))
antenna_list.append(Antenna(id = 'Sat_A',Gain = 500,Power = 100))

class Orbit():
    def __init__(self,first_line,second_line,name=None):
        self.name = name
        self.first_line = first_line
        self.second_line = second_line
        self.json = {'first_line': self.first_line,
                     'second_line': self.second_line}
        self.text = self.first_line + '\n' + self.second_line

orbit_list = []


orbit_list.append( Orbit('1 44533U 19022K   20085.24091529  .00001920  00000-0  76189-4 0  9997','2 44533  51.6417  77.1082 0011268   3.5862 356.5215 15.30556777 29242','LEO') )   # LEO
orbit_list.append( Orbit('1 25544U 98067A   21281.73004796  .00003128  00000-0  65029-4 0  9990','2 25544  51.6444 141.3023 0004210  71.7185  11.5978 15.48952913306193','ISS') )   # ISS (ZARYA)
orbit_list.append( Orbit('1 20580U 90037B   21281.76424799  .00001000  00000-0  49416-4 0  9995','2 20580  28.4708  35.2711 0002511 198.5590 289.2049 15.09769068528135','Hubble') )   # Hubble

# map all functions to select groundstation
def addfunc_orbit(n):
    @bind(document['orbit_'+str(n)], 'click')
    def addn2(e):
        document['display_orbit'].text = orbit_list[n].name
        document['tle_orbit'].value = orbit_list[n].text
    return addn2

for i in range(len(orbit_list)):
    globals()['add{}'.format(i)] = addfunc_orbit(i)



""" Events """


def on_resize(e):
    camera_item.window_resize()




def run_simulation():
    document['top_bar'].style.display = "block"
    document['start_dialog'].style.display = "none"

    global animation, window
    window.onresize = on_resize
    animation = Animation()
    animation.run()
