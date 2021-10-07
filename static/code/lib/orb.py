from browser import window, load

load("static/js/orb.v2.js")

Orb = window.Orb
Const = Orb.Const

Sun = Orb.Sun.new
Luna = Orb.Luna.new
VSOP = Orb.VSOP.new
Kepler = Orb.Kepler.new
SGP4 = Orb.SGP4.new

Observation = Orb.Observation.new

RadecToXYZ = Orb.RadecToXYZ.new
EquatorialToEcliptic = Orb.EquatorialToEcliptic.new
EclipticToEquatorial = Orb.EclipticToEquatorial.new
XYZtoRadec = Orb.XYZtoRadec.new

Time = Orb.Time.new
