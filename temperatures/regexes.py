import re

# Text to search
text = '''Device: Q-tag Fridge-tag 2
Vers: 0.5
Fw Vers: 3.4p0o
Sensor: 1
Conf:
 Serial: 130400141244
 PCB: BG0211306532
 CID: 1000
 Lot: 1792_20_08
 Zone: 0.00
 Measurement delay: 10
 Moving Avrg: 1
 User Alarm Config: 0
 User Clock Config: 1
 Alarm Indication: 0
 Temp unit: C
 Alarm:
  0:
   T AL: -0.5, t AL: 60
  1:
   T AL: +8.3, t AL: 600
 Int Sensor:
  Timeout: 1, Offset: +0.0
 Report history length: 60
 Det Report: 3
 Use ext devices: 0
 Test Res: 1, Test TS: 2021-05-20 12:51
Hist:
 TS Actv: 2022-03-05 11:09
 TS Report Creation: 2022-03-28 07:26
 1:
  Date: 2022-03-28
  Min T: +3.2, TS Min T: 05:24
  Max T: +3.5, TS Max T: 00:00
  Avrg T: +3.3
  Alarm:
   0:
    t Acc: 0
   1:
    t Acc: 0
  Int Sensor timeout:
   t AccST: 0
  Events: 8
  Checked:
   TS AM: 07:20
 2:
  Date: 2022-03-27
  Min T: +2.9, TS Min T: 06:02
  Max T: +3.8, TS Max T: 17:13
  Avrg T: +3.2
  Alarm:
   0:
    t Acc: 0
   1:
    t Acc: 0
  Int Sensor timeout:
   t AccST: 0
  Events: 0
 3:
  Date: 2022-03-26
  Min T: +2.3, TS Min T: 01:57
  Max T: +3.3, TS Max T: 16:49
  Avrg T: +2.8
  Alarm:
   0:
    t Acc: 0
   1:
    t Acc: 0
  Int Sensor timeout:
   t AccST: 0
  Events: 0
 4:
  Date: 2022-03-25
  Min T: +2.1, TS Min T: 01:07
  Max T: +2.8, TS Max T: 16:04
  Avrg T: +2.4
  Alarm:
   0:
    t Acc: 0
   1:
    t Acc: 0
  Int Sensor timeout:
   t AccST: 0
  Events: 0'''

# alarm_pattern = r"Alarm:\s+0:\s+T AL:\s+(?P<Temp_AL_0>[+-]\d+\.\d+)\,\s+" \
#                 r"t AL:\s+(?P<time_AL_0>\d+)\s+1:\s+" \
#                 r"T AL:\s+(?P<Temp_AL_1>[+-]\d+\.\d+)\,\s+" \
#                 r"t AL:\s+(?P<time_AL_1>\d+)"
#
# for m in re.findall(alarm_pattern, text):
#     t_al0 = m[0]
#     t_al_time0 = m[1]
#     t_al1 = m[2]
#     t_al_time1 = m[3]
#     print("t_al0:", t_al0)
#     print("t_al_time0:", t_al_time0)
#     print("t_al1:", t_al1)
#     print("t_al_time1:", t_al_time1)

# sensor_pattern = r'Int Sensor:\s+Timeout:\s+(?P<Timeout>\d+),\s+Offset:\s(?P<Offset>[+-]\d+\.\d+)'
# for m in re.findall(sensor_pattern, text):
#     Timeout = m[0]
#     Offset = m[1]
#     print("Timeout:", Timeout)
#     print("Offset:", Offset)

# pattern_device = "Device:\s+(?P<Device>\w+\-\w+\s+\w+\-\w+\s+\d+)\s+" \
#                  "Vers:\s+(?P<Vers>\d+\.\d+)\s+" \
#                  "Fw Vers:\s+(?P<Fw_vers>\d+\.\d+\w+\d+\w+)\s+" \
#                  "Sensor:\s+(?P<Sensor>\d+)\s+" \
#                  "Conf:\s+" \
#                  "Serial:\s+(?P<Serial>\d+)\s+" \
#                  "PCB:\s+(?P<PCB>\w+\d+)\s+" \
#                  "CID:\s+(?P<CID>\d+)\s+" \
#                  "Lot:\s+(?P<Lot>\d+\_\d+_\d+)\s+" \
#                  "Zone:\s+(?P<Zone>\d+\.\d+)\s+" \
#                  "Measurement delay:\s+(?P<Measurement_delay>\d+)\s+" \
#                  "Moving Avrg:\s+(?P<Moving_Avrg>\d+)\s+" \
#                  "User Alarm Config:\s+(?P<User_Alarm_Config>\d+)\s+" \
#                  "User Clock Config:\s+(?P<Use_clock_Config>\d+)\s+" \
#                  "Alarm Indication:\s(?P<Alarm_Indication>\d+)\s+" \
#                  "Temp unit:\s(?P<Temp_unit>\w)"

# for m in re.findall(pattern_device, text):
#     # device.device_name = m[0]
#     print(m[1])
#     version = m[1]
#     fw_version = m[2]
#     sensor_count = m[3]
#     serial = m[4]
#     pcb = m[5]
#     cid = m[6]
#     lot = m[7]
#     zone = m[8]
#     measurement_delay = m[9]
#     moving_avg = m[10]
#     user_alarm_config = m[11]
#     user_clock_config = m[12]
#     alarm_indication = m[13]
#     temp_unit = m[14]
# report_history_length = m[15]
# det_report = m[16]


pattern = "Date:\s+(?P<DATE>\d+\-\d+\-\d+)\s+" \
          "Min T:\s+(?P<Min_T>[+-]?\d+\.\d+)\,\s+" \
          "TS Min T:\s+(?P<TS_Min_T>\d+\:\d+)\s+" \
          "Max T:\s+(?P<Max_T>[+-]\d+\.\d+)\,\s+" \
          "TS Max T:\s+(?P<TS_Max_T>\d+\:\d+)\s+" \
          "Avrg T:\s+(?P<Avrg_T>[+-]\d+\.\d+)\s+" \
          "Alarm:\s+\d:\s+t Acc:\s+(?P<t_Acc_0>\d+)\s+\d\:\s+" \
          "t Acc:\s+(?P<t_Acc_1>\d+)\s+Int Sensor timeout:\s+" \
          "t AccST:\s+(?P<t_AccST>\d+)\s+" \
          "Events:\s+(?P<Events>\d+)"
#
# result = re.findall(pattern, text)

# print(result)
#
#
for m in re.findall(pattern, text):
    print('--------------------')
    print(m[0])
    print(m[1])
    # print(m.group(0))
    # print(m.group("DATE")),
    # print(m.group("Min_T")),
    # print(m.group("TS_Min_T")),
    # print(m.group("Max_T")),
    # print(m.group("TS_Max_T")),
    # print(m.group("Avrg_T")),
    # print(m.group("t_Acc_0")),
    # print(m.group("t_Acc_1")),
    # print(m.group("t_AccST")),
    # print(m.group("Events")),
    # print(m.group("t_AccST")),
    # print(m.group("Events"))

# if __name__ == '__main__':
#     filename = 'data.txt'
#     parse_file(filename)

# Search for the word using regex
# for m in re.finditer(r'[+-](\d+\.\d+)', text):
#     print(m.span())
#     print(m.group(0))

# item = 4
# for i in range(4):
#     # Print the matches
# print(matches)
