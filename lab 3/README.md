# Emulator McPAT

## Question 1

### Dynamic Power vs Leakage Power
The power consumed in a device is composed of two types -dynamic or switching power and static or leakage power. 
Dynamic power or switching power, depends on the frequency the transistor is operating on. As performance is increased - by performance we mean the speed and the frequency of the integrated circuit - the amount of dynamic power also increases.
Pdynamic = Pswitching= a * f * Ceff * Vdd^2
a = switching activity
f = switching frequency
Ceff = the effective Capacitance
Vdd = the supply voltage
Leakage is the part of the power that is lost due to gate and channel leakae in each transistor. As  process geometry increases, static leakage loss is increased. In geometries less than 90 nm, leakage power can reach up to 25 % of the total power consumption.
Pleakage = f (Vdd, Vth, W/L)
Vth = threshold voltage
W/L = width and length of the transistor
Dynamic power is dissipating only when switching, but leakage power due to leakage current is continuous.
The execution of different programms on the same processor can not change the leakage power because it depends only on the technology of the processor and it is static. The parameter that will be altered is the dynamic power, because the switching activity and the switching frequency will be altered as well. If a program is more time consuming than another,
then its switching activity and therefore the switching frequency will get bigger and so the Pdynamic according to the equation that is described above.
### Energy Efficiency
Assuming that we have two different processors, the first one consumes 5 Watt and the other one consume 40 Watt on a system fed by a battery with specific capacitance. The second one could not provide the system with larger battery duration due to the energy efficiency.
Energy efficiency is the ratio between the output and the input of an energy conversion machine. Because power is highly connected to the performance (speed and frequency), it is easily understandable that there is a tradeoff between these two parameters. Increasing the performance has negative effect on the energy efficiency. So, the processor of 40 Watt will be more efficient but because of the higher frequency, consequently time duration will be decreased. McPAT is an emulator which ,given the characteristics and the parameters of an architecture of a processor, returns results about the power dissipation. But it does not return any results about the execution time of a program and it is independent of the duration of an executable program. That's why, it is not sufficient to give us information about the battery duration, while this is directly related to the execution time. Besides,  **Energy = Power * Time** and energy efficiency derives from input and output energy.

### Xeon vs ARM A9

|Processors | Technology | Core clockrate |Total Leakage | Peak Dynamic | Total Power Consumption |
|-----------|------------|----------------|--------------|--------------|-------------------------|
|XEON       | 65nm       | 3400MHz        | 36.8319 W    | 98.1063 W    | 134.938 W               |
|ARM A9     | 40nm       | 2000MHz        | 0.108687 W   | 1.6332 W     | 1.74189 W               |
Due to the difference on the clockrate and as a result of the power consumption, XEON can not be more energy efficient than ARM A9, because energy efficiency is related only to energy input and output and not to the speed duration. So even if we decrease the duration of XEON 40 times, the total energy consumed will still remain higher. This is presented more thorough an the paradigm below.
The total power consumption of ARM A9 is 1.74189 W. Assuming t is the execution time of XEON, while ARM' duration is 40 times bigger, then its execution time will be 40t. So the energy output will be **1.74819 * 40t = 69,9276 W < 134.938 W**.

## Question 2

### Energy, Delay, Area
Area is the easiest part it we can get it from from McPAT output file. We can find delay in the stats file of GEM5 and in order to get the energy we need to multiply the power dissipation of the system with the execution time.

The assigment indicates that we should take into account only the core and L2 components, and specifically the Runtime Dynamic, Subthreshold Leakage and Gate Leakage. As the code that reads McPAT's output doesn't run with small modification and spending time for reading McPAT's output is out of the score of this LAB, we use the output of the `print_energy.py` script.

The code that converts GEM5 output from Lab 2 to McPAT compatible XML and runs McPAT is in `xplore.py`.

### Plots
Here we use `plot.py`. This script plots EDAP for each parameter:
<p align="center">
<img src=img/i-cache.jpg>
<img src=img/d-cache.jpg>
<img src=img/l1-cache-line.jpg>
<img src=img/l2-cache.jpg>
<img src=img/l2-cache-line.jpg>
</p>

### Comparison w/ the previous cost function
Script `topk.py` orders the results according to EDAP. We see that the best configuration is:

- L1 i-Cache size: **32KB**
- L1 i-Cache associativity: **2**
- L1 d-Cache size: **32KB**
- L1 d-Cache associativity: **2**
- L2 Cache size: **256KB**
- L2 Cachesize: **16**
- Cache line size: **64**

which makes sense after looking the above diagrams.

This result also agrees with the configuration proposed in the previous lab, with the exception of L2 Cache size.

## Review
After completing all the labs we found the the lab require time, a lot of time. They need time for configuring a strategy to deal with the problem, to write and debug the code and to run the benchmarks. Specifically both Lab 2 and 3 require more than 24 hours of running on a quad-thread PC. Moreover the time and energy spent has little to do with the actual purpose of the class and lab.

Although we like the final result, we think it's not worth the time nor the points, if we consider other classes have easier assigments, for more points, that are not part of the final score but add up to it.

Finally we would like to mention that the 3 labs are actually 3 assigments as the presence to the lab didn't really helped us. There were too many groups and only 2-3 stuff members.

Otherwise we liked the practical spirit and the detailed presentation of the labs. Maybe we would like a bit more insight about how to deal with the problem during the labs.