# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, urllib.error

"""
ΟΝΟΜΑΤΕΠΩΝΥΜΟ: ΧΧΧΧ ΧΧΧΧΧ
ΑΜ: ΧΧΧΧΧΧ
"""

# <--- ΕΔΩ ΘΑ ΜΠΟΥΝ ΟΙ ΒΙΒΛΙΟΘΗΚΕΣ ΠΟΥ ΘΑ ΧΡΗΣΙΜΟΠΟΙΉΣΕΤΕ

def get_tmy(lati, long):
    time_UTC, T2m, RH, GHI, DNI, DHI, IR_h, WS10m, WD10m, SP = ([] for i in range(10))
    
    fhand = urllib.request.urlopen(f'https://re.jrc.ec.europa.eu/api/tmy?lat={lati}&lon={long}')

    for line in fhand:
        line = line.decode()
        if line.startswith("Elevation"):
            e = line.split(":")
            elevation = float(e[1])
        if line.startswith("20"):
            words = line.split(',')
            time_UTC.append(words[0])
            T2m.append(float(words[1]))
            RH.append(float(words[2]))
            GHI.append(float(words[3]))
            DNI.append(float(words[4]))
            DHI.append(float(words[5]))
            IR_h.append(float(words[6]))
            WS10m.append(float(words[7]))
            WD10m.append(float(words[8]))
            SP.append(float(words[9]))
    dic = {"time_UTC": time_UTC, "T2m": T2m, "RH": RH, "GHI": GHI, "DNI": DNI, "DHI": DHI, "IR_h": IR_h, "WS10m": WS10m, "WD10m" : WD10m, "SP": SP}    

    print(dic)

# def plot_mean_wd_per_hour(wd_list):
#     pass # <--- ΕΔΩ ΘΑ ΜΠΕΙ ΚΩΔΙΚΑΣ

# ΣΧΟΛΙΑΣΕΤΕ ΤΟΝ ΚΩΔΙΚΑ ΣΑΣ

get_tmy(41.141816091983856, 24.891168951039393)