# Python MPD client library
# Copyright (C) 2008-2010  J. Alexander Treuman <jat@spatialrift.net>
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

class MPDError(Exception):
    pass

class ConnectionError(MPDError):
    pass

class ProtocolError(MPDError):
    pass

class CommandError(MPDError):
    pass

class CommandListError(MPDError):
    pass

class PendingCommandError(MPDError):
    pass

class IteratingError(MPDError):
    pass

from appscript import *
import math
class iTDaemon(object):
    def __init__(self):
        self.iTunes = app('iTunes')

    def undefined():
        """
        playid [SONGID]
        Begins playing the playlist at song SONGID.

        seek {SONGPOS} {TIME}
        Seeks to the position TIME (in seconds) of entry SONGPOS in the playlist.

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
    def pause(self, bool = 1):
        """
        pause {PAUSE}
        Toggles pause/resumes playing, PAUSE is 0 or 1.

        Note
        The use of pause command w/o the PAUSE argument is deprecated.
        """
        self.iTunes.pause()
    def next(self):
        """
        Plays next song in the playlist.
        """
        self.iTunes.next_track()
    def previous(self):
        """
        Plays previous song in the playlist.
        """
        self.iTunes.previous_track()
    def stop(self):
        """
        Stops playing.
        """
        self.iTunes.stop()

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
        elapsed: Total time elapsed within the current song, but with higher resolution.
        bitrate: instantaneous bitrate in kbps
        xfade: crossfade in seconds
        audio: sampleRate:bits:channels
        updatings_db: job id
        error: if there is an error, returns message here

        volume: -1\nrepeat: 0\nrandom: 0\nsingle: 0\nconsume: 0\nplaylist: 2\nplaylistlength: 0\nxfade: 0\nstate: stop\nlist_OK\nOK\n
        """
        repeat = {k.off: ["0","0"],
                k.one:["1","1"],
                k.all:["1","0"]}
        #stopped/playing/paused/fast forwarding/rewinding'
        state = { k.stopped: "stop",
                k.playing:  "play",
                k.paused:   "pause",
                k.fast_forwarding: "play",
                k.rewinding: "play"}
        random = { True : "1",
                False : "0"}
        ret = "volume: %s\n"  % self.iTunes.sound_volume.get()
        ret += "repeat: %s\n" % repeat[self.iTunes.current_playlist.song_repeat.get()][0]
        ret += "random: %s\n" % random[self.iTunes.current_playlist.shuffle.get()] 
        ret += "single: %s\n" % repeat[self.iTunes.current_playlist.song_repeat.get()][1]
        ret += "consume: %s\n" % "0"
        ret += "playlist: %s\n" % "2" 
        ret += "playlistlength: %s\n" % self.iTunes.current_playlist.duration.get()  
        ret += "xfade: %s\n" % "0"
        ret += "state: %s\n" % state[self.iTunes.player_state.get()]
        ret += "time: %s\n" % self.iTunes.player_position.get()
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
        ret = "Time: %s\n" % math.trunc(self.iTunes.current_track.duration.get())
        ret += "Album: %s\n" % self.iTunes.current_track.album.get() 
        ret += "Artist: %s\n" % self.iTunes.current_track.artist.get() 
        ret += "Title: %s\n" % self.iTunes.current_track.name.get()
        ret += "Track: %s\n" % self.iTunes.current_track.track_number.get()
        ret += "Pos: %s\n" % self.iTunes.player_position.get()
        return ret

    #PLAYBACK OPTIONS
    def to_code():
        """
        Playback options

        consume {STATE}
        Sets consume state to STATE, STATE should be 0 or 1. When consume is activated, each song played is removed from playlist.

        crossfade {SECONDS}
        Sets crossfading between songs.

        random {STATE}
        Sets random state to STATE, STATE should be 0 or 1.

        repeat {STATE}
        Sets repeat state to STATE, STATE should be 0 or 1.

        setvol {VOL}
        Sets volume to VOL, the range of volume is 0-100.

        single {STATE}
        Sets single state to STATE, STATE should be 0 or 1. When single is activated, playback is stopped after current song, or song is repeated if the 'repeat' mode is enabled.

        replay_gain_mode {MODE}
        Sets the replay gain mode. One of off, track, album.

        Changing the mode during playback may take several seconds, because the new settings does not affect the buffered data.

        This command triggers the options idle event.

        replay_gain_status
        Prints replay gain options. Currently, only the variable replay_gain_mode is returned.
        """
        pass


