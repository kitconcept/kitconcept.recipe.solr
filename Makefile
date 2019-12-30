# convenience makefile to boostrap & run buildout

version = 3.7

all: .installed.cfg
	bin/test

.installed.cfg: bin/buildout *.cfg
	bin/buildout

bin/buildout: bin/pip
	bin/pip install --upgrade -r requirements.txt
	@touch -c $@

bin/python bin/pip:
	virtualenv --clear --python=python$(version) .

clean:
	git clean -Xdf

.PHONY: all clean
