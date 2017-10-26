# transcribe.nvim

Transcribe is a [NeoVim](https://neovim.io/) plugin aimed at helping humans to transcribe recondings to text.

**Warning** : this project is still in a very early stage of development. It's not feature complete yet and you can expect breaking changes.

## Features

+ **Control media playback (load, play and pause) directly from NeoVim** rather than juggling with another software in the background and using media keys

## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug):

```vim
Plug 'gaalcaras/transcribe.nvim', { 'do': './install' }
```

Transcribe relies on [mpv](https://mpv.io/) and [python-mpv](https://github.com/jaseg/python-mpv) for media playback. Run `./install` to make sure they are both installed, or install them manually. Don't forget to run `:UpdateRemotePlugins` and restart NeoVim to properly install or update the plugin.

## Usage

Load local file or URL:

```vim
:TranscribeAudio https://www.youtube.com/watch?v=o8NPllzkFhE
```

Playback should start playing automatically.

You can pause/resume playback with `<leader><space>` or using the command

```vim
:TranscribePause
```

## Why?

As far as I know, no plugin implements transcription features properly in vim or NeoVim, probably because the intersection between vim users and transcription work is very thin.

While I have [found](https://github.com/htdebeer/scripts/blob/master/transcribe.vim) [some](https://github.com/AndrewRadev/subtitles.vim) [projects](http://www.mentadreams.com/2012/07/how-to-transcribe-using-vim/) with the same goal as Transcribe, they all relied on mpv's slave mode.
Even though slave mode is hackable and fun, I found it unreliable when used repeatedly.
NeoVim [remote plugin](https://neovim.io/doc/user/remote_plugin.html) allows Transcribe to communicate with mpv asynchronously through the API.