class MPDaemon(object):
    def __init__(self):
        self.iterate = False
        self.itd = iTDaemon()
        self._commands = {
            # Status Commands
            "clearerror":       self._fetch_nothing,
            "currentsong":      self.itd.currentsong,
            "idle":             self._fetch_list,
            "noidle":           None,
            "status":           self.itd.status,
            "stats":            self._fetch_object,
            # Playback Option Commands
            "consume":          self._fetch_nothing,
            "crossfade":        self._fetch_nothing,
            "random":           self._fetch_nothing,
            "repeat":           self._fetch_nothing,
            "setvol":           self._fetch_nothing,
            "single":           self._fetch_nothing,
            "volume":           self._fetch_nothing,
            # Playback Control Commands
            "next":             self.itd.next,
            "pause":            self.itd.pause,
            "play":             self.itd.play,
            "playid":           self._fetch_nothing,
            "previous":         self.itd.previous,
            "seek":             self._fetch_nothing,
            "seekid":           self._fetch_nothing,
            "stop":             self._fetch_nothing,
            # Playlist Commands
            "add":              self._fetch_nothing,
            "addid":            self._fetch_item,
            "clear":            self._fetch_nothing,
            "delete":           self._fetch_nothing,
            "deleteid":         self._fetch_nothing,
            "move":             self._fetch_nothing,
            "moveid":           self._fetch_nothing,
            "playlist":         self._fetch_playlist,
            "playlistfind":     self._fetch_songs,
            "playlistid":       self._fetch_songs,
            "playlistinfo":     self._fetch_songs,
            "playlistsearch":   self._fetch_songs,
            "plchanges":        self._fetch_songs,
            "plchangesposid":   self._fetch_changes,
            "shuffle":          self._fetch_nothing,
            "swap":             self._fetch_nothing,
            "swapid":           self._fetch_nothing,
            # Stored Playlist Commands
            "listplaylist":     self._fetch_list,
            "listplaylistinfo": self._fetch_songs,
            "listplaylists":    self._fetch_playlists,
            "load":             self._fetch_nothing,
            "playlistadd":      self._fetch_nothing,
            "playlistclear":    self._fetch_nothing,
            "playlistdelete":   self._fetch_nothing,
            "playlistmove":     self._fetch_nothing,
            "rename":           self._fetch_nothing,
            "rm":               self._fetch_nothing,
            "save":             self._fetch_nothing,
            # Database Commands
            "count":            self._fetch_object,
            "find":             self._fetch_songs,
            "list":             self._fetch_list,
            "listall":          self._fetch_database,
            "listallinfo":      self._fetch_database,
            "lsinfo":           self._fetch_database,
            "search":           self._fetch_songs,
            "update":           self._fetch_item,
            # Connection Commands
            "close":            None,
            "kill":             None,
            "password":         self._fetch_nothing,
            "ping":             self._fetch_nothing,
            # Audio Output Commands
            "disableoutput":    self._fetch_nothing,
            "enableoutput":     self._fetch_nothing,
            "outputs":          self._fetch_outputs,
            # Reflection Commands
            "commands":         self._fetch_list,
            "notcommands":      self._fetch_list,
            "tagtypes":         self._fetch_list,
            "urlhandlers":      self._fetch_list,
            # stuff
            "command_list_ok_begin":    self._fetch_nothing,
            "command_list_end":    self._fetch_nothing,
        }
    def _fetch_list(self):
        pass
    def _fetch_nothing(self):
        pass
    def _fetch_object(self):
        pass
    def _fetch_item(self):
        pass
    def _fetch_songs(self):
        pass
    def _fetch_database(self):
        pass
    def _fetch_playlist(self):
        pass
    def _fetch_changes(self):
        pass
    def _fetch_playlists(self):
        pass
    def _fetch_outputs(self):
        pass

    def command(self,command):
        retval = ''
        if command not in self._commands:
            print command.strip().split('\n')
            command_list = command.strip().split('\n')
            for c in command_list:
                print "running command: %s" % c
                rc = self._commands[c]()
                if rc:
                    retval += rc + NEXT + "\n"
        else:
            retval = self._commands[command]() 
        retval = retval + "OK" + '\n'
        print retval
        return retval


def escape(text):
    return text.replace("\\", "\\\\").replace('"', '\\"')


# vim: set expandtab shiftwidth=4 softtabstop=4 textwidth=79:
