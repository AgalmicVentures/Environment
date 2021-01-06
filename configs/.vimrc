
" Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
"
" Permission is hereby granted, free of charge, to any person obtaining a copy
" of this software and associated documentation files (the "Software"), to deal
" in the Software without restriction, including without limitation the rights
" to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
" copies of the Software, and to permit persons to whom the Software is
" furnished to do so, subject to the following conditions:
"
" The above copyright notice and this permission notice shall be included in
" all copies or substantial portions of the Software.
"
" THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
" IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
" FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
" AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
" LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
" OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
" SOFTWARE.

"General Settings
set autochdir
set backspace=indent,eol,start
set backup
set backupdir=~/.vim/backups
set noerrorbells
set nomodeline "Horrible security flaws lie here
set whichwrap=b,s,<,>,[,]
set wildmenu
set wildignore=*.pyc,*.o,*.obj,*.so,*.dylib,*.exe,*.dll,*.jpg,*.png,*.gif
set wildmode=list:longest

"UI Settings
set cmdheight=2
set incsearch
set lazyredraw
set ruler
set scrolloff=12
set showcmd
set showmatch
"set nowrap

"Smart Indenting
set noexpandtab
"set autoindent
"set smartindent

"Folding
set foldenable
set foldmethod=indent
set foldlevel=100 "Don't autofold anything

"Abbreviations
ab header* //********** **********

"Auto-commands
if has("autocmd")
	"Automatically source .vimrc when it is edited
	au BufWritePost ~/.vimrc :source ~/.vimrc
endif

"Use TAB to complete when typing words, else inserts TABs as usual.
"Uses dictionary and source files to find matching words to complete.

"See help completion for source,
"Note: usual completion is on <C-n> but more trouble to press all the time.
"Use the Linux dictionary when spelling is in doubt.
function! Tab_Or_Complete()
	if col('.')>1 && strpart( getline('.'), col('.')-2, 3 ) =~ '^\w'
		return "\<C-N>"
	else
		return "\<Tab>"
	endif
endfunction

:inoremap <Tab> <C-R>=Tab_Or_Complete()<CR>
:set dictionary="/usr/dict/words"

" Move text and re-highlight
vnoremap > ><CR>gv
vnoremap < <<CR>gv
