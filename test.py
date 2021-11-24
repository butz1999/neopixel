import requests
import time
import json

jdata = """ [
    [ [0,0,0], [1,1,1], [2,2,2], [3,3,3], [4,4,4], [5,5,5], [6,6,6], [7,7,7] ],
    [ [8,8,8], [9,9,9], [10,10,10], [11,11,11], [12,12,12], [13,13,13], [14,14,14], [15,15,15] ],
    [ [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0] ],
    [ [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0] ],
    [ [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0] ],
    [ [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0] ],
    [ [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0] ],
    [ [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0] ]
] """

data = json.loads(jdata)

print(data)

print(tuple(data[0][0]))

bmp = []
for i in range(8):
    line = []
    for j in range(8):
        line.append(tuple(data[i][j]))
        #print(data[i][j])
    bmp.append(line)

print(bmp)

response = requests.post("http://localhost:8080/test/random/32", data=jdata)

#while True:
#    response = requests.post("http://localhost:8080/test/random/32")
#    time.sleep(1)
