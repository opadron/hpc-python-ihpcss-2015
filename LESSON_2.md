
## Lesson 2: Using mpi4py for distributed memory parallelism

Below are some key notes on how to use mpi4py.  See
[mpi4py Tutorial](http://www.mpi4py.scipy.org/docs/usrman/tutorial.html) for
more details.

 - Access mpi4py
    ```python
    from mpi4py import MPI

    # no need to call MPI_Init(); it's done automatically
    # no need to call MPI_Finalize(), either;  it's done when the program ends
    ```

 - The "python" version of MPI maps to the C API in a mostly straightforward
   way.

    ```python
    comm = MPI.COMM_WORLD # in C, it's "MPI_COMM_WORLD"

    # most MPI operations are implemented as methods of the Communicator
    size = comm.Get_size() # in C: MPI_Comm_size(comm, &size)
    rank = comm.Get_rank() # in C: MPI_Comm_rank(comm, &rank)
    ```

 - Two flavors of communication methods
   - python version that can send and receive most values
     - they are spelled with all lowercase letters
     - very convenient, but also very slow
    ```python
    if rank == 0:
        x = dict()
        x['python'] = 'awesome!'
        x['source rank'] = rank

        comm.send(x, dest=1) # notice the lowercase spelling
    elif rank == 1:
        x = comm.recv(src=0) # notice the lowercase spelling

    for i in range(2):
        if rank == i:
            print('rank: %d, x: %s' % (rank, str(x)))
        comm.Barrier()
    ```

    ```
    rank: 0, x: {'source rank': 0, 'python': 'awesome!'}
    rank: 1, x: {'source rank': 0, 'python': 'awesome!'}
    ```

   - very fast version that uses buffer objects (such as numpy arrays)
     - these have the first letter capitalized (like in C)

    ```python
    if rank == 0:
        x = np.arange(10, dtype=np.int32)

        # notice the Capitalized spelling
        # type and number of elements are automatically inferred from the array
        comm.Send(x, dest=1, tag=12)
    elif rank == 1:
        x = np.empty((10,), dtype=np.int32)

        # notice the Capitalized spelling
        #
        # also, other MPI options, such as tag can
        # be supplied as optional keyword arguments
        comm.Recv(x[:], src=0, tag=12)


    for i in range(2):
        if rank == i:
            print('rank: %d, x: %s' % (rank, str(x)))
        comm.Barrier()
    ```

    ```
    rank: 0, x: [0 1 2 3 4 5 6 7 8 9]
    rank: 1, x: [0 1 2 3 4 5 6 7 8 9]
    ```


 - Examples of several MPI operations
   - point-to-point communication
    ```python
    # pure python version
    comm.send(data, dest=1, tag=11)
    data = comm.recv(source=0, tag=11)

    # native version
    comm.Send(data[1:100], dest=1, tag=21)
    comm.Recv(data[101:200], source=0, tag=21)
    ```

   - broadcasting
    ```python
    # pure python version
    data = comm.bcast(data, root=0)

    # native version
    comm.Bcast(data[1:100], root=0)
    ```

   - scattering
    ```python
    # pure python version
    size = comm.Get_size()
    rank = comm.Get_rank()
    data = None
    if rank == 0:
        data = list(range(size))

    data = comm.scatter(data, root=0)
    assert rank == data

    # native version (if data and input_data were both numpy arrays)
    comm.Scatter(data[:size], input_data[:1], root=0)
    assert rank == input_data[0]
    ```

   - Gathering
    ```python
    # pure python version
    data = comm.gather(rank, root=0)

    # native version (if output_data and data were both numpy arrays)
    comm.Gather(output_data[:1], data[:size], root=0)
    ```

   - Reduction
    ```python
    # pure python version
    local_max = compute_scalar()
    global_max = comm.reduce(local_max, op=MPI.MAX, root=0)

    # native version
    local_max = np.empty((1,))
    global_max = np.empty((1,))

    local_max[0] = compute_scalar()
    comm.Reduce(local_max, global_max, op=MPI.SUM, root=0)
    ```

   - Other operations
     - Asynchronous communication
       - The asynchronous operations return a request object with a `wait()`
         method
    ```python
    req = comm.ISend(data[:], dest=1)
    compute_something_else()
    req.wait()
    ```
     - And finally, most other variants of the MPI operations are available
     (`Allreduce()`, `Sendrecv()`, `Bsend()`, `Ibsend()`, `Ssend()`, `Issend()`,
     `Alltoall()`, etc.)

### Exercise 2
 - Start in the `laplace-mpi/` directory
 - Edit the `laplace_mpi.py` file and replace the missing sections of code
   with your own code that uses MPI
 - Type `make run` to run the application with your changes
   - Use the `laplace-serial` example as a reference implementation
 - Try to get the best performance by using the native operations for sending
   and receiving large messages.

