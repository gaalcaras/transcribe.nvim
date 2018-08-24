function! transcribe#init#general()
  call s:init_options()
  call transcribe#helper#load_media()
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
