import subprocess

from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection

class ClamAV(ServiceBase):
	def __init__(self, config=None):
		super(ClamAV, self).__init__(config)

	def start(self):
		self.log.debug("ClamAV service started")

	def stop(self):
		self.log.debug("ClamAV service ended")

	def execute(self, request):
		result = Result()
		file_path = request.file_path

		p1 = subprocess.Popen("clamscan " + file_path, shell=True, stdout=subprocess.PIPE)
		p1.wait()
		stdout = p1.communicate()[0].decode("utf-8")

		report = stdout.split("\n")
		report = list(filter(None, report))

		text_section = ResultSection("Successfully scanned the file")
		if "FOUND" in report[0]:
			text_section.set_heuristic(1)

		for l in report:
			text_section.add_line(l)

		result.add_section(text_section)
		request.result = result