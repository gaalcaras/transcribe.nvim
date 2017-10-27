function! transcribe#helper#load() abort
  command! -nargs=1 -range TranscribeAudio
        \ call transcribe#helper#control(<q-args>, 'audio')
endfunction

function! transcribe#helper#control(media, mode) abort
  call _transcribe_load(a:media, a:mode)

  command! -nargs=0 -range TranscribePause
        \ call _transcribe_pause()
  command! -nargs=1 -range TranscribeSpeedSet
        \ call _transcribe_speed(<q-args>, 'set')
  command! -nargs=0 -range TranscribeSpeedInc
        \ call _transcribe_speed(0.1, 'inc')
  command! -nargs=0 -range TranscribeSpeedDec
        \ call _transcribe_speed(0.1, 'dec')

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
endfunction
