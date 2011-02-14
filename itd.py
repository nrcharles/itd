# Python MPD/iTunes library
# Copyright (C) 2010 Nathan Charles
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

HELLO_PREFIX = "OK MPD "
ERROR_PREFIX = "ACK "
SUCCESS = "OK"
NEXT = "list_OK"

import appscript
import math
import SocketServer
class iTunesModel(object):
    """This class maps mpd keywords to iTunes applescript calls
    """
    def __init__(self):
        try:
            self.iTunes = appscript.app('iTunes')
        except:
            return -1

    def _getstate(self):
        """This is a setup function in case iTunes views have changed and
        current state is undefined
        returns tuple of playlist and track"""
        playlist = ""
        track = ""
        try:
            playlist = self.iTunes.current_playlist()
            track = self.iTunes.current_track()

        except:
            try:
                self.iTunes.play()
                self.iTunes.pause()
            except:
                return -1,-1

        return playlist, track


    def undefined():
        """
        playid [SONGID]
        Begins playing the playlist at song SONGID.

        seek {SONGPOS} {TIME}
        Seeks to position TIME (in seconds) of entry SONGPOS in the playlist.

        seekid {SONGID} {TIME}
        Seeks to the position TIME (in seconds) of song SONGID.
        """
        pass

    def play(self, song = -1):
        """
        play [SONGPOS]
        Begins playing the playlist at song number SONGPOS.
        """
        self.iTunes.play()
        #return True

    def pause(self, bool = 1):
        """
        pause {PAUSE}
        Toggles pause/resumes playing, PAUSE is 0 or 1.

        Note
        The use of pause command w/o the PAUSE argument is deprecated.
        """
        self.iTunes.pause()
        #return True

    def next(self):
        """
        Plays next song in the playlist.
        """
        self.iTunes.next_track()
        #return True

    def previous(self):
        """
        Plays previous song in the playlist.
        """
        self.iTunes.previous_track()
        #return True
        
    def stop(self):
        """
        Stops playing.
        """
        self.iTunes.stop()
        #return True

    #STATUS
    def status(self):
        """
        volume: 0-100
        repeat: 0 or 1
        single: 0 or 1
        consume: 0 or 1
        playlist: 31-bit unsigned integer, the playlist version number
        playlistlength: integer, the length of the playlist
        state: play, stop, or pause
        song: playlist song number of the current song stopped on or playing
        songid: playlist songid of the current song stopped on or playing
        nextsong:  playlist song number of the next song to be played
        nextsongid: playlist songid of the next song to be played
        time: total time elapsed (of current playing/paused song)
        elapsed: 
             Total time elapsed within the current song, with higher resolution.
        bitrate: instantaneous bitrate in kbps
        xfade: crossfade in seconds
        audio: sampleRate:bits:channels
        updatings_db: job id
        error: if there is an error, returns message here

        volume: -1\nrepeat: 0\nrandom: 0\nsingle: 0\nconsume: 0\nplaylist: 2\nplaylistlength: 0\nxfade: 0\nstate: stop\nlist_OK\nOK\n

        0.15.0
        volume: 100
        repeat: 0
        random: 0
        single: 0
        consume: 0
        playlist: 5
        playlistlength: 3
        xfade: 0
        state: play
        song: 0
        songid: 0
        time: 284:390
        bitrate: 256
        audio: 44100:24:2
        nextsong: 1
        nextsongid: 1

        list_OK

        file: Us vs Us/01 Banner.mp3
        Time: 390
        Artist: Psalters
        Title: Banner
        Album: Us vs Us
        Track: 1/14
        Date: 2004
        Genre: World
        Disc: 1/1
        Pos: 0
        Id: 0
        list_OK
        OK
        """
        cplaylist, ctrack = self._getstate()

        repeat = {appscript.k.off: [0,0],
                appscript.k.one:[1,1],
                appscript.k.all:[1,0]}
        #stopped/playing/paused/fast forwarding/rewinding'
        state = { appscript.k.stopped: "stop",
                appscript.k.playing:  "play",
                appscript.k.paused:   "pause",
                appscript.k.fast_forwarding: "play",
                appscript.k.rewinding: "play"}
        random = { True : 1,
                False : 0}

        ret = "volume: %s\n"  % self.iTunes.sound_volume.get()
        ret += "repeat: %s\n" % repeat[cplaylist.song_repeat.get()][0]
        ret += "random: %s\n" % random[cplaylist.shuffle.get()] 
        ret += "single: %s\n" % repeat[cplaylist.song_repeat.get()][1]
        ret += "consume: %s\n" % "0"
        ret += "playlist: %s\n" % "2" 
        ret += "playlistlength: %s\n" % cplaylist.duration.get()  
        ret += "xfade: %s\n" % "0"
        ret += "state: %s\n" % state[self.iTunes.player_state.get()]
        ret += "song: %s\n" % "1"
        ret += "songid: %s\n" % "1"
        ret += "time: %s:%s\n" % ( self.iTunes.player_position.get(), 
                math.trunc(ctrack.duration.get()))
        ret += "bitrate: %s\n" % "256"
        ret += "audio: %s\n" % "44100:24:2"
        ret += "nextsong: %s\n" % "2"
        ret += "nextsongid: %s\n" % "2"
        return ret

    def stats(self):
        """
        Displays statistics.
        artists: number of artists
        songs: number of albums
        uptime: daemon uptime in seconds
        db_playtime: sum of all song times in the db
        db_update: last db update in UNIX time
        playtime: time length of music played
        """
        pass

    def currentsong(self):
        cplaylist, ctrack = self._getstate()

        ret = "Time: %s\n" % math.trunc(ctrack.duration.get())
        ret += "Album: %s\n" % ctrack.album.get() 
        ret += "Artist: %s\n" % ctrack.artist.get() 
        ret += "Title: %s\n" % self.iTunes.current_track.name.get()
        ret += "Track: %s\n" % self.iTunes.current_track.track_number.get()
        ret += "Pos: %s\n" % self.iTunes.player_position.get()
        return ret

    def plchanges(self, args):
        pass

    def lsinfo(self, args):
        """
        Usage 
        lsinfo [<string directory>]
        Purpose 
        List contents of <string directory>, from the database.
        Arguments
        <string directory>
        """
        pass

    def search(self, args):
        """
        search <string type> <string what>

        search filename bastards_pick_wrong_man
        file: vocal/onion_radio_news/the_onion_radio_news_-_bastards_pick_wrong_man.mp3
        Time: 36
        Artist: Onion Radio News 
        Title: Bastards Pick Wrong Man to Mess With
        Genre: Comedy
        OK
        """
        print args
        cplaylist, ctrack = self._getstate()

        type,what = args.split('" "')
        ret = ""
        query = what.strip().strip('\"')
        #print cplaylist.file_tracks()
        print "query '%s'" % query
        for i in cplaylist.search(for_=query):
            ret += "file: %s/%s.mp3\n" % (i.artist(), i.name())
            #print i.file_track.location()
            ret += "Time: %s\n" % math.trunc(i.duration())
            ret += "Title: %s\n" % i.name()
            ret += "Artist: %s\n" % i.artist()
            ret += "Album: %s\n" % i.album()
            ret += "Track: %s\n" % i.track_number()
            ret += "Date: %s\n" % i.year()
            ret += "Genre: %s\n" % i.genre()
        return ret
        

    #PLAYBACK OPTIONS
    def consume(self, args):
        """
        consume {STATE}
        Sets consume state to STATE, STATE should be 0 or 1. When consume is activated, each song played is removed from playlist.

        """
        pass

    def crossfade(self, args):
        """
        crossfade {SECONDS}
        Sets crossfading between songs.
        """
        pass

    def random(self, args):
        """
        random {STATE}
        Sets random state to STATE, STATE should be 0 or 1.

        song repeat (off/one/all) : playback repeat mode
        """
        pass

    def repeat(self, args):
        """
        repeat {STATE}
        Sets repeat state to STATE, STATE should be 0 or 1.

        song repeat (off/one/all) : playback repeat mode
        """
        cplaylist, ctrack = self._getstate()
        state = { "off":0, "all":1}
        cplaylist.song_repeat.set(state[args])

    def single(self, args):
        """
        single {STATE}
        Sets single state to STATE, STATE should be 0 or 1. When single is 
        activated, playback is stopped after current song, or song is repeated 
        if the 'repeat' mode is enabled.
        """
        cplaylist, ctrack = self._getstate()
        state = { "off":0, "one":1}
        cplaylist.song_repeat.set(state[args])


    def setvol(self, args):
        """
        setvol {VOL}
        Sets volume to VOL, the range of volume is 0-100.
        """
        self.iTunes.sound_volume.set(args)

    def to_code():
        """
        Playback options

        replay_gain_mode {MODE}
        Sets the replay gain mode. One of off, track, album.

        Changing the mode during playback may take several seconds, because 
        the new settings does not affect the buffered data.

        This command triggers the options idle event.

        replay_gain_status
        Prints replay gain options. Currently, only the variable 
        replay_gain_mode is returned.
        """
        pass


