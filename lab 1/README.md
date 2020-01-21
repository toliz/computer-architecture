# Lab 1

## 1. System configuration

The main configuration of the simulated machine are located in the main function of the `starter_se.py` file. These parameters are parsed via the argparse python library to the script.

When running the command

`$ ./build/ARM/gem5.opt -d hello_result configs/example/arm/starter_se.py
--cpu="minor" "tests/test-progs/hello/bin/arm/linux/hello"`

all default arguments are used except *CPU model* which is set to *minor CPU*. Hence the parameters used are the following:

- **CPU model:** minor
- **CPU frequency:** 4 GHz
- **Number of cores:** 1
- **Memory type:** DDR3 @ 1600 MHz 8x8 configuration (8 banks / rank with 8-bit bus)
- **Memory channels:** 2
- **Memory ranks:** None (which probably translates to the model default)
- **Memory size:** 2 GB

## 2. Configuration files

We use the files configuration files config.ini and config.json to verify the above parameters. Below we see a table matching the lines from `config.ini` to the above parameters:

<center>

| Lines        | Commands                                     | Comments |
|-------------:|----------------------------------------------|----------|
| 67           |`type=MinorCPU`                               |          |
| -            | -                                            | CPU frequency missing  |
| 66<br>117    |`[system.cpu_cluster.cpus]`<br>`numThreads=1` |Here we see that there is a single CPU device with a single thread|
| 1265<br>1270 | `banks_per_rank=8`<br>`device_bus_width=8`   | The notation *8x8* is used to describe 8 banks with an 8-bit bus width |
| -            | -                                            | No. of memory channels missing
| 1296<br>1387 | `ranks_per_channel=2`                        |          |
| 1272<br>1363 | `device_size=536870912`                      | 512MB x 2 devices x 2 ranks = 2GB |

</center>

## 3. In-order CPU models

According to [gem5 main page](gem5.org/Main_Page) there are four CPU models:
- a simple CPI CPU
- a detailed in-order CPU
- a detailed out-of-order CPU
- a KVM (Kernel based Virtual Machine) CPU

Out of these four only the first two are in order models:

### Simple CPU

`SimpleCPU` model is better suited for general tryouts, such as testing the workability of a program or its warm-up period. It is consisted of two parts.
The first one is a non-self-executable class , BaseSimpleCPU and is able to check for interrupts, set up a fetch request, handle pre-execute setup, handle post-execute actions, and advance the PC to the next instruction. The second one is divided into two categories, relatively to the memory's type of access and they are both extensions of BaseSimpleCPU, namely AtomicSimpleCPU and TimingSimpleCPU.

`AtomicSimpleCPU` uses the very fast atomic memory accesses . They are able of returning the time that a request needs to be completed, allthough without the delays or the resource contentions, while they are also used for fast forwarding and warming up caches . When the function returns, only then the response returns as well. In this case, the latency estimates from these accesses to estimate overall cache access time. It is also used to read and write memory. AtomicSimpleCPU connects the CPU to the cache,through defining the port which hooks up to memory. In gem5, AtomicSimpleCPU performs all operations for an instruction on every CPU tick(). 

On the contrary `TimingSimpleCPU` uses timing memory accesses. These are the most detailed. They intent to be more realistic, accordingly to the timing, while they include queuing delays and resource contentions. It stalls  on cache accesses and waits for the memory system to respond prior to proceeding. This model of CPU waits for the return from the memory access in otder to provide some level of timing and it can process only one instruction per time.  It uses the same functions as BaseSimpleCPU and defines the port that is used to hook up to memory and connects the CPU to the cache. 


### In-order CPU
`InOrder CPU` model is used to simulate in-order pipelines where ISA and pipeline descriptions are not predefined and specific. The main goal of this model is to provide generic pipeline stages , the number of which can be determined by the user. Furthermore, it uses the resource-request model, in which all the necessary for the CPU components are depicted by the Resource class. Each "resource" will be requested by an instruction with a very specific operation which the resource needs to perform. When the resource completes the task, the instruction can move to the next level. In this way the designers to modelize new custom pipelines from an advanced base.

