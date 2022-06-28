import ctypes
import ctypes.util
import sys

libc = ctypes.CDLL( ctypes.util.find_library('c') )

def listxattr(path):
    size = 0
    while True:
        size += 1024
        buf = ctypes.create_string_buffer(size)
        got = libc.listxattr(path,buf,size,0)
        if got <= 0:
            return []
        if got < size:
            return buf.raw[:got - 1].split('\x00')

def getxattr(path,xattr):
    size = 0
    while True:
        size += 1024
        buf = ctypes.create_string_buffer(size)
        got = libc.getxattr(path,xattr,buf,size,0,0)
        if got == 0:
            return None
        if got < size:
            return buf.raw[:got]

def getxattrs(path):
    for xattr in listxattr(path):
        yield xattr,getxattr(path,xattr)


if __name__ == '__main__':

    result = {'xattr': {}}
    result['fname'] = sys.argv[-1]

    for k,v in getxattrs(sys.argv[-1]):
        result['xattr'][k] = v
        #print(repr(v))

    if result['xattr'] != {}:
        #print(result)
        for key in result['xattr'].keys():
            print('{}: {}'.format(key, result['xattr'].get(key)))
