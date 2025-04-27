from mpi4py import MPI
import hashlib
import string

def md5_cracker(hash_to_crack, start_length, end_length):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

    def generate_attempts(length, prefix=''):
        if length == 0:
            yield prefix
        else:
            for char in characters:
                for next_attempt in generate_attempts(length - 1, prefix + char):
                    yield next_attempt

    for length in range(start_length, end_length + 1):
        for attempt in generate_attempts(length):
            if hashlib.md5(attempt.encode()).hexdigest() == hash_to_crack:
                return attempt
    return None

def main():
    # Initialize MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    #hash_to_crack = "0cc175b9c0f1b6a831c399e269772661"  # Example MD5 hash of "a"
    #hash_to_crack = "900150983cd24fb0d6963f7d28e17f72" # 'abc"
    #hash_to_crack = "5f4dcc3b5aa765d61d8327deb882cf99" # 'password'
    hash_to_crack = "e2fc714c4727ee9395f324cd2e7f331f" # 'abcd'
    #hash_to_crack = "ab56b4d92b40713acc5af89985d4b786" # 'abcde'
    min_length = 1
    max_length = 4

    # Distribute the workload
    total_lengths = max_length - min_length + 1
    range_size = total_lengths // size
    start_length = min_length + rank * range_size
    end_length = start_length + range_size - 1

    if rank == size - 1:
        end_length = max_length

    # Start the timer
    start_time = MPI.Wtime()

    # Each process attempts to crack the hash in its assigned range
    result = md5_cracker(hash_to_crack, start_length, end_length)

    # Gather results at the root process
    results = comm.gather(result, root=0)

    # End the timer
    end_time = MPI.Wtime()

    if rank == 0:
        for r in results:
            if r:
                print("Hash cracked! The plaintext is: {}".format(r))
                break
        else:
            print("Failed to crack the hash.")
        
        # Print the elapsed time
        print("Time taken: {}: seconds".format(end_time - start_time))

if __name__ == "__main__":
    main()
