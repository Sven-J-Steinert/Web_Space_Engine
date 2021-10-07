import urllib.request


def js_time(time):
    return time.timetuple().args


def assign_xyz_vector(vec1, vec2):
    vec1.x, vec1.y, vec1.z = vec2.x, vec2.y, vec2.z


def calculate_distance(vec1, vec2):
    x = vec1.x - vec2.x
    y = vec1.y - vec2.y
    z = vec1.z - vec2.z
    return (x**2 + y**2 + z**2)**(1/2)


class Vector3d:

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return "Vector3d({}, {}, {})".format(self.x, self.y, self.z)


def get_tle(identifier):
    with urllib.request.urlopen(
            "https://celestrak.com/NORAD/elements/science.txt") as response:
        text = response.readlines()
    lines = [line.decode().strip() for line in text]
    for i, line in enumerate(lines):
        if line.startswith(identifier):
            line1 = lines[i+1]
            line2 = lines[i+2]
            return dict(first_line=line1, second_line=line2)
    else:
        return None


def patch_datetime(dt):
    """Return a tuple of year, month, etc. as argument for orb.xyz()"""
    return dt.timetuple().args
