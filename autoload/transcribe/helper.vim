function! transcribe#helper#load() abort
  command! -nargs=1 -range TranscribeAudio
        \ call transcribe#helper#control(<q-args>, 'audio')
endfunction

function! transcribe#helper#control(media, mode) abort
  call _transcribe_load(a:media, a:mode)

  command! -nargs=0 -range TranscribePause
        \ call _transcribe_pause()

  nnoremap <buffer> <plug>(transcribe-toggle-pause) :call _transcribe_pause()<cr>
endfunction