class controller(object):
    """This class impliments a controller that parses data into commands and 
    handles executes those commands

    The default backend is iTunes via applescript but something else could be
    implimented.
    """
    def __init__(self, backend = iTunesModel()):
        self.iterate = False
        self.model = backend
        self._commands = {
            # Status Commands
            "clearerror":       self._undefined,
            "currentsong":      self.model.currentsong,
            "idle":             self._undefined,
            "noidle":           None,
            "status":           self.model.status,
            "stats":            self._undefined,
            # Playback Option Commands
            "consume":          self._undefined,
            "crossfade":        self._undefined,
            "random":           self.model.random,
            "repeat":           self.model.repeat,
            "setvol":           self.model.setvol,
            "single":           self.model.single,
            "volume":           self._undefined,
            # Playback Control Commands
            "next":             self.model.next,
            "pause":            self.model.pause,
            "play":             self.model.play,
            "playid":           self._undefined,
            "previous":         self.model.previous,
            "seek":             self._undefined,
            "seekid":           self._undefined,
            "stop":             self._undefined,
            # Playlist Commands
            "add":              self._undefined,
            "addid":            self._undefined,
            "clear":            self._undefined,
            "delete":           self._undefined,
            "deleteid":         self._undefined,
            "move":             self._undefined,
            "moveid":           self._undefined,
            "playlist":         self._undefined,
            "playlistfind":     self._undefined,
            "playlistid":       self._undefined,
            "playlistinfo":     self._undefined,
            "playlistsearch":   self._undefined,
            "plchanges":        self.model.plchanges,
            "plchangesposid":   self._undefined,
            "shuffle":          self._undefined,
            "swap":             self._undefined,
            "swapid":           self._undefined,
            # Stored Playlist Commands
            "listplaylist":     self._undefined,
            "listplaylistinfo": self._undefined,
            "listplaylists":    self._undefined,
            "load":             self._undefined,
            "playlistadd":      self._undefined,
            "playlistclear":    self._undefined,
            "playlistdelete":   self._undefined,
            "playlistmove":     self._undefined,
            "rename":           self._undefined,
            "rm":               self._undefined,
            "save":             self._undefined,
            # Database Commands
            "count":            self._undefined,
            "find":             self._undefined,
            "list":             self._undefined,
            "listall":          self._undefined,
            "listallinfo":      self._undefined,
            "lsinfo":           self._undefined,
            "search":           self.model.search,
            "update":           self._undefined,
            # Connection Commands
            "close":            None,
            "kill":             None,
            "password":         self._undefined,
            "ping":             self._undefined,
            # Audio Output Commands
            "disableoutput":    self._undefined,
            "enableoutput":     self._undefined,
            "outputs":          self._undefined,
            # Reflection Commands
            "commands":         self._undefined,
            "notcommands":      self._undefined,
            "tagtypes":         self._undefined,
            "urlhandlers":      self._undefined,
            # stuff
            "command_list_ok_begin":    self._undefined,
            "command_list_end":    self._undefined,
        }
    def _undefined(self, attr=None):
        print "undefined"

    def _execute(self, command):
        cmd, sep, args = command.partition(' ')
        print "running command: %s" % cmd
        if cmd:
            if args:
                return self._commands[cmd.strip()](args)
            else:
                return self._commands[cmd.strip()]()

    def handle(self, command):
        retval = ''
        if command.find('list_ok') is not -1:
            ListOK = True
        else:
            ListOK = False
        if command.find('command_list') is not -1:
            command_list = command.strip().split('\n')
            print command_list
            for c in command_list:
                if c:
                    rc = self._execute(c)
                    if rc:
                        retval += rc
                        if ListOK:
                            retval += NEXT + "\n"
        else:
            retval = self._execute(command) 
        if retval:
            return "%sOK\n" % retval
        else:
            return "OK\n"