### Minor CPU
Additionally there is the `Minor CPU` model. Minor CPU works with fixed pipeline while multithreading is not capable by its default settings. Its pipeline is in four stages --Fetch1-Fetch2-Decode-Execution-- and controls the cyclic tick event and the cycle skipping (idling). Its data structures are configurable but large-amounts of life-cycle information are avoided. All internal structures have fixed sizes on construction. Gem5 contains objects of MINORCPU and can provide data and instruction interfaces for connection to a cache system through a Python configuration. Its main goal is to provide a framework for processors with similar capabilities.

## Benchmarking

### 3.a Running the demo
We wrote a demo program `demo.c` for benchmarking.

The execution time for the **Minor CPU** is *13.838 ms* while for the **TimingSimple CPU** is *33.951 ms*.

### 3.b Intuition
From the results we can tell that there is a huge difference between the two executions. The first one, using the MinorCPU, is a lot faster than the one with the TimingSimpleCPU. First of all, the MinorCPU , works with the known Pipeline --Fetch1-Fetch2-Decode-Execute-- which gives the CPU the ability of parallel actions as it is seemed by the picture. The instructions of MinorCPU in gem5 are very simple. In addition to this, the simplicity of the program that we executed allows the MinorCPU to be very effective on this amount of time.

On the contrary, TimingSimpleCPU works in a different way. The execution is very thorough, while it contains all the time delays and resource contentions that would actually happens in a realistic situation where this CPU would work. Waiting for the response of the system in order to process to the next instruction has negative effects on the execution time and stalls the whole procedure. 

### 3.c Testing different clock speeds and mem-types

We change the **CPU Clock** from 1 to 3 GHz for the 2 models keeping the default memory type. In the table below we can see the execution time of the demo:

<center>

| Clock | CPU type     | Execution time (ms) |
|-------|--------------|---------------------|
| 1 GHz | Minor        | 27.648              |
| 2 GHz | Minor        | 13.838              |
| 3 GHz | Minor        |  9.226              |
| 1 GHz | TimingSimple | 67.875              |
| 2 GHz | TimingSimple | 33.951              |
| 3 GHz | TimingSimple | 22.621              |

</center>

We can see that there is a linear scaling in the CPU clock and the execution time.

We change the **Memory Type** for the 2 models keeping the default CPU Clock. In the table below we can see the execution time of the demo:

<center>

| Memory type         | CPU type     | Execution time (ms) |
|---------------------|--------------|---------------------|
| LPDDR2_S4_1066_1x32 | Minor        | 13.848              |
| DDR3_1600_8x8       | Minor        | 13.838              |
| DDR4_2400_8x8       | Minor        | 13.838              |
| LPDDR2_S4_1066_1x32 | TimingSimple | 33.958              |
| DDR3_1600_8x8       | TimingSimple | 33.951              |
| DDR4_2400_8x8       | TimingSimple | 33.950              |

</center>

We can see that there the memory type barely affects the execution time.

## Lab assessment

The overall experience of the lab was fun. We didn't learn much about compter architecture but we learned various skills like *git* and *markdown*, which are not taught in our university although really helfpul in real life.

We liked the practical and on-point attitude. The lab wasn't about things not related to each other, but about having a solid understading of how *gem5* works; and also a bit of comparing gem5 models, which was our favorite part.

The description of the assignment was very clear and detailed, asking for very specific things and offering guidance, something we are not really used to. So kudos for that :blush: On the other hand though there were some typos on the uploaded pdf which wasted a lot of our time. Moreover the actual duration of the lab was 1h instead of 2h and the staff was not sufficient (in number) to accommodate all our needs :disappointed: Finally the installation of gem5 was too hard for many people, and still some of them haven't installed gem5 on their personal computers. Although not your fault, we think it's worth mentioning :no_mouth: