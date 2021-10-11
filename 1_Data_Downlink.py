import asyncio
import websockets
import json
import traceback
import csv
import math

def view_actor_data(actor, port_type, port_name):
    pass
fieldnames = ["Num","Speed X", "Speed Y", "Speed Z","Total Speed", "Lo", "La", "Heading(Deg)"]

fieldnamesP = ["Num","Speed X", "Speed Y", "Speed Z","Total Speed", "Lo", "La", "Heading(Deg)"]

fieldnamesoriOS = ["Num", "Own_Ori"]
fieldnamesoriTS1 = ["Num", "TS1_Ori"]
fieldnamesoriTS2 = ["Num", "TS2_Ori"]
fieldnamesoriTS3 = ["Num", "TS3_Ori"]
fieldnamesoriTS4 = ["Num", "TS4_Ori"]
fieldnamesoriTS5 = ["Num", "TS5_Ori"]

with open('Data_Collected/OS_Data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

with open('Data_Collected/TS1_Data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

with open('Data_Collected/TS2_Data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()


with open('Data_Collected/TS3_Data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

with open('Data_Collected/TS4_Data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

with open('Data_Collected/TS5_Data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()


with open('Data_Collected/ori/OriOS.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriOS)
    csv_writer.writeheader()

with open('Data_Collected/ori/OriTS1.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS1)
    csv_writer.writeheader()

with open('Data_Collected/ori/OriTS2.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS2)
    csv_writer.writeheader()

with open('Data_Collected/ori/OriTS3.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS3)
    csv_writer.writeheader()

with open('Data_Collected/ori/OriTS4.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS4)
    csv_writer.writeheader()

with open('Data_Collected/ori/OriTS5.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS5)
    csv_writer.writeheader()



def OS_find_gps_port_value(actor, port_type, port_name_ls,n):
    #print(n)
    port_list = actor[port_type]
    #print('port list :',actor)
    num_port = len(port_list)
    #print('num_port: ',num_port)
    num_port_name = len(port_name_ls)
    #print('num_port_name: ', num_port_name)
    speed = []
    gps_info = []
    OS_result = [[], []]
    orip = []
    num = 0
    for i in range(num_port_name):  # 5,2
        for j in range(num_port):  # 34, 34
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "WORLD_VELOCITY".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        speed.append(v['value'])
                    OS_result[1] = speed
                else:
                    gps_info.append(port_list[j]['value']['value'])
                    OS_result[0] = gps_info
                    break

    #print(num)
    #print('iioopanjxnj',orip)
    print('Own Ship Info')
    print('Speed X:',speed[0])
    print('Speed Y:', speed[1])
    print('Speed Z:', speed[2])
    total_speed = math.sqrt((speed[0])**2 + (speed[1])**2)
    print('Total Speed :',total_speed)
    print('Long: ',gps_info[2])
    print('Latt: ', gps_info[3])
    print('Heading(Deg) : ', math.degrees(gps_info[4]))
    print('---------------------')
    key1 = 0
    if key1 == 0:

        with open('Data_Collected/OS_Data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "Num": n-1,
                "Speed X": speed[0],
                "Speed Y": speed[1],
                "Speed Z": speed[2],
                "Total Speed" : total_speed,
                "Lo": gps_info[2],
                "La": gps_info[3],
                "Heading(Deg)":  math.degrees(gps_info[4]),
            }
            csv_writer.writerow(info)

    #print(result)
    return OS_result

#--------------------------------------------------TS1---------------------------------------------------------
def TS1_find_gps_port_value(actor, port_type, port_name_ls,n):
    #print(n)
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    speed = []
    gps_info = []
    TS1_result = [[], []]
    num = 0
    for i in range(num_port_name):  # 5,2
        for j in range(num_port):  # 34, 34
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "WORLD_VELOCITY".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        speed.append(v['value'])
                    TS1_result[1] = speed
                else:
                    gps_info.append(port_list[j]['value']['value'])
                    TS1_result[0] = gps_info
                    break
    #print(num)
    print('TS1 Ship Info')
    print('Speed X:',speed[0])
    print('Speed Y:', speed[1])
    print('Speed Z:', speed[2])
    total_speed = math.sqrt((speed[0])**2 + (speed[1])**2)
    print('Total Speed :',total_speed)
    print('Long: ',gps_info[2])
    print('Latt: ', gps_info[3])
    hdz1 = math.degrees(gps_info[4])
    if hdz1 < 0:
        ha1 = hdz1 +0
    else:
        ha1 = hdz1
    print('Heading(Deg) : ', -ha1)
    print('---------------------')
    key1 = 0
    if key1 == 0:

        with open('Data_Collected/TS1_Data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "Num": n,
                "Speed X": speed[0],
                "Speed Y": speed[1],
                "Speed Z": speed[2],
                "Total Speed" : total_speed,
                "Lo": gps_info[2],
                "La": gps_info[3],
                "Heading(Deg)": (ha1-180),
            }
            csv_writer.writerow(info)

    #print(result)
    return TS1_result


#--------------------------------------------------TS2---------------------------------------------------------



def TS2_find_gps_port_value(actor, port_type, port_name_ls,n):
    #print(n)
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    speed = []
    gps_info = []
    TS2_result = [[], []]
    num = 0
    for i in range(num_port_name):  # 5,2
        for j in range(num_port):  # 34, 34
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "WORLD_VELOCITY".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        speed.append(v['value'])
                    TS2_result[1] = speed
                else:
                    gps_info.append(port_list[j]['value']['value'])
                    TS2_result[0] = gps_info
                    break
    #print(num)
    print('TS2 Ship Info')
    print('Speed X:',speed[0])
    print('Speed Y:', speed[1])
    print('Speed Z:', speed[2])
    total_speed = math.sqrt((speed[0])**2 + (speed[1])**2)
    print('Total Speed :',total_speed)
    print('Long: ',gps_info[2])
    print('Latt: ', gps_info[3])
    hdz2 = math.degrees(gps_info[4])
    if hdz2 < 0:
        ha2 = hdz2 +0
    else:
        ha2 = hdz2

    print('Heading(Deg) : ', ha2)
    print('---------------------')
    key1 = 0
    if key1 == 0:

        with open('Data_Collected/TS2_Data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "Num": n,
                "Speed X": speed[0],
                "Speed Y": speed[1],
                "Speed Z": speed[2],
                "Total Speed" : total_speed,
                "Lo": gps_info[2],
                "La": gps_info[3],
                "Heading(Deg)": -360-(ha2+180)-180-90,
            }
            csv_writer.writerow(info)

    #print(result)
    return TS2_result

#--------------------------------------------------TS3---------------------------------------------------------


def TS3_find_gps_port_value(actor, port_type, port_name_ls,n):
    #print(n)
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    speed = []
    gps_info = []
    TS3_result = [[], []]
    num = 0
    for i in range(num_port_name):  # 5,2
        for j in range(num_port):  # 34, 34
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "WORLD_VELOCITY".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        speed.append(v['value'])
                    TS3_result[1] = speed
                else:
                    gps_info.append(port_list[j]['value']['value'])
                    TS3_result[0] = gps_info
                    break
    #print(num)
    print('TS3 Ship Info')
    print('Speed X:',speed[0])
    print('Speed Y:', speed[1])
    print('Speed Z:', speed[2])
    total_speed = math.sqrt((speed[0])**2 + (speed[1])**2)
    print('Total Speed :',total_speed)
    print('Long: ',gps_info[2])
    print('Latt: ', gps_info[3])

    hdz3 = math.degrees(gps_info[4])
    if hdz3 < 0:
        ha3 = hdz3 + 0
    else:
        ha3 = hdz3

    print('Heading(Deg) : ', math.degrees(gps_info[4]))
    print('---------------------')
    key1 = 0
    if key1 == 0:

        with open('Data_Collected/TS3_Data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "Num": n,
                "Speed X": speed[0],
                "Speed Y": speed[1],
                "Speed Z": speed[2],
                "Total Speed" : total_speed,
                "Lo": gps_info[2],
                "La": gps_info[3],
                "Heading(Deg)": ha3-90,
            }
            csv_writer.writerow(info)

    #print(result)
    return TS3_result


#--------------------------------------------------TS4---------------------------------------------------------


def TS4_find_gps_port_value(actor, port_type, port_name_ls,n):
    #print(n)
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    speed = []
    gps_info = []
    TS4_result = [[], []]
    num = 0
    for i in range(num_port_name):  # 5,2
        for j in range(num_port):  # 34, 34
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "WORLD_VELOCITY".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        speed.append(v['value'])
                    TS4_result[1] = speed
                else:
                    gps_info.append(port_list[j]['value']['value'])
                    TS4_result[0] = gps_info
                    break
    #print(num)
    print('TS4 Ship Info')
    print('Speed X:',speed[0])
    print('Speed Y:', speed[1])
    print('Speed Z:', speed[2])
    total_speed = math.sqrt((speed[0])**2 + (speed[1])**2)
    print('Total Speed :',total_speed)
    print('Long: ',gps_info[2])
    print('Latt: ', gps_info[3])

    hdz4 = math.degrees(gps_info[4])
    if hdz4 < 0:
        ha4 = hdz4 +0
    else:
        ha4 = hdz4

    print('Heading(Deg) : ', ha4)
    print('---------------------')
    key1 = 0
    if key1 == 0:

        with open('Data_Collected/TS4_Data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "Num": n,
                "Speed X": speed[0],
                "Speed Y": speed[1],
                "Speed Z": speed[2],
                "Total Speed" : total_speed,
                "Lo": gps_info[2],
                "La": gps_info[3],
                "Heading(Deg)": -360-(ha4+180)-180,
            }
            csv_writer.writerow(info)

    #print(result)
    return TS4_result


#--------------------------------------------------TS5---------------------------------------------------------


def TS5_find_gps_port_value(actor, port_type, port_name_ls,n):

    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    speed = []
    gps_info = []
    TS5_result = [[], []]
    num = 0
    for i in range(num_port_name):  # 5,2
        for j in range(num_port):  # 34, 34
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "WORLD_VELOCITY".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        speed.append(v['value'])
                    TS5_result[1] = speed
                else:
                    gps_info.append(port_list[j]['value']['value'])
                    TS5_result[0] = gps_info
                    break
    #print(num)
    print('TS5 Ship Info')
    print('Speed X:',speed[0])
    print('Speed Y:', speed[1])
    print('Speed Z:', speed[2])
    total_speed = math.sqrt((speed[0])**2 + (speed[1])**2)
    print('Total Speed :',total_speed)
    print('Long: ',gps_info[2])
    print('Latt: ', gps_info[3])

    hdz5 = math.degrees(gps_info[4])
    if hdz5 < 0:
        ha5 = hdz5 +0
    else:
        ha5 = hdz5

    print('Heading(Deg) : ', ha5)
    print('---------------------')
    key1 = 0
    if key1 == 0:

        with open('Data_Collected/TS5_Data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            info = {
                "Num": n-1,
                "Speed X": speed[0],
                "Speed Y": speed[1],
                "Speed Z": speed[2],
                "Total Speed" : total_speed,
                "Lo": gps_info[2],
                "La": gps_info[3],
                "Heading(Deg)": -ha5,
            }
            csv_writer.writerow(info)

    #print(result)
    return TS5_result
#----------------------------------Oriernation---------------


def find_ori_port_valueOS(actor, port_type, port_name_ls,n):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    orientation = []
    for i in range(num_port_name):
        for j in range(num_port):
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "ORIENTATION".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        orientation.append(v['value'])
                else:
                    break
    #print('OrintationOS: ', math.degrees(orientation[-1]))
    with open('Data_Collected/ori/OriOS.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriOS)

        info = {
            "Num": n,
            "Own_Ori": round(math.degrees(orientation[2]),2),
        }
        csv_writer.writerow(info)

def find_ori_port_valueTS1(actor, port_type, port_name_ls, n):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    orientation = []
    for i in range(num_port_name):
        for j in range(num_port):
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "ORIENTATION".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        orientation.append(v['value'])
                else:
                    break
    # print('OrintationOS: ', math.degrees(orientation[-1]))
    with open('Data_Collected/ori/OriTS1.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS1)

        info = {
            "Num": n-1,
            "TS1_Ori": round(math.degrees(orientation[2]),2),
        }
        csv_writer.writerow(info)

def find_ori_port_valueTS2(actor, port_type, port_name_ls, n):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    orientation = []
    for i in range(num_port_name):
        for j in range(num_port):
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "ORIENTATION".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        orientation.append(v['value'])
                else:
                    break
    # print('OrintationOS: ', math.degrees(orientation[-1]))
    with open('Data_Collected/ori/OriTS2.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS2)

        info = {
            "Num": n,
            "TS2_Ori": round(math.degrees(orientation[2]), 2),
        }
        csv_writer.writerow(info)

def find_ori_port_valueTS3(actor, port_type, port_name_ls, n):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    orientation = []
    for i in range(num_port_name):
        for j in range(num_port):
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "ORIENTATION".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        orientation.append(v['value'])
                else:
                    break
    # print('OrintationOS: ', math.degrees(orientation[-1]))
    with open('Data_Collected/ori/OriTS3.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS3)

        info = {
            "Num": n,
            "TS3_Ori": round(math.degrees(orientation[2]), 2),
        }
        csv_writer.writerow(info)

def find_ori_port_valueTS4(actor, port_type, port_name_ls, n):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    orientation = []
    for i in range(num_port_name):
        for j in range(num_port):
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "ORIENTATION".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        orientation.append(v['value'])
                else:
                    break
    # print('OrintationOS: ', math.degrees(orientation[-1]))
    with open('Data_Collected/ori/OriTS4.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS4)

        info = {
            "Num": n,
            "TS4_Ori": round(math.degrees(orientation[2]), 2),
        }
        csv_writer.writerow(info)

def find_ori_port_valueTS5(actor, port_type, port_name_ls, n):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    orientation = []
    for i in range(num_port_name):
        for j in range(num_port):
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "ORIENTATION".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        orientation.append(v['value'])
                else:
                    break
    # print('OrintationOS: ', math.degrees(orientation[-1]))
    with open('Data_Collected/ori/OriTS5.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnamesoriTS5)

        info = {
            "Num": n,
            "TS5_Ori": round(math.degrees(orientation[2]), 2),
        }
        csv_writer.writerow(info)

    return math.degrees(orientation[2])

def Ori_find_gps_port_value(actor, port_type, port_name_ls):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    speed = []
    gps_info = []
    orient = []
    Ori_result = [[], []]
    for i in range(num_port_name):
        for j in range(num_port):
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "WORLD_VELOCITY".upper():
                    value_ls = port_list[j]['value']['valueObjects']
                    for v in value_ls:
                        speed.append(v['value'])
                    Ori_result[1] = speed
                elif port_name == "ORIENTATION".upper():
                    break
                else:
                    gps_info.append(port_list[j]['value']['value'])
                    Ori_result[0] = gps_info
                    break

    print('Own Ship Info')
    print('Speed X:',speed[0])
    print('Speed Y:', speed[1])
    print('Speed Z:', speed[2])
    total_speed = math.sqrt((speed[0])**2 + (speed[1])**2)
    print('Total Speed :',total_speed)
    print('Long: ',gps_info[2])
    print('Latt: ', gps_info[3])
    print('Heading(Deg) : ', math.degrees(gps_info[4]))
    print('---------------------')
    return Ori_result


def find_actuator_port_value(actor, port_type, port_name_ls):
    port_list = actor[port_type]
    num_port = len(port_list)
    num_port_name = len(port_name_ls)
    result = []
    for i in range(num_port_name):  # 5, 2
        for j in range(num_port):  # 34, 34
            port_name = port_list[j]['port']['name']
            if port_name == port_name_ls[i]:
                if port_name == "COMMANDED_ANGLE".upper():
                    angle = port_list[j]['value']['value']
                    result.append(angle)
                elif port_name == "COMMANDED_RPM".upper():
                    velocity = port_list[j]['value']['value']
                    result.append(velocity)
    return result


def set_actuator_json(actor, port_type, deg):
    port_list = actor[port_type]
    num_port = len(port_list)
    for i in range(num_port):
        port_name = port_list[i]['port']['name']
        if port_name == "COMMANDED_ANGLE".upper():
            port_list[i]['value']['value'] = deg * 3.14 / 180
            # print(port_list[i]['value']['value'])
        elif port_name == "COMMANDED_RPM".upper():
            port_list[i]['value']['value'] = 10                                             # Why Constant Value ?
            # print(port_list[i]['value']['value'])
    return actor


def ls_to_dic(receivedata, port_gps_info):
    num_port = len(receivedata)
    num_port_name = len(port_gps_info)
    result = dict()
    for i in range(0, num_port, num_port_name):
        for key, val in zip(port_gps_info, receivedata[i:i + num_port_name]):
            if key not in result:
                result[key] = []
            result[key].append(val)
    return result


async def start():
    num = 0
    uri = "ws://192.168.114.18:8887"
    actor_info = {
        'clazz': '',
        'name': '',
        'uuid': None,
        'parent_uuid': None
    }

    port_gps_info = {
        'clazzname': '',
        'LONGITUDE': None,
        'LATITUDE': None,
        'EASTING': None,
        'NORTHING': None,
        'BEARING': None,
        'WORLD_VELOCITY': [],
    }

    port_gps_info_ori = {
        'clazzname': '',
        'LONGITUDE': None,
        'LATITUDE': None,
        'EASTING': None,
        'NORTHING': None,
        # 'BEARING': None,
        'WORLD_VELOCITY': [],
        'ORIENTATION':[]
    }


    port_actuator_info = {
        'clazzname': '',
        # 'ANGLE': [], # starboard rudder, port rudder
        # 'ACTUAL_RPM': [] # starboard rpm, port rpm
        'COMMANDED_ANGLE': [],  # starboard rudder, port rudder
        'COMMANDED_RPM': []  # starboard rpm, port rpm
    }

    Ori_port_gps_name_ls, Ori_port_actuator_name_ls = [], []
    for name in port_gps_info_ori:
        Ori_port_gps_name_ls.append(name)
    Ori_port_gps_name_ls.pop(0)  # port's name
    for name in port_actuator_info:
        Ori_port_actuator_name_ls.append(name)
    Ori_port_actuator_name_ls.pop(0)

    port_gps_name_ls, port_actuator_name_ls = [], []
    for name in port_gps_info:
        port_gps_name_ls.append(name)
    port_gps_name_ls.pop(0)  # port's name
    for name in port_actuator_info:
        port_actuator_name_ls.append(name)
    port_actuator_name_ls.pop(0)

    #---------------------Orient-----------------------

    gps_gunnerus_ori = actor_info.copy()
    gps_gunnerus_ori['clazz'] = 'TypedSixDOFActor'
    gps_gunnerus_ori['name'] = 'Gunnerus'

    gps_ts1_ori = actor_info.copy()
    gps_ts1_ori['clazz'] = 'TypedSixDOFActor'
    gps_ts1_ori['name'] = 'Target Ship 1'

    gps_ts2_ori = actor_info.copy()
    gps_ts2_ori['clazz'] = 'TypedSixDOFActor'
    gps_ts2_ori['name'] = 'Target Ship 2'

    gps_ts3_ori = actor_info.copy()
    gps_ts3_ori['clazz'] = 'TypedSixDOFActor'
    gps_ts3_ori['name'] = 'Target Ship 3'

    gps_ts4_ori = actor_info.copy()
    gps_ts4_ori['clazz'] = 'TypedSixDOFActor'
    gps_ts4_ori['name'] = 'Target Ship 4'

    gps_ts5_ori = actor_info.copy()
    gps_ts5_ori['clazz'] = 'TypedSixDOFActor'
    gps_ts5_ori['name'] = 'Target Ship 5'


    #----------GPS Ships-----------------------

    gps_gunnerus = actor_info.copy()
    gps_gunnerus['clazz'] = 'GPSController'
    gps_gunnerus['name'] = 'GPS1'

    gps_target_ship_1 = actor_info.copy()
    gps_target_ship_1['clazz'] = 'GPSController'
    gps_target_ship_1['name'] = 'Target Ship 1'

    gps_target_ship_2 = actor_info.copy()
    gps_target_ship_2['clazz'] = 'GPSController'
    gps_target_ship_2['name'] = 'Target Ship 2'

    gps_target_ship_3 = actor_info.copy()
    gps_target_ship_3['clazz'] = 'GPSController'
    gps_target_ship_3['name'] = 'Target Ship 3'

    gps_target_ship_4 = actor_info.copy()
    gps_target_ship_4['clazz'] = 'GPSController'
    gps_target_ship_4['name'] = 'Target Ship 4'

    gps_target_ship_5 = actor_info.copy()
    gps_target_ship_5['clazz'] = 'GPSController'
    gps_target_ship_5['name'] = 'Target Ship 5'

    gunnerus_thruster_port = actor_info.copy()
    gunnerus_thruster_port['clazz'] = 'ThrusterActor'
    gunnerus_thruster_port['name'] = 'Port'

    gunnerus_thruster_starboard = actor_info.copy()
    gunnerus_thruster_starboard['clazz'] = 'ThrusterActor'
    gunnerus_thruster_starboard['name'] = 'Starboard'

    actor_info_list1 = [gps_gunnerus]
    actor_Ori_1 = [gps_gunnerus_ori]
    actor_ts1_1 = [gps_ts1_ori]
    actor_ts2_1 = [gps_ts2_ori]
    actor_ts3_1 = [gps_ts3_ori]
    actor_ts4_1 = [gps_ts4_ori]
    actor_ts5_1 = [gps_ts5_ori]

    actor_info_list2 = [gps_target_ship_1]
    actor_info_list3 = [gps_target_ship_2]
    actor_info_list4 = [gps_target_ship_3]
    actor_info_list5 = [gps_target_ship_4]
    actor_info_list6 = [gps_target_ship_5]

    actuator_get_json1 = []
    port_value1 = []

    actuator_get_json2 = []
    port_value2 = []

    actuator_get_json3 = []
    port_value3 = []

    actuator_get_json4 = []
    port_value4 = []

    actuator_get_json5 = []
    port_value5 = []

    actuator_get_json6 = []
    port_value6 = []

    actuator_get_json7 = []
    port_value7 = []

    actuator_get_json8 = []
    port_value8 = []

    actuator_get_json9 = []
    port_value9 = []

    actuator_get_json10 = []
    port_value10 = []

    actuator_get_json11 = []
    port_value11 = []

    actuator_get_json12 = []
    port_value12 = []

    async with websockets.connect(uri, ping_timeout=None) as websocket:
        while True:
            if not websocket.open:
                print('reconnecting')
                websocket = await websockets.connect(uri)
            else:
                resp = await websocket.recv()
                # print(resp)
                actuator_set_json = None
                actuators_set_json = []
                try:
                    data_dic = json.loads(resp[resp.index('{'):])
                    for i in range(1):
                        actor_info1 = actor_info_list1[i]
                        actor_info2 = actor_info_list2[i]
                        actor_info3 = actor_info_list3[i]
                        actor_info4 = actor_info_list4[i]
                        actor_info5 = actor_info_list5[i]
                        actor_info6 = actor_info_list6[i]

                        actor_ori1 = actor_Ori_1[i]
                        actor_orits1 = actor_ts1_1[i]
                        actor_orits2 = actor_ts2_1[i]
                        actor_orits3 = actor_ts3_1[i]
                        actor_orits4 = actor_ts4_1[i]
                        actor_orits5 = actor_ts5_1[i]

                        actor1 = await evaluate_actor(data_dic, actor_info1['clazz'],
                                                     actor_info1['name'])  # out the dic data type

                        actor2 = await evaluate_actor(data_dic, actor_info2['clazz'],
                                                     actor_info2['name'])  # out the dic data type

                        actor3 = await evaluate_actor(data_dic, actor_info3['clazz'],
                                                     actor_info3['name'])  # out the dic data type

                        actor4 = await evaluate_actor(data_dic, actor_info4['clazz'],
                                                     actor_info4['name'])  # out the dic data type

                        actor5 = await evaluate_actor(data_dic, actor_info5['clazz'],
                                                     actor_info5['name'])  # out the dic data type

                        actor6 = await evaluate_actor(data_dic, actor_info6['clazz'],
                                                     actor_info6['name'])  # out the dic data type
                        actor7 =  await evaluate_actor(data_dic, actor_ori1['clazz'],
                                                     actor_ori1['name'])  # out the dic

                        actor8 =  await evaluate_actor(data_dic, actor_orits1['clazz'],
                                                     actor_orits1['name'])  # out the dic


                        actor9 =  await evaluate_actor(data_dic, actor_orits2['clazz'],
                                                     actor_orits2['name'])  # out the dic


                        actor10 =  await evaluate_actor(data_dic, actor_orits3['clazz'],
                                                     actor_orits3['name'])  # out the dic


                        actor11 =  await evaluate_actor(data_dic, actor_orits4['clazz'],
                                                     actor_orits4['name'])  # out the dic


                        actor12 =  await evaluate_actor(data_dic, actor_orits5['clazz'],
                                                     actor_orits5['name'])  # out the dic


                        if actor1 != None:
                            num += 1
                            if actor1['name'] == 'Starboard' or actor1['name'] == 'Port':
                                actuator_get_json1.append(actor1)
                                actuator_set_json1 = set_actuator_json(actor1, 'input', 90)
                                actuators_set_json.append(actuator_set_json)
                                actuator_port_value = find_actuator_port_value(actor1, 'output', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                                actuator_port_value = find_actuator_port_value(actor1, 'input', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                            else:
                                gps_port_value = OS_find_gps_port_value(actor1, 'output', port_gps_name_ls,num)
                                # ls_to_dic(gps_port_value, port_gps_name_ls)
                                port_value1.append(gps_port_value)

                        if actor2 != None:
                            if actor2['name'] == 'Starboard' or actor2['name'] == 'Port':
                                actuator_get_json2.append(actor2)
                                actuator_set_json = set_actuator_json(actor2, 'input', 90)
                                actuators_set_json.append(actuator_set_json)
                                actuator_port_value = find_actuator_port_value(actor2, 'output', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                                actuator_port_value = find_actuator_port_value(actor2, 'input', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                            else:
                                gps_port_value = TS1_find_gps_port_value(actor2, 'output', port_gps_name_ls,num)
                                # ls_to_dic(gps_port_value, port_gps_name_ls)
                                port_value2.append(gps_port_value)

                        if actor3 != None:
                            if actor3['name'] == 'Starboard' or actor3['name'] == 'Port':
                                actuator_get_json3.append(actor3)
                                actuator_set_json = set_actuator_json(actor3, 'input', 90)
                                actuators_set_json.append(actuator_set_json)
                                actuator_port_value = find_actuator_port_value(actor3, 'output', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                                actuator_port_value = find_actuator_port_value(actor3, 'input', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                            else:
                                gps_port_value = TS2_find_gps_port_value(actor3, 'output', port_gps_name_ls,num)
                                # ls_to_dic(gps_port_value, port_gps_name_ls)
                                port_value3.append(gps_port_value)

                        if actor4 != None:
                            if actor4['name'] == 'Starboard' or actor4['name'] == 'Port':
                                actuator_get_json4.append(actor4)
                                actuator_set_json = set_actuator_json(actor4, 'input', 90)
                                actuators_set_json.append(actuator_set_json)
                                actuator_port_value = find_actuator_port_value(actor4, 'output', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                                actuator_port_value = find_actuator_port_value(actor4, 'input', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                            else:
                                gps_port_value = TS3_find_gps_port_value(actor4, 'output', port_gps_name_ls,num)
                                # ls_to_dic(gps_port_value, port_gps_name_ls)
                                port_value4.append(gps_port_value)

                        if actor5 != None:
                            if actor5['name'] == 'Starboard' or actor5['name'] == 'Port':
                                actuator_get_json5.append(actor5)
                                actuator_set_json = set_actuator_json(actor5, 'input', 90)
                                actuators_set_json.append(actuator_set_json)
                                actuator_port_value = find_actuator_port_value(actor5, 'output', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                                actuator_port_value = find_actuator_port_value(actor5, 'input', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                            else:
                                gps_port_value = TS4_find_gps_port_value(actor5, 'output', port_gps_name_ls,num)
                                # ls_to_dic(gps_port_value, port_gps_name_ls)
                                port_value5.append(gps_port_value)

                        if actor6 != None:
                            if actor6['name'] == 'Starboard' or actor6['name'] == 'Port':
                                actuator_get_json6.append(actor6)
                                actuator_set_json = set_actuator_json(actor6, 'input', 90)
                                actuators_set_json.append(actuator_set_json)
                                actuator_port_value = find_actuator_port_value(actor6, 'output', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                                actuator_port_value = find_actuator_port_value(actor6, 'input', port_actuator_name_ls,num)
                                # port_value.append(actuator_port_value)
                            else:
                                gps_port_value = TS5_find_gps_port_value(actor6, 'output', port_gps_name_ls,num)
                                # ls_to_dic(gps_port_value, port_gps_name_ls)
                                port_value6.append(gps_port_value)

                        if actor7 != None:
                            if actor7 != None:
                                if actor7['name'] == 'Starboard' or actor7['name'] == 'Port':
                                    actuator_get_json7.append(actor7)
                                    # actuator_set_json = set_actuator_json(actor, 'input', 90)
                                    # actuators_set_json.append(actuator_set_json)
                                    # actuator_port_value = find_actuator_port_value(actor, 'output', port_actuator_name_ls)
                                    # port_value.append(actuator_port_value)
                                    # actuator_port_value = find_actuator_port_value(actor, 'input', port_actuator_name_ls)
                                    # print(actor)
                                    # port_value.append(actuator_port_value)
                                    # print(port_value)
                                # elif actor['clazz'].__contains__('TypedSixDOFActor'):
                                elif actor7['clazz'].__contains__('TypedSixDOFActor'):
                                    gps_gunnerus_orientation = find_ori_port_valueOS(actor7, 'output', Ori_port_gps_name_ls,num)
                                    #print(gps_gunnerus_orientation)
                                else:
                                    gps_port_value_rest = Ori_find_gps_port_value(actor7, 'output', Ori_port_gps_name_ls,num)
                                    # ls_to_dic(gps_port_value, port_gps_name_ls)
                                    port_value7.append(gps_port_value_rest)

                        if actor8 != None:
                            if actor8 != None:
                                if actor8['name'] == 'Starboard' or actor8['name'] == 'Port':
                                    actuator_get_json8.append(actor8)
                                    # actuator_set_json = set_actuator_json(actor, 'input', 90)
                                    # actuators_set_json.append(actuator_set_json)
                                    # actuator_port_value = find_actuator_port_value(actor, 'output', port_actuator_name_ls)
                                    # port_value.append(actuator_port_value)
                                    # actuator_port_value = find_actuator_port_value(actor, 'input', port_actuator_name_ls)
                                    # print(actor)
                                    # port_value.append(actuator_port_value)
                                    # print(port_value)
                                # elif actor['clazz'].__contains__('TypedSixDOFActor'):
                                elif actor8['clazz'].__contains__('TypedSixDOFActor'):
                                    gps_ts1_orientation = find_ori_port_valueTS1(actor8, 'output', Ori_port_gps_name_ls,num)
                                    print(gps_ts1_orientation)
                                else:
                                    gps_port_value_rest = Ori_find_gps_port_value(actor8, 'output', Ori_port_gps_name_ls,num)
                                    # ls_to_dic(gps_port_value, port_gps_name_ls)
                                    port_value8.append(gps_port_value_rest)

                        if actor9 != None:
                            if actor9 != None:
                                if actor9['name'] == 'Starboard' or actor9['name'] == 'Port':
                                    actuator_get_json9.append(actor9)
                                    # actuator_set_json = set_actuator_json(actor, 'input', 90)
                                    # actuators_set_json.append(actuator_set_json)
                                    # actuator_port_value = find_actuator_port_value(actor, 'output', port_actuator_name_ls)
                                    # port_value.append(actuator_port_value)
                                    # actuator_port_value = find_actuator_port_value(actor, 'input', port_actuator_name_ls)
                                    # print(actor)
                                    # port_value.append(actuator_port_value)
                                    # print(port_value)
                                # elif actor['clazz'].__contains__('TypedSixDOFActor'):
                                elif actor9['clazz'].__contains__('TypedSixDOFActor'):
                                    gps_ts2_orientation = find_ori_port_valueTS2(actor9, 'output', Ori_port_gps_name_ls,num)
                                    print(gps_ts2_orientation)
                                else:
                                    gps_port_value_rest = Ori_find_gps_port_value(actor9, 'output', Ori_port_gps_name_ls,num)
                                    # ls_to_dic(gps_port_value, port_gps_name_ls)
                                    port_value9.append(gps_port_value_rest)

                        if actor10 != None:
                            if actor10 != None:
                                if actor10['name'] == 'Starboard' or actor10['name'] == 'Port':
                                    actuator_get_json10.append(actor10)
                                    # actuator_set_json = set_actuator_json(actor, 'input', 90)
                                    # actuators_set_json.append(actuator_set_json)
                                    # actuator_port_value = find_actuator_port_value(actor, 'output', port_actuator_name_ls)
                                    # port_value.append(actuator_port_value)
                                    # actuator_port_value = find_actuator_port_value(actor, 'input', port_actuator_name_ls)
                                    # print(actor)
                                    # port_value.append(actuator_port_value)
                                    # print(port_value)
                                # elif actor['clazz'].__contains__('TypedSixDOFActor'):
                                elif actor10['clazz'].__contains__('TypedSixDOFActor'):
                                    gps_ts3_orientation = find_ori_port_valueTS3(actor10, 'output', Ori_port_gps_name_ls,num)
                                    print(gps_ts3_orientation)
                                else:
                                    gps_port_value_rest = Ori_find_gps_port_value(actor10, 'output', Ori_port_gps_name_ls,num)
                                    # ls_to_dic(gps_port_value, port_gps_name_ls)
                                    port_value10.append(gps_port_value_rest)

                        if actor11 != None:
                            if actor11 != None:
                                if actor11['name'] == 'Starboard' or actor11['name'] == 'Port':
                                    actuator_get_json11.append(actor11)
                                    # actuator_set_json = set_actuator_json(actor, 'input', 90)
                                    # actuators_set_json.append(actuator_set_json)
                                    # actuator_port_value = find_actuator_port_value(actor, 'output', port_actuator_name_ls)
                                    # port_value.append(actuator_port_value)
                                    # actuator_port_value = find_actuator_port_value(actor, 'input', port_actuator_name_ls)
                                    # print(actor)
                                    # port_value.append(actuator_port_value)
                                    # print(port_value)
                                # elif actor['clazz'].__contains__('TypedSixDOFActor'):
                                elif actor11['clazz'].__contains__('TypedSixDOFActor'):
                                    gps_ts4_orientation = find_ori_port_valueTS4(actor11, 'output',
                                                                                 Ori_port_gps_name_ls, num)
                                    print(gps_ts4_orientation)
                                else:
                                    gps_port_value_rest = Ori_find_gps_port_value(actor11, 'output',
                                                                                  Ori_port_gps_name_ls, num)
                                    # ls_to_dic(gps_port_value, port_gps_name_ls)
                                    port_value11.append(gps_port_value_rest)

                        if actor12 != None:
                            if actor12['name'] == 'Starboard' or actor12['name'] == 'Port':
                                actuator_get_json12.append(actor12)
                                # actuator_set_json = set_actuator_json(actor, 'input', 90)
                                # actuators_set_json.append(actuator_set_json)
                                # actuator_port_value = find_actuator_port_value(actor, 'output', port_actuator_name_ls)
                                # port_value.append(actuator_port_value)
                                # actuator_port_value = find_actuator_port_value(actor, 'input', port_actuator_name_ls)
                                # print(actor)
                                # port_value.append(actuator_port_value)
                                # print(port_value)
                            # elif actor['clazz'].__contains__('TypedSixDOFActor'):
                            elif actor12['clazz'].__contains__('TypedSixDOFActor'):
                                gps_ts5_orientation = find_ori_port_valueTS5(actor12, 'output',
                                                                             Ori_port_gps_name_ls, num)
                                print(gps_ts5_orientation)
                            else:
                                gps_port_value_rest = Ori_find_gps_port_value(actor12, 'output',
                                                                              Ori_port_gps_name_ls, num)
                                # ls_to_dic(gps_port_value, port_gps_name_ls)
                                port_value12.append(gps_port_value_rest)

                       # print('Act: ',actor_info)
                except:
                    traceback.print_exc()
                # print(port_value)
                # save the actuation factor
                # save_json_file(actuator_get_json)

                # with open('my_file.json') as json_file:
                #     data = json.load(json_file)
                #     print(data)
                #     await websocket.send(json.dumps(data))

                if actuators_set_json != None:
                    for i in range(len(actuators_set_json)):
                        # print(actuators_set_json[i])
                        await websocket.send(json.dumps(actuators_set_json[i]))
            #print(num)


       # print('Act: ', actor_info[0])


async def evaluate_actor(data_dic, clazz, name):
    x = False if data_dic['clazz'].find(clazz) == -1 else True
    y = (data_dic['name'] == name)
    if x and y:
        return data_dic


def save_ls_file(receivedata):  # list
    with open('my_file.txt', 'w') as f:
        for item in receivedata:
            f.write("%s\n" % item)


def save_json_file(receivedata):  # dic
    with open('my_file.json', 'w') as f:
        for item in receivedata:
            #print(item)                                #Change
            json.dump(item, f)
    # f.close()


# def trans_json(actuator_get_json):
#     return json.loads(actuator_get_json[actuator_get_json.index('['):])

if __name__ == '__main__':
    # rospy.init_node("simulator_drl")
    asyncio.get_event_loop().run_until_complete(start())
    asyncio.get_event_loop().run_forever()
