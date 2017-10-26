function! transcribe#init#general()
  call s:init_default_mappings()
  call transcribe#helper#load()
endfunction

function! s:init_default_mappings()
  function! s:map(mode, lhs, rhs, ...)
    if !hasmapto(a:rhs, a:mode)
          \ && ((a:0 > 0) || (maparg(a:lhs, a:mode) ==# ''))
      silent execute a:mode . 'map <silent><buffer>' a:lhs a:rhs
    endif
  endfunction

  call s:map('n', '<leader><space>', '<plug>(transcribe-toggle-pause)')
endfunction
