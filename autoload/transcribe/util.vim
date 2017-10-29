function! transcribe#util#print_msg(string) abort
  echomsg '[transcribe] ' . a:string
endfunction

function! transcribe#util#print_error(string) abort
  echohl Error | echomsg '[transcribe] ' . a:string | echohl None
endfunction

function! transcribe#util#get_current_timepos() abort
  let l:current_word = expand('<cWORD>')
  call _transcribe_set_timepos(l:current_word, '[%H:%M:%S]')
endfunction
