all:
	@echo "Targets:"
	@echo ""
	@echo "  clean"
	@echo "  deploy"
	@echo "  freeze"
	@echo "  test"
	@echo "  test_frozen"
	@echo ""

deploy: clean freeze upload

clean:
	rm -rf website/wampws/build

freeze:
	python website/wampws/__init__.py -f

upload:
	python website/wampws/upload.py --bucket "wamp.ws" --directory "build"

test:
	python website/wampws/__init__.py -d

test_frozen:
	python website/wampws/__init__.py -f -d
