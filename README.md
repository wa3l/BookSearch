## Index-based Search Engine
**Author: wael Al-Sallami**  
**Date: Feb 11, 2013**

### Usage
1. To run the program and get an interactive interface, type:
> ./main

2. To search for something, simply type your query into the command-line:
> quixo* "mark twain"

3. To get help, type `help` or `?`

4. To terminate the program, type `exit` or hit `Ctrl+D`

### General Notes
The first time you run the program, it'll attempt to generate the positional and the K-gram indices. The program will prompt you to wait while it writes them. This usually takes about ~12 seconds and builds positional and K-gram indices that are ~45MB and ~7MB in size respectively. The program will also display an accurate interval upon the actions it takes, this includes building/saving indices, loading them, and all search queries.

After the indices are written to disk, you can type your query and get results back. This happens instantly and takes virtually no time (searching for `quixo* "mark twain"` on my machine takes 0.000559 sec).

On subsequent runs of the program, indices are going to be read from disk instead of being built each time. The total ~52MB takes about 3 seconds to be loaded into memory.

User input is cleaned up from special characters, lower-cased, and finally parsed for all three types of queries. Any combination of query types is accepted.

On the optimization side, a lot of thought went into identifying the bottlenecks in the program workflow and trying to rectify some of them. I timed various parts of the code and made sure to shave off a few seconds whenever I can. For instance, I experimented with Pickle, cPicke, Json, and Marshal for dumps and loads, and ended up using Marshal. Additionally, I noticed that list.pop(x) and dict.get(x) are slower than the `in` (best case `O(1)`) and `[]` operators and avoided using them when possible. 

In the end, I was able to cut down the program execution from ~4 minutes to ~12 seconds (first run when writing indices) and 3 seconds per subsequent sessions (reading indices).


- Wael Al-Sallami