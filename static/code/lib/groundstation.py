
class Groundstation:

    def __init__( self, id, name, bands, Lat, Lon, altitude):
        self.id = id
        self.name = name
        # size of booleanarray = 7
        # 1     2   3    4    5   6    7  8   9
        # UHF, L ,  S , SGLS, C , X , Ka, K, Ku
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


for i in range(len(gs_list)):
    print(gs_list[i].bands)
