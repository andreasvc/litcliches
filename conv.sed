# issues:
# - what to do with multiple sentences (mini dialogues);
# - how many words to allow in square brackets?
#   (Zie je nou wel,) ik kán wel [pannenkoeken bakken]!
# - fix scope of "/" when it should span multiple words.
#   Als je ’t eenmaal hebt/er eenmaal een hebt, wil/kun je nooit meer zonder!
#   should be:
#   Als je ('t eenmaal hebt/er eenmaal een hebt), [...]
#   fixed with manual editing.
# - can brackets be nested? yes:
#   Als je toch aan het X'en bent/X aan het Y'en bent(, X dan meteen even (Y) voor mij).
#   not translated correctly
# - "etc." and "..." as placeholder: A/B/...

# unicode whitespace
s/\xc2\x91\|\xc2\x92\|\xc2\xa0\|\xe2\x80\x8e/ /;

# remove trailing material in parentheses/brackets
s/([^()]*)\s*$//g;
s/\[[^][]*\]\s*$//g;

# remove anything in angular brackets/hashtag nonsense
s/<[^<>]*>//g;
s/#\S+//g;

# normalize punctuation
s/…/.../g;
s/’/'/g;
s/­/-/g;

# escape ? and .
s/?/ \\?/g;
s/!/ !/g;
s/\([^.]\)\./\1 ./g;
s/\./\\./g;
s/:/ :/g;

# single letter variables can be any single word
s/\b\(\(ge\|door\)-\)\?[xyzXYZABC]\(-\|'\(en\|er\|t\|d\)\)\? /\2\\w+\4 /g;

# remaining parenthesized material becomes optional
s/( *\([^()]*\S\) *) */(?:\1 )?/g;

# alternative pronouns
s/\b'm\b/&\/hem/g;
s/\bd'r\b/&\/er\/haar/g;
s/\bhij\b/&\/zij\/ze/g;
s/\bm'n\b/&\/mijn/g;
s/\bnu\b/&\/nou/g;
s/\bvrouw\b/&\/man\/vent/g;
s/\bvader\b/&\/moeder\/ouders/g;
s/-ie\b/(?:&| ie| hij)/g;

# replace / where between [...]
:a; s/\(\[[^][]*\)\//\1|/; ta

# alternatives: [A/B] => (?:A|B)
s/\[\([^][|]\+ *\( *| *[^][|]\+\)\+\)\]/(?:\1)/g;

# remaining alternatives: A/B => (?:A|B)
s/\( *\)\([-'\A-Za-z]\+\( *\/ *[-'A-Za-z]\+\)\+\)\( *\)/\1(?:\2)\4/g;
s/ *\/ */|/g;

# tokenize punctuation
s/\(\S\)\([,;"!]\)\(\S\)/\1 \2 \3/g;
s/\( [,;"]\)\(\S\)/\1 \2/g;
s/\(\S\)\([,;"!] \)/\1 \2/g;

# cliche with initial caps should match from start of (quoted) sentence
s/^\(\((?:\)*\[\?[A-Z]\)/(?:^|' )\1/g

# make ellipsis optional
s/\.\.\.\( *\)/(?:\.\.\.\1)?/g;

# material in square brackets can be 1-3 words
s/\[[^][]*\] */(?:[-\\w]+ ){1,3}/g;

# make leading interjections optional
s/\(^\|)\)\(ach ja\|ach joh\|ach kom\|ach\|afijn\|aha\?\|bah\|deksels\|donders\|en toch\|enfin\|excuses\|gadverdamme\|god bewaar me\|godallemachtig\|goddank\|goddome\|goeiemorgen\|gossie\|gossiemijne\|grutjes\|gunst\|gut\|ha\|hallo\|he\|hee\|hehe\|helaas\|hemel\|hemeltjelief\|heremijntijd\|hoera\|hup\|inderdaad\|ja ja\|ja maar\|ja\|jaja\|jakkes\|jandorie\|jasses\|jawel\|jee\|jeetje\|jeminee\|jep\|jezus-christus\|jezus\|joepie\|joh\|jup\|kijk\|komaan\|lieve hemel\|maar toch\|maar\|mijn hemel\|nee maar\|nee\|nja\|nou en of\|nou hup\|nou nou\|nou\|nu\|oh\? ja\|oh\? nee\|oh\?\|och\|oef\|oh god\|oh oh\|oh\?\|ok\|oké\|okee\|okido\|okidoki\|poeh\|potdorie\|sapperloot\|shit\|sjonge\|snotverdomme\|sorry\|st\|tja\|toe maar\|vedomme\|verdorie\|verrek\|wel\|welja\|zeg\|zo\) [,!?] /\1(?:\2 [,!?] )?/gI
# st ?

# make trailing interjections optional
s/, \([A-Z]\w+\|ach\|blijkbaar\|excuses\|goddank\|he\|hee\|hoera\|hoor\|ja\|joh\|kennelijk\|maar toch\|nee\|nietwaar\|sorry\|toch\|verdomme\|verdorie\|zeg\) *\([.?!'"]\)/(?:, \1)? \2/gI

# allow different kinds of sentence ending punctuation
s/ \(\\?\|\\\.\|!\)\s*$/ [.?!'"]/g;

# allow unaccented form of accents
s/\([äáàâ]\)/[\1a]/g;
s/\([éèêë]\)/[\1e]/g;
s/\([íîï]\)/[\1i]/g;
s/\([ôö]\)/[\1o]/g;
s/\([üûù]\)/[\1u]/g;

# trim white space
s/ \+/ /g;

# trim spurious alternations
s/^|//g;
s/|\s*$//g;

# remove empty lines
/^\s*$/d;
