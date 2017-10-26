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
