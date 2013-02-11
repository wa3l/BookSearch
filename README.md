## Index-based Search Engine
**Author: wael Al-Sallami**  
**Date: Feb 11, 2013**

### Usage
1. To run the program type:
> ./main

2. To search for something, simply type your query into the command-line:
> quixo* "mark twain"

3. To get help, type `help` or `?`

4. To terminate the program, type `exit` or hit `Ctrl+D`

### General Notes
The first time you run the program, it'll attempt to generate the positional index and the kgram indices. The program will prompt you to wait while it writes the them. This usually takes about ~12 seconds and builds positional and K-gram indices that are ~45MB and ~7MB respectively. The program will also display an accurate interval upon the actions it takes, this includes building/saving indices, loading them, and all search queries.

After the indices are written to disk, you can type your query and get results back. This happens instantly and takes virtually no time (searching for `quixo* "mark twain"` on my machine takes 0.000559 sec).

On subsequent runs of the program, indices are going to be read from disk instead of being generated each time. The total ~52MB takes about 3 seconds to be loaded into memory.

### 