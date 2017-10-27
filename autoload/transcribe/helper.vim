function! transcribe#helper#load_media() abort
  command! -nargs=1 -complete=file TranscribeAudio
        \ call transcribe#helper#control(<q-args>, 'audio')
endfunction

function! transcribe#helper#control(media, mode) abort
  call _transcribe_load(a:media, a:mode)

  command! -nargs=0 TranscribePause
        \ call _transcribe_pause()
  command! -nargs=1 TranscribeSpeedSet
        \ call _transcribe_speed(<q-args>, 'set')
  command! -nargs=0 TranscribeSpeedInc
        \ call _transcribe_speed(0.1, 'inc')
  command! -nargs=0 TranscribeSpeedDec
        \ call _transcribe_speed(0.1, 'dec')
  command! -nargs=1 TranscribeSeek
        \ call _transcribe_seek(<q-args>)
  command! -nargs=0 TranscribeSeekInc
        \ call _transcribe_seek(15)
  command! -nargs=0 TranscribeSeekDec
        \ call _transcribe_seek(-15)

  nnoremap <buffer> <plug>(transcribe-toggle-pause)
        \ :call _transcribe_pause()<cr>
  inoremap <buffer> <plug>(transcribe-toggle-pause)
        \ <Esc>:call _transcribe_pause()<cr>a
  nnoremap <buffer> <plug>(transcribe-inc-speed)
        \ :call _transcribe_speed(0.1, 'inc')<cr>
  inoremap <buffer> <plug>(transcribe-inc-speed)
        \ <Esc>:call _transcribe_speed(0.1, 'inc')<cr>a
  nnoremap <buffer> <plug>(transcribe-dec-speed)
        \ :call _transcribe_speed(0.1, 'dec')<cr>
  inoremap <buffer> <plug>(transcribe-dec-speed)
        \ <Esc>:call _transcribe_speed(0.1, 'dec')<cr>a
  nnoremap <buffer> <plug>(transcribe-inc-seek)
        \ :call _transcribe_seek(15)<cr>
  inoremap <buffer> <plug>(transcribe-inc-seek)
        \ <Esc>:call _transcribe_seek(15)<cr>a
  nnoremap <buffer> <plug>(transcribe-dec-seek)
        \ :call _transcribe_seek(-15)<cr>
  inoremap <buffer> <plug>(transcribe-dec-seek)
        \ <Esc>:call _transcribe_seek(-15)<cr>a
endfunction
