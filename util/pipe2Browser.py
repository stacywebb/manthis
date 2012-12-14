#!/opt/local/bin/python
import getopt, sys, os
import tempfile

def usage():
    print 'pipe2Browser -h -b </Applications/YourBrowser.app>'
    sys.exit()
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hb:")
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    browser = '/Applications/Safari.app'
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o == "-h":
            usage()
            sys.exit()
        else:
            assert False, "unhandled option"
    
    # be a good citizen and clean up past files
    os.system('rm -f /tmp/*.diff.html')
    
    htmlText = sys.stdin.read()
    tmpfile = tempfile.NamedTemporaryFile(mode='w', suffix='.diff.html', dir='/tmp', delete=False)
    tmpfilename = tmpfile.name
    tmpfile.write(htmlText)
    tmpfile.close()
    
    execString = 'open -a ' + browser + ' ' + tmpfilename
    os.system(execString)


    
if __name__ == "__main__":
    main()