def escape(text):
    return text.replace("\\", "\\\\").replace('"', '\\"').replace(' ',"_")

class iTDRequestHandler(SocketServer.BaseRequestHandler ):
    """This class provides an interface which impliments the mpd spec
    """
    def setup(self):
        print self.client_address, 'connected!'
        self.request.send('OK MPD ' + version + '\n')

    def handle(self):
        data = 'dummy'
        while data:
            data = self.request.recv(1024)
            print data
            #self.request.send(mpd.command(data))
            ret = mpd.handle(data)
            print ret
            self.request.send(ret)

    def finish(self):
        print self.client_address, 'disconnected!'


def usage():
    pass

if __name__ == "__main__":
    import getopt
    import sys

    opts, args = getopt.getopt(sys.argv[1:], 'dfh')

    if opts:
        for o,a in opts:
            if o == '-h':
                usage()
                sys.exit(1)
            if o == '-d':
                #run in background
                import daemon
                daemon.daemonize()
            if o == '-f':
                #run in forground
                print "Running in Foreground"
    else:
        usage()
        sys.exit(1)

    try:
        version ='0.1'
        mpdport = 6600
        mpd = controller()
        server = SocketServer.ThreadingTCPServer(('', mpdport), 
                iTDRequestHandler)
        server.serve_forever()

    except (KeyboardInterrupt, SystemExit):
        sys.exit(1)
    except:
        raise
