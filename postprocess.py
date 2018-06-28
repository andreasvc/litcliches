from __future__ import print_function, division
import warnings
from collections import OrderedDict, defaultdict
import io
import os
import re2
import matplotlib
if __name__ == '__main__':
	matplotlib.use('AGG')
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas
import seaborn as sns
from ansi2html import Ansi2HTMLConverter
warnings.simplefilter('ignore', UserWarning)
sns.set_style('ticks')
MATCHESBY10K = '@ 10,000 sentences'


def stripansi(text):
	"""Remove all ANSI colors."""
	return re2.sub('\x1b\[\\d\\d?m', '', text)


def getmatch(text):
	"""Get part of string marked with ANSI red."""
	return re2.findall('^.*\x1b\[31;1m(.*)\x1b\[0m.*$', text, flags=re2.DOTALL)


def readmatches(filename, index):
	"""Read matches (output of discodop treesearch) and produce DataFrame.

	Result will only contain filenames in ``index``."""
	matches = set()
	fnames = set()
	linenos = defaultdict(set)
	for line in io.open(filename, encoding='utf8'):
		fname, lineno, match = line.split(':', 2)
		fname = stripansi(fname).split('.')[0]
		fnames.add(fname)
		lineno = int(stripansi(lineno))
		match, = getmatch(match)
		matches.add(match)
		linenos[fname, match].add(lineno)

	data = pandas.DataFrame(index=index, columns=matches)
	data = data.fillna(0).astype(int)
	for (fname, match), x in linenos.items():
		if fname in index:
			data.at[fname, match] = len(x)
	return data


def overview(data, numcliches, numsents):
	"""Return a new DataFrame with summary statistics."""
	newdata = pandas.DataFrame(OrderedDict([
			('texts', data.shape[0]),
			('sentences', numsents),
			('matches', numcliches),
			(MATCHESBY10K,
				numcliches / numsents * 10000),
			('@ 10,000 sentences, freq > 1',
				(data * (data > 1)).sum(axis=1)
				/ numsents * 10000),
			('count of most repeated match', data.max(axis=1)),
			('types', (data > 0).sum(axis=1)),
			])).sort_values(by=MATCHESBY10K, ascending=False)
	newdata['type-token ratio'] = newdata['types'] / newdata['matches']
	newdata.index = [a.split('.')[0] for a in newdata.index]
	return newdata


def tohtml(filename):
	"""Produce HTML file with highlighted matches."""
	conv = Ansi2HTMLConverter(dark_bg=False)
	with io.open(filename, 'r', encoding='utf8') as inp:
		ansi = inp.read()
	with open('%s.html' % filename.rsplit('.', 1)[0],
			'w', encoding='utf8') as out:
		out.write(conv.convert(ansi
				).replace('#AAAAAA', '#FFFFFF', 1).replace('.tok', ''))


