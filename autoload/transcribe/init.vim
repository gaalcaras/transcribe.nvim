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

  call s:map('n', '<leader>k', '<plug>(transcribe-inc-speed)')
  call s:map('i', '<C-k>', '<plug>(transcribe-inc-speed)')
  call s:map('n', '<leader>j', '<plug>(transcribe-dec-speed)')
  call s:map('i', '<C-j>', '<plug>(transcribe-dec-speed)')
endfunction
