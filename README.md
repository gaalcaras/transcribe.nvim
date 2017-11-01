# transcribe.nvim

Transcribe is a [NeoVim](https://neovim.io/) plugin aimed at helping humans to transcribe recondings to text.

**Warning** : this project is still in a very early stage of development. It's not feature complete yet and you can expect breaking changes.

## Table of contents
<!-- vim-markdown-toc GFM -->

* [Features](#features)
* [Installation](#installation)
* [Quick start](#quick-start)
  * [Playback control](#playback-control)
  * [Progress and time codes](#progress-and-time-codes)
  * [Mappings](#mappings)
* [Why?](#why)

<!-- vim-markdown-toc -->
## Features

+ **Control media playback directly from NeoVim** rather than juggling with another software in the background and using media keys
  * Load media (local file or remote URL), play and pause
  * Set playback speed
  * Seek forward or backward
+ **Time code management**:
  * Insert current time position in the buffer
  * Directly go to time code under the cursor / on the current line
+ **Sync mode**:
  * Always keep the playback in sync with your position in the file, using
    time codes.

## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug):

```vim
Plug 'gaalcaras/transcribe.nvim', { 'do': 'make install' }
```

Transcribe relies on [mpv](https://mpv.io/) and [python-mpv](https://github.com/jaseg/python-mpv) for media playback. Run `make install` to make sure they are both installed, or install them manually. Don't forget to run `:UpdateRemotePlugins` and restart NeoVim to properly install or update the plugin.

## Quick start

This is a quick introduction to the plugin. Please read the [documentation](doc/transcribe.txt) for an exhaustive overview of the plugin.

First things first: load a local file or an URL.

```
:TranscribeAudio https://www.youtube.com/watch?v=o8NPllzkFhE
```

Playback should start automatically. Transcribe will then load commands and mappings.

### Playback control

+ Pause or resume playback using the command `:TranscribePause`
+ Increase/decrease playback speed by 0.1 increments with `:TranscribeSpeedInc`/`:TranscribeSpeedDec` or directly set it with `:TranscribeSpeedSet 0.8`
+ Seek forward/backward by 15 seconds increments with `:TranscribeSeekForward`/`:TranscribeSeekBackward` or directly set it with : `:TranscribeSeek -34`

### Progress and time codes

+ See where you are in media playback with `:TranscribeProgress`
+ Jump to time code with `:TranscribeGoto 00:34:23`
+ Toggle sync mode on/off with `:TranscribeSyncMode`

### Mappings

| Mapping           | Action                                | Mode   | Plug                                 |
| --                | --                                    | --     | --                                   |
| `<leader><space>` | Pause/Resume                          | Normal | `<plug>(transcribe-toggle-pause)`    |
| `<C-space>`       | Pause/Resume                          | Insert | `<plug>(transcribe-toggle-pause)`    |
| `<leader>k`       | Increase speed by 0.1                 | Normal | `<plug>(transcribe-speed-inc)`       |
| `<C-k>`           | Increase speed by 0.1                 | Insert | `<plug>(transcribe-speed-inc)`       |
| `<leader>j`       | Decrease speed by 0.1                 | Normal | `<plug>(transcribe-speed-dec)`       |
| `<C-j>`           | Decrease speed by 0.1                 | Insert | `<plug>(transcribe-speed-dec)`       |
| `<leader>l`       | Seek forward by 15s                   | Normal | `<plug>(transcribe-seek-forward)`    |
| `<C-l>`           | Seek forward by 15s                   | Insert | `<plug>(transcribe-seek-forward)`    |
| `<leader>h`       | Seek backward by 15s                  | Normal | `<plug>(transcribe-seek-backward)`   |
| `<C-h>`           | Seek backward by 15s                  | Insert | `<plug>(transcribe-seek-backward)`   |
| `<leader>p`       | See playback progress                 | Normal | `<plug>(transcribe-progress)`        |
| `<C-t>`           | Insert current time position          | Insert | `<plug>(transcribe-timepos-get)`     |
| `<leader>gw`      | Go to time code under cursor          | Normal | `<plug>(transcribe-timepos-curword)` |
| `<leader>gl`      | Go to first time code on current line | Normal | `<plug>(transcribe-timepos-curline)` |
| `<C-l>`           | Go to first time code on current line | Insert | `<plug>(transcribe-timepos-curline)` |
| `<leader>ms`      | Toggle sync mode on/off               | Normal | `<plug>(transcribe-sync-mode)`       |

## Why?

As far as I know, no plugin implements transcription features properly in vim or NeoVim, probably because the intersection between vim users and transcription work is very thin.

While I have [found](https://github.com/htdebeer/scripts/blob/master/transcribe.vim) [some](https://github.com/AndrewRadev/subtitles.vim) [projects](http://www.mentadreams.com/2012/07/how-to-transcribe-using-vim/) with the same goal as Transcribe, they all relied on mpv's slave mode.
Even though slave mode is hackable and fun, I found it unreliable when used repeatedly.
NeoVim [remote plugin](https://neovim.io/doc/user/remote_plugin.html) allows Transcribe to communicate with mpv asynchronously through the API.