def main():
	"""
	Input: matches.txt
	Additional data used: ../numsents.txt ../../Riddle/metadata.csv
	Output:
		tables: results.tsv bymatch.tsv overview.tsv
		graphs: barplot.pdf regressionLiterariness.pdf regressionQuality.pdf
		html: matches.html
	"""
	# Read data
	metadata = pandas.read_csv('../../Riddle/metadata.csv', index_col='Label')
	numsents = pandas.read_table('../numsents.txt', index_col=1, sep=' ',
			skipinitialspace=True, header=None, names=['Sentences', 'Text']
			)['Sentences'].astype(int)
	numsents.index = [a.split('.')[0] for a in numsents.index]
	numsents2 = numsents.ix[['cgn_syn_nl_train', 'lassytrain']]
	numsents = numsents.ix[metadata.index]
	data = readmatches('matches.txt', numsents.index)
	numcliches = data.sum(axis=1)
	# bookfilter = numsents.ix[metadata.index] > 1000
	bookfilter = metadata.ix[((metadata['# literary ratings'] >= 50)
			& (numsents.ix[metadata.index] > 1000))].index
	print(len(bookfilter), len(data.index))

	# Produce tables
	newdata = overview(data.ix[bookfilter], numcliches, numsents)
	newdata.to_csv('results.tsv', sep='\t', encoding='utf8')
	data.sum().sort_values(ascending=False).to_csv('bymatch.tsv', sep='\t',
			encoding='utf8')
	table = pandas.DataFrame({'Novels': newdata.ix[bookfilter].mean()})
	# macro average
	table.ix[MATCHESBY10K] = (newdata['matches'].sum()
			/ newdata['sentences'].sum() * 10000)
	table.ix['@ 10,000 sentences, freq > 1'] = (
				(data * (data > 1)).sum().sum()
				/ newdata['sentences'].sum() * 10000)
	table.ix['count of most repeated match'] = newdata[
			'count of most repeated match'].max()

	# breakdown by genres
	for genre in metadata.Category.unique():
		books = metadata.ix[bookfilter][(metadata.Category == genre)].index
		table['Novels - ' + genre] = newdata.ix[books].mean()
		table.at['texts', 'Novels - ' + genre] = len(books)
		# macro average
		table.at[MATCHESBY10K, 'Novels - ' + genre] = (
				newdata.ix[books]['matches'].sum()
				/ newdata.ix[books]['sentences'].sum() * 10000)
		table.at['@ 10,000 sentences, freq > 1', 'Novels - ' + genre] = (
				(data.ix[books] * (data.ix[books] > 1)).sum().sum() /
				newdata.ix[books]['sentences'].sum() * 10000)
		table.at['count of most repeated match', 'Novels - ' + genre] = (
				newdata.ix[books]['count of most repeated match'].max())

	# reference corpora
	tmp = readmatches('referencematches.txt',
			['cgn_syn_nl_train', 'lassytrain'])
	ref = overview(tmp, tmp.sum(axis=1), numsents2)
	table['Lassy Small'] = ref.ix['lassytrain']
	table['CGN'] = ref.ix['cgn_syn_nl_train']
	table.at['texts', 'Lassy Small'] = table.at['texts', 'CGN'] = 1
	print(table.T.to_string(float_format=lambda x: '%g' % round(x, 2)))
	print(table.T.to_latex(float_format=lambda x: '%g' % round(x, 2)))
	table.T.to_csv('overview.tsv', sep='\t', encoding='utf8')

	# HTML version of matches
	for filename in ('matches.txt', 'referencematches.txt'):
		tohtml(filename)

	# Graphs
	newdata = pandas.concat([newdata, metadata], axis=1)
	# discard short novels for plots and correlations
	newdata = newdata.ix[bookfilter].sort_values(
			by=MATCHESBY10K, ascending=False)

	colorcat = 'Quality rating'
	norm = matplotlib.colors.Normalize(vmin=1, vmax=7)
	mappable = cm.ScalarMappable(norm, 'gist_heat')
	mappable.set_array(
				metadata.ix[newdata.index[::-1]][colorcat])
	colors = mappable.to_rgba(
				metadata.ix[newdata.index[::-1]][colorcat])
	ax = newdata[MATCHESBY10K].ix[::-1].plot(
			kind='barh', figsize=(4, 20), grid=False, color=colors)
	ax.set_xlabel(MATCHESBY10K)
	plt.tick_params(axis='both', which='major', labelsize=3)
	plt.tick_params(axis='both', which='minor', labelsize=3)
	cbar = plt.colorbar(mappable, ticks=range(1, 8))
	cbar.solids.set_edgecolor("face")
	cbar.set_label(colorcat)
	ax.xaxis.label.set_size(3)
	ax.figure.tight_layout()
	ax.figure.savefig('barplot.pdf')

	sns.jointplot(
			x='Literary rating', y=MATCHESBY10K, data=newdata,
			kind='reg', xlim=(1, 7),
			ylim=(-5, newdata[MATCHESBY10K].max() + 5))
	plt.savefig('regression%s.pdf' % 'Literariness')
	plt.savefig('regression%s.png' % 'Literariness', dpi=300)
	sns.jointplot(
			x='Quality rating', y=MATCHESBY10K, data=newdata,
			kind='reg', xlim=(3, 7),
			ylim=(-5, newdata[MATCHESBY10K].max() + 5))
	plt.savefig('regression%s.pdf' % 'Quality')
	plt.savefig('regression%s.png' % 'Quality', dpi=300)

if __name__ == '__main__':
	for path in ('cliches', ):
		os.chdir(path)
		print(path)
		main()
		os.chdir('..')
