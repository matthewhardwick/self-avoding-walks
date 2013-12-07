name = report

$(name).pdf : $(name).tex statement.tex overview.tex implementation.tex sample.tex conclusion.tex
	pdflatex $(name) && \
	#bibtex $(name) && \
	pdflatex $(name) && \
	pdflatex $(name)

clean :
	rm -f \
	$(name).aux \
	$(name).bbl \
	$(name).blg \
	$(name).log \
	$(name).out \
	$(name).pdf \
	$(name).toc
