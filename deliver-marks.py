import os
import sys
import time

# -*- encoding: utf8 -*-

def main(marksFile):
    f = open(marksFile)
    #with  as f:
    task_names = {}
    for line in f:
	if line.startswith('#fio,user'):
	    splitted = line.strip().split(',')
	    for ind, name in enumerate(splitted[2:]):
		task_names[ind] = name

	if line[0] in ('#', '-') or line == '':
	    continue
	splitted = line.strip().split(',')
	name, userName, tasks = splitted[0], splitted[1], splitted[2:]
	if userName == '':
	    continue
	print(name, userName, tasks)
	homedir = os.path.join('/home/' + userName)
	if not(os.path.exists(homedir) and os.path.isdir(homedir)):
	    print('Sorry, no such homedir %s' % repr(homedir))
	    sys.exit(1)
	line_fio = '  ' + name
	line_time = '  Generated at ' + time.ctime()
	#line1 = ' %s' % '|'.join('%2d' % (i+1) for i in range(len(tasks)))
	#line2 = (' ' * 1 +
	#	'|'.join('%2s' % (i) for i in (tasks)))
#	print(['%2s' % (i) for i in (tasks)])
	line1 = []
	for ind, i in enumerate(tasks):
		line1.append('%15s %s\n' % (task_names.get(ind, 'Unknown'), i))
	line1 = ''.join(line1)



	print(task_names)
	print(line1)
	filename = os.path.join(homedir, 'UNIX_MARKS.txt')
	print(filename)
	f1 =  open(filename, 'w')
	os.chmod(filename, 0644)

	print >> f1, line_fio
	print >> f1, line_time
	print >> f1, line1
	f1.close()

if __name__ == "__main__":
    main(sys.argv[1])
            
