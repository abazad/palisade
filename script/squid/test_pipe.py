import sys

while True:
	try:
		line = sys.stdin.readline()
		line = line.strip()
		user, password = line.split(' ')
	except KeyboardInterrupt:
		break
	else:
		sys.stdout.write('User/Password: %s/%s\n' % (user, password))
		sys.stdout.flush()
