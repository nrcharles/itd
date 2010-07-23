# a simple tcp server

import SocketServer
from sys import exit, argv
import mpd
version ='0.1'
mpdport = 6600

mpd = mpd.MPDaemon()

class EchoRequestHandler(SocketServer.BaseRequestHandler ):
    def setup(self):
        print self.client_address, 'connected!'
        self.request.send('OK MPD ' + version + '\n')

    def handle(self):
        data = 'dummy'
        while data:
            data = self.request.recv(1024)
            print data
            #self.request.send(mpd.command(data))
            ret = mpd.command(data)
            print ret
            self.request.send(ret)
            if data.strip() == 'bye':
                return

    def finish(self):
        print self.client_address, 'disconnected!'
        self.request.send('bye ' + str(self.client_address) + '\n')

    #server host is a tuple ('host', port)

def usage():
    pass

if __name__ == "__main__":
    import getopt

    opts, args = getopt.getopt(argv[1:], 'dfh',["username=","password="])

    if opts:
        for o,a in opts:
            if o == '-h':
                usage()
                exit(1)
            if o == '-d':
                #run in background
                import daemon
                daemon.daemonize()
            if o == '-f':
                #run in forground
                print "Running in Foreground"
    else:
        usage()
        exit(1)

    try:
        server = SocketServer.ThreadingTCPServer(('', mpdport), EchoRequestHandler)
        server.serve_forever()


    except (KeyboardInterrupt, SystemExit):
        exit(1)
    except:
        raise
