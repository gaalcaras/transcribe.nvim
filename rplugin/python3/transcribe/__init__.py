import neovim
import mpv

from transcribe.util import (error, msg, fmtseconds, time_to_seconds) # noqa


@neovim.plugin
class Transcribe(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self._last_seek = 0

    def _mpv_log(self, loglevel, component, message):
        if (loglevel == 'error') or ('ERROR' in message):
            err_msg = '{}: {}'.format(component, message)
            error(self.nvim, err_msg)

    @neovim.function('_transcribe_load')
    def load_media(self, args):
        """Initialize player and load media file

        Arguments:
        mediafile -- file or URL
        mode      -- audio by default
        """
        if not args:
            error(self.nvim, 'takes at least one argument')
            return

        media = args[0]
        mode = args[1] if len(args) == 2 else 'audio'

        if mode == 'audio':
            self.player = mpv.MPV(ytdl=True, video=False,
                                  log_handler=self._mpv_log)
            self.player.play(media)
        else:
            error(self.nvim, 'Wrong loading mode value')

        @self.player.event_callback('file-loaded')
        def echo_loaded(event):
            msg(self.nvim, 'media loaded')

        @self.player.event_callback('pause')
        def echo_pause(event):
            msg(self.nvim, 'playback paused')

        @self.player.event_callback('unpause')
        def echo_unpause(event):
            msg(self.nvim, 'playback resumed')

        @self.player.event_callback('seek')
        def echo_seek(event):
            seek = self._last_seek
            time_pos = fmtseconds(self.player.time_pos)

            if seek > 0:
                direction = 'forward'
            else:
                direction = 'backward'

            seek_msg = 'seek {} ({:+d}s): {}'.format(direction, seek, time_pos)
            msg(self.nvim, seek_msg)

    @neovim.function('_transcribe_pause')
    def toggle_pause(self, args):
        self.player.cycle('pause')

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
            error(self.nvim, 'argument should be a number')
            return

        if mode == 'set':
            self.player.speed = speed
        else:
            if (self.player.speed + speed) >= 0.1:
                self.player.speed += speed
            else:
                error(self.nvim, 'speed is already at minimum setting')
                return

        info = 'playback speed set to {:1.1f}'.format(self.player.speed)
        msg(self.nvim, info)

    @neovim.function('_transcribe_seek')
    def seek(self, args):
        """Seek forward or backward

        Arguments:
        seek_target -- nonzero integer (nb of seconds)
        """
        # Wait for media file to be properly loaded
        self.player.wait_for_property('time-pos')

        if not args:
            error(self.nvim, 'takes at least one argument')
            return

        seek_target = args[0]

        try:
            seek_target = int(seek_target)
        except ValueError:
            error(self.nvim, 'argument should be an integer')
            return

        if seek_target == 0:
            error(self.nvim, 'argument should be a nonzero integer')
            return

        self.player.seek(seek_target)
        self._last_seek = seek_target

    @neovim.function('_transcribe_get_timepos', sync=True)
    def get_timepos(self, args):
        """Get formatted time position in current file

        Arguments:
        format -- format string with {H}, {M}, {S}
        """

        # Wait for media file to be properly loaded
        self.player.wait_for_property('time-pos')

        fmt = args[0] if len(args) == 1 else '[{H}:{M}:{S}] '
        return fmtseconds(self.player.time_pos, fmt)

    @neovim.function('_transcribe_set_timepos')
    def set_timepos(self, args):
        """Set time position in current media file"""

        # Wait for media file to be properly loaded
        self.player.wait_for_property('time-pos')

        if not args:
            error(self.nvim, 'takes at least one argument')
            return

        time = args[0]
        fmt = args[1] if len(args) == 2 else '%H:%M:%S'
        msg(self.nvim, fmt)

        try:
            seconds = time_to_seconds(time, fmt)
        except ValueError:
            error(self.nvim, 'argument should be formatted as %H:%M:%S')
            return

        self.player.time_pos = seconds

    @neovim.function('_transcribe_progress')
    def msg_progress(self, args):
        """Display message with position in current file"""

        # Wait for media file to be properly loaded
        self.player.wait_for_property('time-pos')

        time_pos = fmtseconds(self.player.time_pos)
        perc_pos = round(self.player.percent_pos)

        msg_time_pos = 'progress: {} ({}%)'.format(time_pos, perc_pos)
        msg(self.nvim, msg_time_pos)
