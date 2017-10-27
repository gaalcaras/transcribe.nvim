import neovim
import mpv

from transcribe.util import (error, msg) # noqa

@neovim.plugin
class Transcribe(object):
    def __init__(self, nvim):
        self.nvim = nvim

    def _mpv_log(self, loglevel, component, message):
        if (loglevel == 'error') or ('ERROR' in message):
            err_msg = '{}: {}'.format(component, message)
            error(self.nvim, err_msg)

    @neovim.function('_transcribe_load')
    def load_media(self, args):
        media = args[0]
        mode = args[1]

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

    @neovim.function('_transcribe_pause')
    def toggle_pause(self, args):
        self.player.cycle('pause')

    @neovim.function('_transcribe_speed')
    def set_speed(self, args):
        """Change playback speed

        Arguments:
        speed -- speed or increment
        mode  -- how to change speed (set, increase or decrease)
        """
        speed = args[0]
        mode = args[1]

        try:
            speed = round(float(speed), 1)
        except ValueError:
            error(self.nvim, 'argument should be a positive number')
            return

        if speed < 0:
            error(self.nvim, 'speed should a positive number')
            return

        if mode == 'set':
            self.player.speed = speed
        elif mode == 'inc':
            self.player.speed += speed
        elif mode == 'dec':
            if (self.player.speed - speed) >= 0.1:
                self.player.speed -= speed
            else:
                error(self.nvim, 'speed is already at minimum setting')
                return
        else:
            error(self.nvim, 'speed mode should be either set, inc or dec')

        info = 'playback speed set to {:1.1f}'.format(self.player.speed)
        msg(self.nvim, info)
