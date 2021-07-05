from pypozyx import (PozyxSerial, PozyxConstants, version,
					 SingleRegister, DeviceRange, POZYX_SUCCESS, POZYX_FAILURE, get_first_pozyx_serial_port)

from pypozyx.tools.version_check import perform_latest_version_check
import time
'''
 1. This script can calculate the accuracy of measurement between pozyx_computer and destination_pozyxs.
 2. destination_pozyxs's ID should be added in devices list
 3. The distance measurement is not stable
'''
class ReadyToRange(object):
	def __init__(self, pozyx, devices, protocol=PozyxConstants.RANGE_PROTOCOL_PRECISION,\
		remote_id=None):
		self.pozyx = pozyx
		self.remote_id = None
		self.protocol = protocol
		self.devices = devices

	def setup(self):
		print("------------POZYX RANGING V{} -------------".format(version))
		self.pozyx.printDeviceInfo(None)
		for device_id in self.devices:
			self.pozyx.printDeviceInfo(device_id)
		


	def ranging(self, device_id):
		device_range = DeviceRange()
		status = self.pozyx.doRanging(device_id, device_range, self.remote_id)
		# status = self.pozyx.getDeviceRangeInfo(device_id, device_range, self.remote_id)
		if status == POZYX_SUCCESS:
			print(hex(device_id)," : ",device_range)
			pass
		else:
			error_code = SingleRegister()
			status = self.pozyx.getErrorCode(error_code)
			if status == POZYX_SUCCESS:
				print("\033[93m error ranging, local %s\033[0m" % self.pozyx.getErrorCode(error_code))
			else:
				print("ERROR Ranging, couldn't retrieve local error")
		return device_range
			
	def calculate_accuracy(self, result, ground_truth,thres):
		acc = 0
		total = 50
		for i in range(total):
			if abs(result.distance - ground_truth) < thres:
				acc +=1
		return 100 * acc/total


	
if __name__ == "__main__":
	serial_port = get_first_pozyx_serial_port()
	if serial_port is None:
		print("No Pozyx connected. Check your USB cable or your driver!")
		quit()

	remote = True
	if not remote:
		remote_id = None

	ranging_protocol = PozyxConstants.RANGE_PROTOCOL_PRECISION
	ground_truth = 1640
	thres = 100
	devices = [0x6a0f, 0x6a27]

	pozyx = PozyxSerial(serial_port)
	r = ReadyToRange(pozyx, devices,ranging_protocol)

	r.setup()
	ranging_result = []

	# for i in range(10):
	while True:
		for device_id in devices:
			result = r.ranging(device_id)
			accuracy = r.calculate_accuracy(result, ground_truth, thres)
			if accuracy > 80:
				print("\033[94m",hex(device_id)," accuracy: ", accuracy, " %\033[0m")
			else:
				print(hex(device_id)," accuracy: ", accuracy, " %")
			time.sleep(0.1)

	# while True:
	# 	r.ranging()
	# 	time.sleep(0.1)

