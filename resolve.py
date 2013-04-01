import re, os, sys
from subprocess import check_output
import shlex

def findlib(path, name):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def resolve_line(m_obj):
    if m_obj is None:
        return
    i = m_obj.group(1)
    addr = m_obj.group(2)
    so = m_obj.group(4)
    os_file = findlib(resolve_line.path, so)
    if os_file is not None:
        #err if use shlex, why?
        out = check_output('addr2line -e %s %s' % (os_file, addr), shell=True)
        print '#%s %s' % (i, out)

def resolve(logfile, search_path):
    resolve_line.path = search_path
    t_re = re.compile(r'.*#(\d+)\s+pc\s+([0-9a-z]+)\s+(/.*/)(.*\.so)', re.I)
    with open(logfile) as f:
        for line in f:
            m = t_re.match(line)
            resolve_line(m)


def main():
    resolve(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()    
