## VimScript-LLM

# What does it do

This implements a vim plugin that allows you to call an LLM from inside vim to give you otherwise hard-to-write vim commands

# Why

Vim has a very powerful internal language, but it's hard to learn or use productively. Vimscript-LLM allows you to use natural language to write vim commands for you. For example, you can call `:LLM replace any amount of text between two commas on one line with exactly one tab` and get a command that otherwise would've taken some time to write.

# Status

It turns out that LLMs are OK but not great at writing Vim commands. I'm getting useful output from ~half my calls and need to improve an internal validation loop to ensure valid outputs.
