#!/usr/bin/python

import sys
import os
import requests
import json


def usage():
    basename = os.path.basename(__file__)
    print(f"usage : {basename} latitude longitude")
    print()
    print("example:")
    print("    $ python {basename} 35.6814672 139.7653745")
    print('    {"latitude": 35.6814672, "longitude": 139.7653745, "altitude": 39.6706, "geoid_height": 36.6706, "elevation": 3.0}')
    print()

    sys.exit()


if len(sys.argv) != 3:
    usage()


lat = float(sys.argv[1])
long = float(sys.argv[2])

# https://vldb.gsi.go.jp/sokuchi/surveycalc/api_help.html
res = requests.get(
    f"http://vldb.gsi.go.jp/sokuchi/surveycalc/geoid/calcgh/cgi/geoidcalc.pl?outputType=json&latitude={lat}&longitude={long}")

# {"OutputData":{"latitude":"35.681467200","longitude":"139.765374500","geoidHeight":"36.6706"}}
d = json.loads(res.text)
geoid_height = float(d["OutputData"]["geoidHeight"])


# https://maps.gsi.go.jp/development/elevation_s.html
res = requests.get(
    f"https://cyberjapandata2.gsi.go.jp/general/dem/scripts/getelevation.php?outtype=JSON&lat={lat}&lon={long}")

# {'elevation': 3, 'hsrc': '5m（レーザ）'}
d = json.loads(res.text)
elevation = float(d["elevation"])

# output results
d = {}
d["latitude"] = lat
d["longitude"] = long
d["altitude"] = geoid_height + elevation
d["geoid_height"] = geoid_height
d["elevation"] = elevation
print(json.dumps(d))
