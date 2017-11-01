function! transcribe#init#general()
  call s:init_options()
  call s:init_default_mappings()

  call transcribe#helper#load_media()
endfunction

function! s:init_default_mappings()
  function! s:map(mode, lhs, rhs, ...)
    if !hasmapto(a:rhs, a:mode)
          \ && ((a:0 > 0) || (maparg(a:lhs, a:mode) ==# ''))
      silent execute a:mode . 'map <silent><buffer>' a:lhs a:rhs
    endif
  endfunction

  if g:transcribe_localleader
    let l:prefix = '<localleader>'
  else
    let l:prefix = '<leader>'
  endif

  call s:map('n', l:prefix . '<space>', '<plug>(transcribe-toggle-pause)')
  call s:map('i', '<C-space>', '<plug>(transcribe-toggle-pause)')

  call s:map('n', l:prefix . 'k', '<plug>(transcribe-speed-inc)')
  call s:map('i', '<C-k>', '<plug>(transcribe-speed-inc)')
  call s:map('n', l:prefix . 'j', '<plug>(transcribe-speed-dec)')
  call s:map('i', '<C-j>', '<plug>(transcribe-speed-dec)')

  call s:map('n', l:prefix . 'l', '<plug>(transcribe-seek-forward)')
  call s:map('i', '<C-l>', '<plug>(transcribe-seek-forward)')
  call s:map('n', l:prefix . 'h', '<plug>(transcribe-seek-backward)')
  call s:map('i', '<C-h>', '<plug>(transcribe-seek-backward)')

  call s:map('n', l:prefix . 'p', '<plug>(transcribe-progress)')
  call s:map('i', '<C-t>', '<plug>(transcribe-timepos-get)')
  call s:map('n', l:prefix . 'gw', '<plug>(transcribe-timepos-curword)')
  call s:map('n', l:prefix . 'gl', '<plug>(transcribe-timepos-curline)')
  call s:map('i', '<C-l>', '<plug>(transcribe-timepos-curline)')
  call s:map('n', l:prefix . 'ms', '<plug>(transcribe-sync-mode)')
endfunction

function! s:init_options()
  call s:init_option('transcribe_speed_inc', 0.1)
  call s:init_option('transcribe_seek_inc', 15)
  call s:init_option('transcribe_localleader', 0)
endfunction

function! s:init_option(option, default)
  let l:option = 'g:' . a:option
  if !exists(l:option)
    let {l:option} = a:default
  endif
endfunction
