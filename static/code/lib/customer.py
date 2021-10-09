class Customer:

    def __init__( self,EIRP, LPolarization, G_T, DataRate,Lpoint,Lmod_demod,f,d):
        self.EIRP = float(EIRP)
        self.LPolarization = float(LPolarization)
        self.G_T = float(G_T)
        self.DataRate = float(DataRate)
        self.Lpoint= float(Lpoint)
        self.Lmod_demod = float(Lmod_demod)
        self.f = float(f)
        self.d = float(d)
