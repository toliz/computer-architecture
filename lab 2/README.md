# Lab 2

## 1. SPEC CPU2006 benchmarking

The simulated processor has a **cache line size** of 64 bytes. The cache is organized in a 2 level scheme with L1 cache subdivided in instruction cache and data cache.

<table>
    <thead>
        <tr>
            <th style="text-align:center;">  </th>
            <th style="text-align:center;"> L1 I-cache </th>
            <th style="text-align:center;"> L1 D-cache </th>
            <th style="text-align:center;"> L2 cache </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th> Size </th> 
            <td> 32 KB </td> 
            <td> 64 KB </td> 
            <td> 2 MB </td> 
        </tr>
        <tr>
            <th> Associativity </th> 
            <td> 2 </td> 
            <td> 2 </td> 
            <td> 8 </td>
        </tr>
    </tbody>
</table>

For the above CPU design we run 5 *SPEC CPU 2006* benchmarks and we measure execution time, CPI and cache miss rates. We can see the results in the table below:

<table>
    <thead>
        <tr>
            <th style="text-align:center;">  </th>
            <th style="text-align:center;"> specbzip </th>
            <th style="text-align:center;"> spechmmer </th>
            <th style="text-align:center;"> speclibm </th>
            <th style="text-align:center;"> specmcf </th>
            <th style="text-align:center;"> specsjeng </th>
        </tr>
    </thead>
    <tbody style="text-align:right;">
        <tr>
            <th style="text-align:right"> Execution Time </th> 
            <td> 87.5 ms </td> 
            <td> 58.2 ms </td> 
            <td> 174.7 ms </td> 
            <td> 54.4 ms </td> 
            <td> 513.6 ms </td> 
        </tr>
        <tr>
            <th style="text-align:right;"> CPI </th> 
            <td> 1.75 </td> 
            <td> 1.16 </td> 
            <td> 3.49 </td> 
            <td> 1.09 </td> 
            <td> 10.24 </td>
        </tr>
        <tr>
            <th style="text-align:right;"> I-L1 miss rate </th> 
            <td> 0.0054 % </td> 
            <td> 0.0145 % </td> 
            <td> 0.0097 % </td> 
            <td> 0.0019 % </td> 
            <td> 0.0015 % </td>
        </tr>
        <tr>
            <th style="text-align:right;"> D-L1 miss rate </th> 
            <td> 1.4618 % </td> 
            <td> 0.1669 % </td> 
            <td> 6.0971 % </td> 
            <td> 0.1955 % </td> 
            <td> 12.1831 % </td>
        </tr>
        <tr>
            <th style="text-align:right;"> L2 miss rate </th> 
            <td> 26.6550 % </td> 
            <td> 8.1390 % </td> 
            <td> 99.9967 % </td> 
            <td> 72.6148 % </td> 
            <td> 99.9979 % </td>
        </tr>
    </tbody>
</table>

First of all we notice that execution time has a linear relation (x50) with CPI, which is to be expected if we do the maths:

`100M instr. x CPI / 2B clocks = Exec (secs) => Exec (ms) = 50 * CPI`

So below we see the other 4 values ploted in a single diagram:

<p align="center">
<img src=img/caches.jpg>
</p>

D-cache miss rate is propotional to the CPI while L2 cache miss rate follows the trend. However i-cache is follows a different trend.

Afterwards we re-run the benchmarks with the parameter `--cpu-clock=1GHz` to set the CPU frequency to 1 GHz (default value is 2 GHz).

We check the configuration file and we see that in both cases (cpu clock set to 1 and 2 GHz) the `system.clock_domain.clock` is set to 1000 while `system.cpu_clk_domain.clock` is set 1000 and 500 respectively.

According to [1] the first parameter is the system clock and is used to sychronize the the clocks in the different system modules (CPU, memory, etc.) while the senond parameter is the CPU clock. Usually it's set in a multiple of the system clock. Moreover the CPU clock affects the execution time while the system clock no.

|     |specbzip | spechmmer | speclibm | specmcf | specsjeng|
|-----|---------|-----------|----------|---------|----------|
|1 GHz| 167.4   | 116       | 262.3    | 107.1   | 704      |
|2 GHz| 87.5    | 58.2      | 174.7    | 54.4    | 513.6    |

We notice that in the specbzip, spechmmer and specmcf there is a perfect scaling whilst in the speclibm and specsjeng there isn't. This might be due to the inability of the caches and memory to fetch missed instruction and data in the double rate.

## 2. Design Exploration

Here we are going to explore the system's configuration effect on the CPI (average CPI of the 5 benchmarks). For simplicity reason we focus on the average of the benchmarks although a more detailed report should explore the effect on each benchmark seperately.

In order to conduct this section successfully we wrote 3 python scripts:
- `xplore.py` wraps the gem5 command with the proper arguments and runs the benchmarks for many different configurations
- `topk.py` analizes the output folders of the simulations and pretty prints the results (for your convinience your can redirect them in a file, but you should comment out the bold print statements)
- `plot.py` is the final script which plot diagrams for the parameters individually so we can see the effect of the component on the system.

