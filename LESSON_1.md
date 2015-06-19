
## Lesson 1: Using Numpy as a faster array data type

Below are some key notes on how to use numpy.  See
[Tentative NumPy Tutorial](http://wiki.scipy.org/Tentative_NumPy_Tutorial) for
more details on the different parts of the numpy library.

 - Access numpy

    ```python
    import numpy as np
    ```
 - How to make new arrays
    ```python
    shape = (10, 20)  # for a 10x20 array
    type = np.float64 # for doubles (default)

    # allocate without initializing
    my_array = np.empty(shape, dtype=type)

    # allocate and initialize to zeros
    my_array = np.zeros(shape, dtype=type)

    # allocate and inintialize to ones
    my_array = np.ones(shape, dtype=type)

    # below are two ways of building the same array
    start = 0.0
    end = 10.0
    num_points = 20
    increment = (end - start)/num_points

    my_array = np.linspace(start, end, num_points, endpoint=False, dtype=type)
    my_array = np.arange(start, end, increment, dtype=type)
    ```
 - Basic Operations
   - Apply Elementwise
   - Multiplication (`*`) is element-wise multiplication
     (**not matrix multiplication**)
     - use `np.dot(A, B)` for matrix multiplication
   - Some operations (e.g.: `+=`) operate in-place
   - Reduction operators reduce the entire array by default
     - `np.max(A)` will return the maximum value in the whole array
     - Use the `axis` keyword arguments to reduce along a particular
       dimension
    ```python
    max_columns = np.max(A, axis=0)
    ```

 - Universal Functions (ufuncs)
   - Mathematical expressions that operate element-wise over any number of
     dimensions
     - Mostly just transcendental functions (sin, sqrt, log)

 - Indexing and Slicing
   - `A[i, j, k]`: all indeces between a single pair of brackets
   - Can access slices instead of individual elements
    ```python
    A[start:stop:stride, j, k]
    ```
   - Can use ellipses to "slice" over the dimensions, themselves
    ```python
    A[::2, ..., 3]
    ```
   - Useful for writing your own ufuncs that work over any number of
     dimensions
     - Laplace operator
     - Hyper gradient

 - "Vectorizing" your Python code
   - All of numpy's number crunching routines are implemented in compiled C
     - So, the best way to take advantage of the compiled code speed is to
       express as many of your calculations in terms of large, element-wise,
       array expressions as possible.
       - Replacing for loops with array expressions is usually a good way to
         start
         - `num_positive = np.count_nonzero(my_array > 0.0)` is much faster than
           a for loop in Python

### Exercise 1
 - Start in the `laplace-numpy/` directory
 - Edit the `laplace_numpy.py` file and replace the missing sections of code
   with your own code that uses numpy
 - Type `make run` to run the application with your changes
   - Use the `laplace-serial` example as a reference implementation
 - Try to get the best performance by making use of numpy's array expressions
   wherever you can

