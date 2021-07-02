import pypozyx
from pypozyx import get_first_pozyx_serial_port, PozyxSerial, UWBSettings
# print(pypozyx.get_first_pozyx_serial_port())
serial_port = get_first_pozyx_serial_port()
if serial_port is not None:
    pozyx = PozyxSerial(serial_port)
    # print(pozyx)
    uwb_settings = UWBSettings()
    # print("uwb_settings: ",uwb_settings)
    pozyx.getUWBSettings(uwb_settings)
    # print("uwb_settings: ",uwb_settings)
else:
    print("No Pozyx port was found")



from pypozyx import PozyxSerial, get_first_pozyx_serial_port, POZYX_SUCCESS, SingleRegister, EulerAngles, Acceleration
# initalize the Pozyx as above


# initialize the data container
who_am_i = SingleRegister()
print("who_am_i: ",who_am_i)
# get the data, passing along the container
status = pozyx.getWhoAmI(who_am_i)
print("status: ", status)
tagid = pozyx.getTagIds(who_am_i)
print("tagid: ", tagid)
# check the status to see if the read was successful. Handling failure is covered later.
if status == POZYX_SUCCESS:
# if status == 1:
    # print the container. Note how a SingleRegister will print as a hex string by default.
    print(who_am_i) # will print '0x43'
# if status == POZYX_FAILURE:
#     print("fal")
# and repeat
# initialize the data container
acceleration = Acceleration()
# get the data, passing along the container
pozyx.getAcceleration_mg(acceleration)
print("acceleraion: ",acceleration)
# initialize the data container
euler_angles = EulerAngles()
# get the data, passing along the container
pozyx.getEulerAngles_deg(euler_angles)
print("euler_angles: ", euler_angles)


uwb_channel = SingleRegister(5)
pozyx.setUWBChannel(uwb_channel)


uwb_settings = UWBSettings(channel=5, bitrate=1, prf=2, plen=0x08, gain_db=25.0)
# print(uwb_settings)

from pypozyx import PozyxSerial, get_first_pozyx_serial_port, POZYX_SUCCESS, SingleRegister, PozyxConstants, Coordinates, DeviceCoordinates
from pypozyx import POZYX_SUCCESS, POZYX_FAILURE, POZYX_TIMEOUT


remote_device_id = 0x6a7a
# this will read the WHO_AM_I register of the remote tag
who_am_i = SingleRegister()
pozyx.getWhoAmI(who_am_i)
print(who_am_i) # will print 0x43