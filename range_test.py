from pypozyx import (PozyxSerial, PozyxConstants, version,
                     SingleRegister, DeviceRange, POZYX_SUCCESS, POZYX_FAILURE, get_first_pozyx_serial_port)

from pypozyx.tools.version_check import perform_latest_version_check
import time

class ReadyToRange(object):
	def __init__(self, pozyx, destination_id, range_step_mm=1000, protocol=PozyxConstants.RANGE_PROTOCOL_PRECISION,\
		remote_id=None):
		self.pozyx = pozyx
		self.destination_id = destination_id
		self.range_step_mm = range_step_mm
		self.remote_id = remote_id
		self.protocol = protocol

	def setup(self):
		print("------------POZYX RANGING V{} -------------".format(version))
		if self.remote_id is None:
			for device_id in [self.remote_id, self.destination_id]:
				self.pozyx.printDeviceInfo(device_id)
		else:
			for device_id in [None, self.remote_id, self.destination_id]:
				self.pozyx.printDeviceInfo(device_id)

	def loop(self):
		device_range = DeviceRange()
		status = self.pozyx.doRanging(
			self.destination_id, device_range, self.remote_id)
		if status == POZYX_SUCCESS:
			print(device_range)
		else:
			error_code = SingleRegister()
			status = self.pozyx.getErrorCode(error_code)
			if status == POZYX_SUCCESS:
				print("\033[93m error ranging, local %s\033[0m" % self.pozyx.getErrorCode(error_code))
			else:
				print("ERROR Ranging, couldn't retrieve local error")

if __name__ == "__main__":
	check_pypozyx_version = True
	if check_pypozyx_version:
		perform_latest_version_check()
	
	serial_port = get_first_pozyx_serial_port()
	if serial_port is None:
		print("No Pozyx connected. Check your USB cable or your driver!")
		quit()

	remote_id = 0x6a7a
	remote = False
	if not remote:
		remote_id = None

	destination_id = 0x6a7a
	ranging_protocol = PozyxConstants.RANGE_PROTOCOL_PRECISION

	range_step_mm = 1000

	pozyx = PozyxSerial(serial_port)
	r = ReadyToRange(pozyx, destination_id, range_step_mm, ranging_protocol, remote_id)

	# r.setup()
	while True:
		r.loop()
		time.sleep(0.5)

