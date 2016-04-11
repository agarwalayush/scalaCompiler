all : binary

binary :
	mkdir -p bin
	cp src/codegen bin
	chmod +x bin/codegen

clean :
	rm -rf bin
	rm -rf test/*.o test/*.s
