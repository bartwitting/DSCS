import os
import json

# This piece of code uses the Wi-Fi adapter to track the amount of active phones around
#os.system("howmanypeoplearearound --out mac_adresses.json --adapter en0 --sort")

with open('mac_adresses.json') as f:
  data = json.load(f)

all_cellphones = [x for x in data['cellphones']]
threshold = -67 #Around 10 meters
cellphones_within_threshold = [x for x in all_cellphones if x['rssi'] > threshold]

print (len(cellphones_within_threshold))

#####################
#Calculates the distance
#####################
# Power = waarde op 1 meter afstand

# Constant depends on the Environmental factor. Range 2-4

#Power = -47.27906976744186
#RSSI = -67
#N = 2

#Distance = 10**((int(Power)-int(RSSI))/(10 * int(N)))
#print(Distance)