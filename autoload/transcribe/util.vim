function! transcribe#util#print_msg(string) abort
  echomsg '[transcribe] ' . a:string
endfunction

function! transcribe#util#print_error(string) abort
  echohl Error | echomsg '[transcribe] ' . a:string | echohl None
endfunction
