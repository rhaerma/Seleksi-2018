
import sys
def testArgs():
    if (sys.argv[0]):
        print('gotcha')
        print(len(sys.argv))
    else:
        print('1')