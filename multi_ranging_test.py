from pypozyx import (PozyxSerial, PozyxConstants, version,
                     SingleRegister, DeviceRange, POZYX_SUCCESS, POZYX_FAILURE, get_first_pozyx_serial_port)

from pypozyx.tools.version_check import perform_latest_version_check
import time
'''
 This script can measure the distances between pozyx_computer and destination_pozyxs.
'''
class ReadyToRange(object):
	def __init__(self, pozyx, destination_id, range_step_mm=1000, protocol=PozyxConstants.RANGE_PROTOCOL_PRECISION,\
		remote_id=None):
		self.pozyx = pozyx
		self.destination_id = destination_id
		self.range_step_mm = range_step_mm
		self.remote_id = None
		self.protocol = protocol
		self.devices = [0x6a0f, 0x6a7a]

	def setup(self):
		print("------------POZYX RANGING V{} -------------".format(version))
		for device_id in self.devices:
			self.pozyx.printDeviceInfo(device_id)
		


	def loop(self):
		device_range = DeviceRange()
		for device_id in self.devices:
			status = self.pozyx.doRanging(device_id, device_range, self.remote_id)
			if status == POZYX_SUCCESS:
				print(hex(device_id)," : ",device_range)
			else:
				error_code = SingleRegister()
				status = self.pozyx.getErrorCode(error_code)
				if status == POZYX_SUCCESS:
					print("\033[93m error ranging, local %s\033[0m" % self.pozyx.getErrorCode(error_code))
				else:
					print("ERROR Ranging, couldn't retrieve local error")
        
	
if __name__ == "__main__":
	# check_pypozyx_version = True
	# if check_pypozyx_version:
	# 	perform_latest_version_check()
	
	serial_port = get_first_pozyx_serial_port()
	if serial_port is None:
		print("No Pozyx connected. Check your USB cable or your driver!")
		quit()

	remote_id = 0x6a0f
	remote = True
	if not remote:
		remote_id = None

	destination_id = 0x6a7a
	ranging_protocol = PozyxConstants.RANGE_PROTOCOL_PRECISION

	range_step_mm = 1000

	pozyx = PozyxSerial(serial_port)
	r = ReadyToRange(pozyx, destination_id, range_step_mm, ranging_protocol, remote_id)

	r.setup()
	while True:
		r.loop()
		time.sleep(0.5)

