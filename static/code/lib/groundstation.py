
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
