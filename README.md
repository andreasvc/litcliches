# Cliche expressions in literary and genre novels

Code for the paper "Cliche expressions in literary and genre novels",
to be presented at the Latech-CLfL 2018 workshop.

This repository is intended for documentation purposes, as the relevant data
cannot be made publicly available.

## Data used

- Lassy small, Lassy large; http://www.let.rug.nl/~vannoord/Lassy/
- Corpus Gesproken Nederlands (Spoken Dutch corpus); http://lands.let.ru.nl/cgn/
- The Riddle of Literary Quality corpus of 401 novels; http://literaryquality.huygens.knaw.nl/
- Cliche expressions that formed the basis for the book ISBN: 978-94-004-0511-0; https://www.dathoorjemijnietzeggen.nl/

## Python modules used

install with `pip3 install ...`

- matplotlib
- pandas
- seaborn
- ansi2html
- https://github.com/andreasvc/pyre2
- https://github.com/andreasvc/disco-dop

## Makefile overview

- `cliche_queries.txt`: Original file with cliches is converted to regular expressions (using regular expressions...) with sed script `conv.sed`
- `runqueries`: cliches are counted in novels by running each query on all the novels
- `postprocess`: produces HTML files, plots, and CSV files.

The rest of the analysis is done in the notebook.