Though there many hypothesis that can be made to conduct this lab, we made the following one:

`L1 and L2 caches are independent from each other.`

This means that any parameters related to L1 cache will be studied seperately than those related to L2, with the exception of cache line size with affects both. Hence we conducted 2 expirements:

### L1 expirement

Here we tune the i-cache and d-cache size and associativity as well as cache line size. We wanted to see have i-cache and d-cache affect each other. We will check all the possible combinations within a range to find the ideal one. To do so we need some external help to define the boundaries.

[2] and [3] describe what cache line size is and it's a common practice to use 32, 64 and 128 byte sizes (with 64 being dominant). We use the same numbers in our expirements.

[4] points out that associativity is preferred to be a power of 2 as well (although some manifucturerers like AMD have used 3-way associative caches in the past). From the class lectures we've seen associativities ranging from 1 to 16, so we don't go further in our expirements. More specifically we use 1/2/4-way associative i-caches, 2/4/8 associative d-caches and 4/8/16 associative L2-caches.

Finally there are too many ways to split cache size. We didn't find any reason to go beyond 16 KB L1-cache or 256 KB L2-cache, and although these sizes aren't supposed to be a power of 2, setting them so helps divide nicely and uniformly the spectrum.

We kept the default parameters for L2-cache since we made the hypothesis they affect our system independently from L1 and we will figure the ideal configuration in the next section.

Below we can see the effect of the components in our system. We run the 5 given benchmarks for 10M instruction on a laptop with a core i7-6500U CPU and 8 gigs of RAM. This first expirement took about one day.

<p align="center">
<img src=img/i-cache.jpg>
<img src=img/d-cache.jpg>
<img src=img/l1-cache-line.jpg>
</p>

Although we see a more rapid slot change in the first 2 diagrams we note that the actual improvement in CPI is tiny. On the other hand cache line size greately affects the average CPI. Also seeing some room for improvement it would be interesting to go beyond these limits and further inscrease associativity while also try to max out L1-D cache (We could try a 192 KB d-cahe with a 64 KB i-cache).

However in the context of this lab and due to the tiny improvement of the CPI we don't go beyond the above expirements. For the next section it would be interesting to max out the specs with the exception of L1 i-cache but as we can see by running `topk.py` (see `results-1.txt`) we can have the same CPI with the configuration below (well, up to the 2nd decimal digit...):

- L1 i-cache size: **32 KB**
- L1 i-cache associativity: **2**
- L1 d-cache size: **32 KB**
- L1 d-cache associativity: **2**
- Cache line size: **128**

**Overall we only see that only cache line size notably affects the CPI as configs with the same cache line size end up having almost the same average CPI (check `results-1.txt`)**

### L2 Expirement

Now we test the L2 cache. As noted in the previous section we are going to use powers of 2. We range L2 cache size from 256KB to 4MB and L2 associativity from 4 to 16 way. We will also tuny cache line size since it may affect the performance.

<p align="center">
<img src=img/l2-cache.jpg>
<img src=img/l2-cache-line.jpg>
</p>

Here we see more aggressive slops. Although the CPI isn't greately affected by the L2 configuration the plots would encourage us to go beyond the tested specs. But 4 MB is the given limit for this lab and honestly we haven't saw a L2-cache with associativity higher than 16. So we settle here.

Again cache line size is what really lowered the average CPI. The results of this section are in `results-2.txt` while you can take a look of the overall results in `results.txt`.

**Theoretically the *ultimately best* configuration would be the maxed out one with the exception of i-cache size (which we would set at 64 KB).**

Finally we would like to reference [5] as it was a nice and hands-on article on how caches affect the execution time.

In this repo we include `l1.npy` and `l2.npy` as they don't take much space and they contain all the essential information about the average CPI, however we *gitignored* the `xplore-1` and `xplore-2` folder which contain gem5's simulation results as they are about 800 MB containing excesive information.


## 3. Cost analysis and optimization

In order to define the cost function relating to the characteristics of our architectural design, firstly we need to understand the importance of each one of these parameters το the CPI and execution time. If we notice the results of our experiment, we see that the change of the cache line size alters the CPI more than any other factor. An other significant parameter are cache memories sizes. Decreasing the L2 cache size increases the CPI a bit more, whilst decreasing the L1 cache size does the same as well. Although the difference on L1 is that it is divided into instruction and data cache. So, to remain at the same CPI, the sum of these two memories combined shall not fall down to one order of magnitude. Instruction cache size, though, is a bit more effective than data cache. That's why its coefficient is a bit bigger. Finally, it is observed that any change on the associativity does not affect CPI on a worth noticing level.

