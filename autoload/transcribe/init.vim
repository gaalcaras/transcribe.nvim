function! transcribe#init#general()
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

  call s:map('n', '<leader><space>', '<plug>(transcribe-toggle-pause)')
  call s:map('i', '<C-space>', '<plug>(transcribe-toggle-pause)')

  call s:map('n', '<leader>k', '<plug>(transcribe-speed-inc)')
  call s:map('i', '<C-k>', '<plug>(transcribe-speed-inc)')
  call s:map('n', '<leader>j', '<plug>(transcribe-speed-dec)')
  call s:map('i', '<C-j>', '<plug>(transcribe-speed-dec)')

  call s:map('n', '<leader>l', '<plug>(transcribe-seek-forward)')
  call s:map('i', '<C-l>', '<plug>(transcribe-seek-forward)')
  call s:map('n', '<leader>h', '<plug>(transcribe-seek-backward)')
  call s:map('i', '<C-h>', '<plug>(transcribe-seek-backward)')

  call s:map('n', '<leader>p', '<plug>(transcribe-progress)')
  call s:map('i', '<C-t>', '<plug>(transcribe-timepos-get)')
  call s:map('n', '<leader>g', '<plug>(transcribe-timepos-set)')
endfunction
