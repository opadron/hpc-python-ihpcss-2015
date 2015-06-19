
## Introduction

### HPC Programming With Python
**Omar Padron**<br>
Blue Waters Science and Engineering Application Support<br>
[NCSA](http://www.ncsa.illinois.edu) - Illinois, USA

### Setup

    ssh your_user_name@bwbay.ncsa.illinois.edu
    # enter your password
    
    git clone git://github.com/opadron/hpc-python-ihpcss-2015
    cd hpc-python-ihpcss-2015
    source idev
    # wait for your interactive job to start
    
    cd $PBS_O_WORKDIR
    source environment

You should get two lines of output telling you the version of python loaded.
The phrase "Blue Waters" should be highlighted.

    
    Python 2.7.5 (default, Mar 12 2015, 11:35:48)
    [GCC 4.8.2 20131016 (Cray Inc.)] on Blue Waters
    

If you see the above output, then you are ready to go!

### Python for HPC
 - Why Python?
   - Faster development cycle
     - Usually only need 1/10<sup>th</sup> of the number of lines of code
   - More flexibility
   - Greater software ecosystem
     - The [Python Package Index](https://pypi.python.org/pypi) has over
       60 **thousand** packages available.
<br>
 - Outstanding technical challenges
   - [Global Interpreter
     Lock](https://wiki.python.org/moin/GlobalInterpreterLock)
   - Development Tools Still Lacking
     - Need better profilers/debuggers
     - Tools are getting better, but still not "there", yet.
   - Parallel import problem
     - When a large number of nodes all try to read from the same file on a
       shared filesystem.
     - Not unique to Python, but particularly bad for Python
<br>
 - Can you really use Python productively in HPC?
   - Answer depends on what you consider "Python"
     - Pure, interpreted Python code is too slow to be useful
     - however, Python software has tools to help with this
       - combines high-level, interpreted code with low-level, compiled code
       - gives you flexibility where you want it, and speed where you need it
<br>
 - Some expectation management:
   - Python is a great tool, but is neither magic nor a silver bullet.
     - A sufficiently well-tuned, compiled code will almost always outperform
       even the best hand-crafted Python codes.
     - Using Python is consciously choosing to sacrifice some computer
       power for the sake of "people" power.
     - The point of this session is to show how we can avoid throwing the
       performance baby out with the development bath water.
<br>
 - There's too much to see in Python land to fit in an afternoon.
   - Stuff we won't be covering
     - Python + Fortran (sorry, Fortran programmers)
     - Python + C++
     - GPGPU Programming
     - Visualization
       - there's a far better talk happening in the other room (right now!)

### Goals and Agenda
 - Our goal
   - to explore, by example, how to use the tools Python gives you to produce
     HPC applications in less time and effort than with strictly compiled
     languages
     - while retaining an appreciable fraction of the performance of a strictly
       compiled application.
<br>
 - Agenda
   - Description of our two sample applications
     - one is embarrassingly parallel
     - the other has more shame :)
   - Walkthrough of the code for each serial implementation
     - Both pure, sequential, sloooooow Python
   - Then, we'll look at some Python tools that can help us to iteratively
     improve its performance
     - I will demonstrate each on the simpler problem
     - _You_ will work on the more challenging problem (with some help)

### Problem Descriptions
 - **[The Basel problem](https://en.wikipedia.org/wiki/Basel_problem)**<br>
   ![alt](https://upload.wikimedia.org/math/e/6/5/e65abf049dfa50ad9c7db8ae466a495a.png)
   - The whole program just computes a big sum
   - Not a practical way of approximating pi
     - Converges very slowly
     - But a great problem for demonstrating Python programming
<br>
 - **Solution of [Laplace's Equation](https://en.wikipedia.org/wiki/Laplace%27s_equation) in 2D**<br>
   ![alt](https://upload.wikimedia.org/math/a/8/7/a87b3b4e89ea9a5f4c749f9fb56e3336.png)
   - Jacobi Iterations on a 2D array
     - New value at each point in the array is the average of its four cardinal
       neighbors
     - Repeat until the values settle
   - Not as simple, but not too complicated, either

### Schedule (Hopefully)
 - Code Walkthrough
 - [Lesson 1](LESSON_1.md): Using Numpy as a faster array data type
 - [Lesson 2](LESSON_2.md): Using mpi4py for distributed memory parallelism
 - BREAK
 - [Lesson 3](LESSON_3.md) (Advanced!): Generating optimized C code with Cython