#### Cache size vs Cost
Depending to the cost, it is common known that increasing the size of a memory, the cache's price is increased as well. Although the value of L1 is a lot bigger than the one of L2 because of its complexitivity. That's why we are more flexible on changing L2 cache size than L1. In order to include these changes on our function , it was considered to multiply the terms of L1 and L2 cache sizes with a constant. But the influence of the L2 factor must be bigger than L1's. 

#### Associativity vs Cost
Afterwards it is noticeable that changing the associativity of one memory does not change much the CPI after one specific value, but can improve the performance of our processor without an overhead to the price. The only change is the addition of a multiplexer or a more complex one, which cost is negligible.  That's why we consider that's worthy to change the associativity of the caches until a certain point. After this point our function shall remain almost steady. So, the effect of these parameters is less significant than the others.

#### Cache line size vs Cost
Finally, but most significant of all, it is the cache line size. The change of this value does some significant change on the time and CPI of the executable. This is the reason why its contribution on our function is a lot bigger than the other terms. The drawback though, is that this parameter quite expensive to change afterall. Increasing the size of cache line we decrease the size of our cache because the product remains stable. So we fall one order of magnitude on each of these three cache memories we use. As we see from the results, CPI with a 64 B cache line size is almost twice than the one with a 32 B, but almost 20 percent slower than the 128 B. That's why we recommend the tradeoff of 64 B cache line size, At this way we speed up our architecture as more as we can without decreasing the size of our memories, way too much.

### Speed-Up Function
SpeedUp_f = 5 * Icache_size / 16 + ΙcacheAssoc + 
    5 * Dcache_size / 16 + Dcache_Assoc / 2+ 
    12 * L2cache_size * 256 + L2cacheAssoc / 8 +
    22 * Cache_line_size / 32

The divisions on all those terms is happened in order to normalise the parameters to values that can be compared between all those different terms. For that cause, the minimum values of each parameter were used as dividers. The coefficients are chosen so as to express the effect of each one parameter to the execution time.

### Cost Function
**Cost_f = 8 * Icache_size / 16 + 0.25 * ΙcacheAssoc / 4 + 
   8 * Dcache_size / 16 + 0.25 * Dcache_Assoc / 2 +
    2.2 * L2cache_size * 256 + 0.25 * L2cacheAssoc / 8 +
    10.2 * Cache_line_size / 32**
    
The coefficients of this function was chosen after searching through the bibliography about the effect of each of these parameters to the price value of the processor, as it has been described above.

### Performance function

**Perf_f = SpeedUp_f ^ 2 / Cost_f**

The description of this function is derived from the other two functions, but in order to underline the importance of the CPI, we had to get the square of the first one. 
Using the Perf_f on the results of the benchmarks we take the follow results:

|Benchmark| Ic size |Ic Assoc | Dc size | Dc Assoc | L2 size| L2 Assoc | Line Size |
|---------|---------|---------|---------|----------|--------|----------|-----------|
|Specbzip | 32 KB   | 2       | 32 KB   | 2        | 4096 KB| 16       | 64  B     |
|Spechmmer| 32 KB   | 2       | 32 KB   | 2        | 4096 KB| 16       | 64  B     |
|Speclibm | 32 KB   | 2       | 32 KB   | 2        | 4096 KB| 8        | 64  B     |
|Specmcf  | 32 KB   | 2       | 32 KB   | 2        | 4096 KB| 16       | 64  B     |
|Specsjeng| 32 KB   | 2       | 32 KB   | 2        | 4096 KB| 8        | 64  B     |

It happens to be the same for all the different benchmarks because we didn't run many experiments where the L2 size equals 4096 KB and Cache line size equals 64 B. These two parameters affect the result more than all the others. If we had executed more experiments, instruction cache probably would be one order bigger (64 KB). 

## Review
This exercise was very educational and in order to complete it, we gained knowledge about the architecture of cache memories, the way that they work, as well as the problems a computer architect has to deal with so as to choose the best options for manufacturing a processor. Nevertheless, the time needed for the completion of this exercise was a lot more than it was supposed to. The execution of the examples were very time consuming and we thought that it wouldn't have to. For optimising the quality of this exercise and gaining the real essence of this course, it might be better to limitate the different occasions that we had to search through. A different issue would be also to be given to the students some database of CPUs prices to search to, because the evolution of the technology and the policy of the manufacturing companies, did not allow the facilitation of the work we had to do. To be more specific, all modern processors use more advanced technologies and the majority of the circumstances we had to search about were outdated. But the final impression of this exercise is that it was very interesting and could give the motivation to start the occupation with the computer architecture.

## References

[1] https://cs.stackexchange.com/a/38243

[2] https://stackoverflow.com/a/3947435

[3] https://docs.roguewave.com/threadspotter/2010.4/manual/ch03s02.html

[4] https://www.researchgate.net/post/Why_cache_associativity_is_always_a_power_of_2_and_how_this_school_of_thought_reduces_the_hardware_complexity_of_processor

[5] http://igoro.com/archive/gallery-of-processor-cache-effects/