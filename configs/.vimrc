"General Settings
set autochdir
set backspace=indent,eol,start
set backup
set backupdir=~/.vim/backups
set noerrorbells
set whichwrap=b,s,<,>,[,]
set wildmenu
set wildignore=*.pyc,*.o,*.obj,*.exe,*.dll,*.jpg,*.png
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
