import json
try:
    # Python 2
    from urllib2 import quote, urlopen
except ModuleNotFoundError:
    # Python 3
    from urllib.parse import quote
    from urllib.request import urlopen


# Use the Elite Dangerous Star Map API to get system coordinates
def get_coords_from_edsm(system_name):
    system_name_url = quote(system_name)
    edsm_url = "https://www.edsm.net/api-v1/system?systemName={SYSTEM}&showCoordinates=1".format(SYSTEM=system_name_url)
    try:
        url = urlopen(edsm_url, timeout=15)
        response = url.read()
        edsm_json = json.loads(response)
        if "name" and "coords" in edsm_json:
            success = True
            x = edsm_json["coords"]["x"]
            y = edsm_json["coords"]["y"]
            z = edsm_json["coords"]["z"]
        else:
            success = False
            x = 0
            y = 0
            z = 0
    except:
        success = False
        x = 0
        y = 0
        z = 0
    return success, x, y, z
