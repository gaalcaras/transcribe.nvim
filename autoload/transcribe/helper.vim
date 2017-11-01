function! transcribe#helper#load_media() abort
  command! -nargs=1 -complete=file TranscribeAudio
        \ call s:load_media_control(<q-args>, 'audio')
endfunction

function! s:load_media_control(media, mode) abort
  call _transcribe_load(a:media, a:mode)
  call s:load_timepos_control()

  command! -nargs=0 TranscribePause
        \ call _transcribe_pause()
  command! -nargs=1 TranscribeSpeedSet
        \ call _transcribe_speed(<q-args>, 'set')
  command! -nargs=0 TranscribeSpeedInc
        \ call _transcribe_speed(g:transcribe_speed_inc)
  command! -nargs=0 TranscribeSpeedDec
        \ call _transcribe_speed(-g:transcribe_speed_inc)
  command! -nargs=1 TranscribeSeek
        \ call _transcribe_seek(<q-args>)
  command! -nargs=0 TranscribeSeekForward
        \ call _transcribe_seek(g:transcribe_seek_inc)
  command! -nargs=0 TranscribeSeekBackward
        \ call _transcribe_seek(-g:transcribe_seek_inc)

  nnoremap <buffer> <plug>(transcribe-toggle-pause)
        \ :TranscribePause<cr>
  inoremap <buffer> <plug>(transcribe-toggle-pause)
        \ <C-o>:TranscribePause<cr>
  nnoremap <buffer> <plug>(transcribe-speed-inc)
        \ :TranscribeSpeedInc<cr>
  inoremap <buffer> <plug>(transcribe-speed-inc)
        \ <C-o>:TranscribeSpeedInc<cr>
  nnoremap <buffer> <plug>(transcribe-speed-dec)
        \ :TranscribeSpeedDec<cr>
  inoremap <buffer> <plug>(transcribe-speed-dec)
        \ <C-o>:TranscribeSpeedDec<cr>
  nnoremap <buffer> <plug>(transcribe-seek-forward)
        \ :TranscribeSeekForward<cr>
  inoremap <buffer> <plug>(transcribe-seek-forward)
        \ <C-o>:TranscribeSeekForward<cr>
  nnoremap <buffer> <plug>(transcribe-seek-backward)
        \ :TranscribeSeekBackward<cr>
  inoremap <buffer> <plug>(transcribe-seek-backward)
        \ <C-o>:TranscribeSeekBackward<cr>
endfunction

function! s:load_timepos_control() abort
  command! -nargs=0 TranscribeProgress
        \ call _transcribe_progress()
  command! -nargs=1 TranscribeGoto
        \ call _transcribe_set_timepos(<q-args>)
  command! -nargs=0 TranscribeToggleSyncMode
        \ call s:toggle_sync_mode()

  nnoremap <buffer> <plug>(transcribe-progress)
        \ :TranscribeProgress<cr>
  inoremap <buffer> <plug>(transcribe-timepos-get)
        \ <C-R>=_transcribe_get_timepos()<C-M>
  nnoremap <buffer> <plug>(transcribe-timepos-curword)
        \ :call transcribe#util#get_current_timepos()<cr>
  nnoremap <buffer> <plug>(transcribe-timepos-curline)
        \ :call _transcribe_timepos_curline()<cr>
  inoremap <buffer> <plug>(transcribe-timepos-curline)
        \ <C-o>:call _transcribe_timepos_curline()<cr>
  nnoremap <buffer> <plug>(transcribe-sync-mode)
        \ :TranscribeToggleSyncMode<cr>
endfunction

function! s:toggle_sync_mode() abort
  if !exists('#TranscribeSync#CursorMoved')
    call _transcribe_timepos_curline()
    augroup TranscribeSync
      autocmd!
      autocmd CursorMoved * call _transcribe_check_new_line()
      autocmd InsertLeave * call _transcribe_timepos_curline()
    augroup END
  else
    call _transcribe_clear_hl()
    augroup TranscribeSync
      autocmd!
    augroup END
  endif
endfunction
