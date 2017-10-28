install:
	type mpv >/dev/null 2>&1 || { echo >&2 "test"; exit 1; }
	pip install neovim python-mpv --quiet
	nvim +UpdateRemotePlugins +qall

test:
	python -m unittest -q test.util

git-hooks:
	ln -s ../../pre-commit.sh .git/hooks/pre-commit

.PHONY: test install
