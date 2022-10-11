#!/usr/bin/python
#coding: ascii

import can
import csv
import sys
import json
import os

def main(argv):
    locationId = '45E'
    #log_output = []
    output_dic = {}

    filename = sys.argv[1]
    print(filename)
    configFile = sys.argv[2]
    print(configFile)

    outFile = filename.replace('.blf', '.can')
    if os.path.exists(outFile):#remove file if it exists
        os.remove(outFile)
    print(outFile)
    
    with open(configFile, 'r' ) as config:
        json_content = json.load(config)
        config_contents = str(json_content)
        config_contents = config_contents.replace("u'", "'")
        for data_item in json_content['config']:
            arbId = data_item['arb']
            if len(arbId) < 3:
                arbId = "0" + arbId
            output_dic[arbId] = "" #init dic
            print(arbId)
        locationInfo = json_content['locationInfo']
        arbId = locationInfo['arb']
        print(arbId)
        output_dic[arbId] = ""

    #load blf file
    print("Loading BLF file...")
    log = can.BLFReader(filename)
    log = list(log)

    for msg in log:
        msg = str(msg)
        #print(msg)
        msgId = msg[41:44].upper()
        msgPayload = msg[76:99].replace(" ", "").strip()
        msgTimestamp = msg[11:27]
        channel = msg[-1]
        print(channel + "-" + msgId + ":" + msgPayload)
        
        if msgId in output_dic:
            if(msgId == "077" and channel == "2"):
                continue
            print("found key" + msgId)
            output_dic[msgId] = [channel, msgTimestamp, msgId, msgPayload]
            if msgId == locationId and msgPayload[0] == '1':
                with open(outFile, "a+", newline='') as f:
                    writer = csv.writer(f, delimiter=',', quotechar='', quoting=csv.QUOTE_NONE)
                    writer.writerows(output_dic.values())
                    print(output_dic.keys())
                    print(output_dic.values())

if __name__ == "__main__":
   main(sys.argv)