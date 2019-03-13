def getVirtualSerial():
		import subprocess
		result = subprocess.Popen(['python', '/Users/willwade/bin/RelayKeys/resources/demoSerial.py'],stdout=subprocess.PIPE,close_fds=True)
		if result.returncode == 0:
			return result.stdout
		else:
			if result.stderr:
				Style.error('Preprocess failed: ')
				logger.critical(result.stderr)
			return '' 

print(getVirtualSerial())