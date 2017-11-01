import neovim
import mpv

from transcribe.util import (error, msg, fmtseconds, time_to_seconds, # noqa
                             get_timecodes)


@neovim.plugin
class Transcribe(object):
    def __init__(self, nvim):
        self._nvim = nvim
        self._player = {}

        self._last_seek = 0
        self._linenb = self._nvim.funcs.line('.')

    def _mpv_log(self, loglevel, component, message):
        if (loglevel == 'error') or ('ERROR' in message):
            err_msg = '{}: {}'.format(component, message)
            error(self._nvim, err_msg)

    @neovim.function('_transcribe_load')
    def load_media(self, args):
        """Initialize player and load media file

        Arguments:
        mediafile -- file or URL
        mode      -- audio by default
        """
        if not args:
            error(self._nvim, 'takes at least one argument')
            return

        media = args[0]
        mode = args[1] if len(args) == 2 else 'audio'

        if mode == 'audio':
            self._player = mpv.MPV(ytdl=True, video=False,
                                   log_handler=self._mpv_log)
            self._player.play(media)
        else:
            error(self._nvim, 'Wrong loading mode value')

        @self._player.event_callback('file-loaded')
        def echo_loaded(event):
            msg(self._nvim, 'media loaded')

        @self._player.event_callback('pause')
        def echo_pause(event):
            msg(self._nvim, 'playback paused')

        @self._player.event_callback('unpause')
        def echo_unpause(event):
            msg(self._nvim, 'playback resumed')

        @self._player.event_callback('seek')
        def echo_seek(event):
            seek = self._last_seek
            time_pos = fmtseconds(self._player.time_pos)

            if seek == 0:
                seek_msg = 'jump to {}'.format(time_pos)
            else:
                direction = 'forward' if seek > 0 else 'backward'
                seek_msg = 'seek {} ({:+d}s): {}'.format(direction,
                                                         seek, time_pos)

            msg(self._nvim, seek_msg)
            self._last_seek = 0

    @neovim.function('_transcribe_pause')
    def toggle_pause(self, args):
        self._player.cycle('pause')

    @neovim.function('_transcribe_speed')
    def set_speed(self, args):
        """Change playback speed

        Arguments:
        speed -- speed or increment
        mode  -- how to change speed (relative by default or set)
        """
        speed = args[0] if len(args) == 1 else 1
        mode = args[1] if len(args) == 2 else ''

        try:
            speed = round(float(speed), 1)
        except ValueError:
            error(self._nvim, 'argument should be a number')
            return

        if mode == 'set':
            self._player.speed = speed
        else:
            if (self._player.speed + speed) >= 0.1:
                self._player.speed += speed
            else:
                error(self._nvim, 'speed is already at minimum setting')
                return

        info = 'playback speed set to {:1.1f}'.format(self._player.speed)
        msg(self._nvim, info)

    @neovim.function('_transcribe_seek')
    def seek(self, args):
        """Seek forward or backward

        Arguments:
        seek_target -- nonzero integer (nb of seconds)
        """
        # Wait for media file to be properly loaded
        self._player.wait_for_property('time-pos')

        if not args:
            error(self._nvim, 'takes at least one argument')
            return

        seek_target = args[0]

        try:
            seek_target = int(seek_target)
        except ValueError:
            error(self._nvim, 'argument should be an integer')
            return

        if seek_target == 0:
            error(self._nvim, 'argument should be a nonzero integer')
            return

        self._player.seek(seek_target)
        self._last_seek = seek_target

    @neovim.function('_transcribe_get_timepos', sync=True)
    def get_timepos(self, args):
        """Get formatted time position in current file

        Arguments:
        format -- format string with {H}, {M}, {S}
        """

        # Wait for media file to be properly loaded
        self._player.wait_for_property('time-pos')

        fmt = args[0] if len(args) == 1 else '[{H}:{M}:{S}] '
        return fmtseconds(self._player.time_pos, fmt)

    @neovim.function('_transcribe_set_timepos')
    def set_timepos(self, args):
        """Set time position in current media file"""

        # Wait for media file to be properly loaded
        self._player.wait_for_property('time-pos')

        if not args:
            error(self._nvim, 'takes at least one argument')
            return

        time = args[0]
        fmt = args[1] if len(args) == 2 else '%H:%M:%S'
        msg(self._nvim, fmt)

        try:
            seconds = time_to_seconds(time, fmt)
        except ValueError:
            error(self._nvim, 'argument should be formatted as %H:%M:%S')
            return

        self._player.time_pos = seconds

    @neovim.function('_transcribe_progress')
    def msg_progress(self, args):
        """Display message with position in current file"""

        # Wait for media file to be properly loaded
        self._player.wait_for_property('time-pos')

        time_pos = fmtseconds(self._player.time_pos)
        perc_pos = round(self._player.percent_pos)

        msg_time_pos = 'progress: {} ({}%)'.format(time_pos, perc_pos)
        msg(self._nvim, msg_time_pos)

    @neovim.function('_transcribe_check_new_line')
    def check_new_line(self, args):
        """Check if the cursor has moved to a new line"""
        cur_line = self._nvim.funcs.line('.')

        if cur_line != self._linenb:
            self.go_to_current_line_timecode()
            self._linenb = cur_line

    @neovim.function('_transcribe_clear_hl')
    def clear_highlight(self, args=None):
        """Clear all highlights"""
        self._nvim.current.buffer.clear_highlight(-1)

    @neovim.function('_transcribe_timepos_curline')
    def go_to_current_line_timecode(self, args=None):
        """Go to first timecode on current buffer line"""

        # Wait for media file to be properly loaded
        self._player.wait_for_property('time-pos')

        cur_line = self._nvim.current.line
        codes = get_timecodes(cur_line)

        if codes:
            self.set_timepos([codes[0]['timecode'], '[%H:%M:%S]'])

            #  If sync mode is on, highlight synced time code
            augroup = self._nvim.funcs.exists('#TranscribeSync#CursorMoved')

            if not augroup:
                return

            self.clear_highlight()
            cur_line_nb = self._nvim.funcs.line('.')
            self._nvim.current.buffer.add_highlight('Statement',
                                                    cur_line_nb-1,
                                                    codes[0]['start_index'],
                                                    codes[0]['end_index'])
