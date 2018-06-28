all: cliche_queries.txt cliche_singlequery.txt

cliche_queries.txt: conv.sed cliches_edited.txt
	sed --file=conv.sed cliches_edited.txt \
		| sort --unique \
		> cliche_queries.txt

cliche_singlequery.txt: cliche_queries.txt
	python -c 'print("|".join(open("cliche_queries.txt").read().splitlines()))' \
		> cliche_singlequery.txt

referencecorpora: lassytrain.tok cgn_syn_nl_train.tok

lassytrain.tok:
	discodop treetransforms \
		--inputfmt=export --outputfmt=tokens \
		~/data/lassytrain.export lassytrain.tok

cgn_syn_nl_train.tok:
	discodop treetransforms \
		--inputfmt=export --outputfmt=tokens \
		~/data/cgn_syn_nl_train.export cgn_syn_nl_train.tok

numsents.txt: referencecorpora
	cd ../Riddle/tokenized_sentno/ && wc -l *.tok | head -n -1 \
		> /tmp/numsents.txt
	cd ../data && wc -l lassytrain.tok cgn_syn_nl_train.tok | head -n -1 \
		>> /tmp/numsents.txt
	mv /tmp/numsents.txt .

runqueries: runcliches

runcliches:
	cd ../Riddle/tokenized/ && time discodop treesearch \
		--sents --ignore-case --line-number \
		--max-count=0 --numproc=30 --engine=regex \
		--file /datastore/avcrane1/cliches/cliche_queries.txt *.tok \
		> /datastore/avcrane1/cliches/cliches/matches.txt
	cd ../data/ && time discodop treesearch --sents --ignore-case --line-number \
		--max-count=0 --numproc=30 --engine=regex \
		--file /datastore/avcrane1/cliches/cliche_queries.txt cgn_syn_nl_train.tok lassytrain.tok \
		> /datastore/avcrane1/cliches/cliches/referencematches.txt

postprocess: postprocess.py
	python3 postprocess.py

