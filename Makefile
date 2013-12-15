all:
	@echo "Targets:"
	@echo ""
	@echo "   clean               Cleanup"
	@echo "   img                 Generate optimized and compressed images"
	@echo "   freeze              Freeze dynamic Web site into static pages"
	@echo "   test                Test dynamic Web site (Twisted)"
	@echo "   test_frozen         Test frozen Web site (Twisted)"
	@echo "   upload              Upload frozen Web site to S3"
	@echo ""

deploy: clean img freeze upload

clean:
	rm -rf website/wampws/build
	scons -uc

img:
	scons

freeze:
	python website/wampws/__init__.py -f

upload:
	python website/wampws/upload.py --bucket "wamp.ws" --directory "build"

test:
	python website/wampws/__init__.py -d

test_frozen:
	python website/wampws/__init__.py -f -d
