if exists("g:loaded_vimscript_py")
    finish
endif
let g:loaded_vimscript_py = 1

function! LLM(...)
    " TODO: fix this script pathing issue
    let script_path = '/Users/v/.vim/pack/plugins/start/llm/plugin/vimscript_llm.py'
    let args = a:000  " Capture all arguments
    let job = job_start(['python', script_path] + args, {'callback': 'ReplaceCommandLine'})
endfunction

function! ReplaceCommandLine(channel, msg)
    call feedkeys(":" . a:msg, 'n')
endfunction

command! -nargs=* LLM call LLM(<f-args>)
