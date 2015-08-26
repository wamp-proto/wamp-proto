all:
	@echo "Targets:"
	@echo ""
	@echo "   img                 Generate optimized and compressed images"
	@echo "   freeze              Freeze dynamic Web site into static pages"
	@echo "   test                Test dynamic Web site (Twisted)"
	@echo "   test_frozen         Test frozen Web site (Twisted)"
	@echo "   upload              Upload frozen Web site to S3"
	@echo "   clean               Cleanup"
	@echo ""

img:
	scons img

freeze:
	python website/wampws/__init__.py -f --widgeturl ''

upload:
	scons upload

test: img
	python website/wampws/__init__.py -d --widgeturl ''

test_frozen: img freeze
	twistd -n web --port=8080 --path=./website/wampws/build

deploy: img freeze upload

clean:
	rm -rf website/wampws/build
	rm -rf website/wampws/static/img/gen
	rm -f ./twistd.log
	rm -f .sconsign.dblite
	scons -uc
