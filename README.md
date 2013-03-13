## BookSearch - A simple positional/kgram based Search Engine.

### Usage
1. To run the program and get an interactive interface, type:
> ./main.py

2. Place the /books directory where main.py is.

3. To search for something, type your query into the command-line:
> quixo* "mark twain"

4. To get help, type `help` or `?`

5. To terminate the program, type `exit` or hit `Ctrl+D`

### General Notes
The first time you run the search engine, it'll attempt to generate the positional and K-gram indices. The engine will prompt you to wait while it writes them. This usually takes about ~12 seconds and builds positional and K-gram indices that are ~45MB and ~7MB in size respectively (given the books dataset). The engine will also display an accurate interval upon the actions it takes, this includes building/saving indices, loading them, and all search queries.

After indices are written to disk, you can type your query and get results back. This happens instantly (searching for `quixo* "mark twain"` on my machine takes 0.000559 sec).

On subsequent runs, indices are going to be read from disk instead of being built each time. The total ~52MB takes about 3 seconds to be loaded into memory using `marshal`.

User input is cleaned up from special characters, lower-cased, and finally parsed for Boolean, Phrase, and Wildcard queries. Any combination of query types is accepted.

Author
------
Wael Al-Sallami | [wa3l.com](http://wa3l.com).
  
License
-----
Public domain: [http://unlicense.org](http://unlicense.org)
