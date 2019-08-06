# `Sentential`
To understand a word's meaning you need more than a definition. Seeing the word in a sentence can provide more context and relevance. This script searchs some well-known grammer helper websites for sentences containing your desired word and shows prints them in standard output.  


# Build
```sh
~ $ git clone --depth https://git/address/of/sentential.git && cd sentential
# ...
~/sentenial $ [sudo] make install
```
Note that you should have python3, pyton3's requests library, python3's lxml library installed.

# Usage
```sh
~ $ sentencial -h
Usage: sentential [OPTION] WORD
Fetchs some sentence examples which include WORD in them.

OPTION:
  --no-color    Does not show colorized text.
  -h, --help    Shows this help text
```
