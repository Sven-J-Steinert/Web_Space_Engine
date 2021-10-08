
class Groundstation:

    def __init__( self, id, name, bands, Lat, Lon, altitude):
        self.id = id
        self.name = name
        # size of booleanarray = 7
        # 1     2   3    4    5   6    7  8   9
        # UHF, L ,  S , SGLS, C , X , Ku, K, Ka
        self.bands = bands
        self.Lat = Lat  # °
        self.Lon = Lon  # °
        self.altitude = altitude # m

gs_list = []

gs_list.append(Groundstation(
    id='ESR',
    name='Esrange',
    bands=[True,True,True,False,False,True,False,False,False],
    Lat=67.88,
    Lon=21.07,
    altitude=341
    ))

gs_list.append(Groundstation(
    id='INU',
    name='Inuvik',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=68.4,
    Lon=-133.5,
    altitude=51
    ))

gs_list.append(Groundstation(
    id='NP',
    name='North Pole',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=65.8,
    Lon=-147.65,
    altitude=135
    ))

gs_list.append(Groundstation(
    id='CLE',
    name='Clewiston',
    bands=[False,False,True,True,False,True,False,False,False],
    Lat=26.73,
    Lon=-82.03,
    altitude=3
    ))

gs_list.append(Groundstation(
    id='SPO',
    name='South Point',
    bands=[False,False,True,False,False,True,True,False,False],
    Lat=19.02,
    Lon=-155.67,
    altitude=164
    ))

gs_list.append(Groundstation(
    id='YAT',
    name='Yatharagga(WASC)',
    bands=[False,False,True,False,False,False,False,False,False],
    Lat=-29.08,
    Lon=115.58,
    altitude=280
    ))

gs_list.append(Groundstation(
    id='DON',
    name='Dongara(WASC)',
    bands=[False,False,True,False,False,False,False,False,False],
    Lat=-29.05,
    Lon=115.35,
    altitude=280
    ))

gs_list.append(Groundstation(
    id='STG',
    name='Santiago',
    bands=[False,False,True,False,False,False,False,False,False],
    Lat=-33.13,
    Lon=-70.67,
    altitude=698
    ))

gs_list.append(Groundstation(
    id='PAR',
    name='Punta Arenas',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=-52.93,
    Lon=-70.85,
    altitude=88
    ))

gs_list.append(Groundstation(
    id='FUC',
    name='Fucino',
    bands=[False,True,True,False,True,True,False,False,False],
    Lat=42,
    Lon=13.55,
    altitude=652
    ))

gs_list.append(Groundstation(
    id='HAR',
    name='Hartebeesthoek',
    bands=[False,False,True,False,False,False,False,False,False],
    Lat=-25.64,
    Lon=28.08,
    altitude=1288
    ))

gs_list.append(Groundstation(
    id='SVA',
    name='Svalbard',
    bands=[False,True,True,False,True,True,False,False,False],
    Lat=78.23,
    Lon=15.41,
    altitude=248
    ))

gs_list.append(Groundstation(
    id='TRO',
    name='TrollSat',
    bands=[False,False,True,False,True,True,False,False,False],
    Lat=-72.02,
    Lon=2.53,
    altitude=1270
    ))

gs_list.append(Groundstation(
    id='TMS',
    name='Tromso',
    bands=[False,True,True,False,False,True,False,False,False],
    Lat=69.39,
    Lon=18.56,
    altitude=4
    ))

gs_list.append(Groundstation(
    id='GRI',
    name='Grimstad',
    bands=[False,False,False,False,False,True,False,False,False],
    Lat=58.34,
    Lon=8.59,
    altitude=28
    ))

gs_list.append(Groundstation(
    id='PLL',
    name='Puertollano',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=38.69,
    Lon=-4.11,
    altitude=703
    ))

gs_list.append(Groundstation(
    id='SGP',
    name='Singapore',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=1.35,
    Lon=103.82,
    altitude=55
    ))

gs_list.append(Groundstation(
    id='MAU',
    name='Mauritius',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=-20.35,
    Lon=57.55,
    altitude=579
    ))

gs_list.append(Groundstation(
    id='PAN',
    name='Panama',
    bands=[True,False,True,False,False,False,False,False,False],
    Lat=8.54,
    Lon=-80.78,
    altitude=1057
    ))

gs_list.append(Groundstation(
    id='FBA',
    name='Fairbanks',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=64.80,
    Lon=-147.70,
    altitude=135
    ))

gs_list.append(Groundstation(
    id='DUB',
    name='Dubai',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=25.20,
    Lon=55.27,
    altitude=0
    ))

gs_list.append(Groundstation(
    id='HAR2',
    name='Hartebeesthoek',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=-25.64,
    Lon=28.08,
    altitude=1288
    ))

gs_list.append(Groundstation(
    id='INU2',
    name='Inuvik',
    bands=[False,False,True,False,False,True,False,False,False],
    Lat=68.40,
    Lon=-133.50,
    altitude=51
    ))


for i in range(len(gs_list)):
    print(gs_list[i].bands)
