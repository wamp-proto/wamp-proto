# input .fbs files for schema
FILES=wamp.fbs example.fbs reflection.fbs

# flatc compiler to use
#FLATC=${HOME}/scm/xbr/flatbuffers/flatc
FLATC=flatc


default:
	@echo "targets: clean version build"

clean:
	-rm -rf ./_build

version:
	$(FLATC) --version

build: schema cpp csharp go java js php python ts
	cloc ./_build

check_py_modified:
	flake8 void.py
	pycodestyle void.py
	pylint void.py

test: schema
	PYTHONPATH=./_build/python python test.py


# generate schema type library (.bfbs binary)
schema:
	$(FLATC) -o ./_build/schema/ --binary --schema $(FILES)


# generate schema language bindings
cpp:
	$(FLATC) -o ./_build/cpp/ --cpp $(FILES)

csharp:
	$(FLATC) -o ./_build/csharp/ --csharp $(FILES)

go:
	$(FLATC) -o ./_build/go/ --go $(FILES)

java:
	$(FLATC) -o ./_build/java/ --java $(FILES)

js:
	$(FLATC) -o ./_build/js/ --js $(FILES)

php:
	$(FLATC) -o ./_build/php/ --php $(FILES)

python:
	$(FLATC) -o ./_build/python/ --python $(FILES)

ts:
	$(FLATC) -o ./_build/ts/ --ts $(FILES)
