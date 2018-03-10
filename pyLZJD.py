

class IncrementalMMH3:
    """Murmurhash3 implementation that supports incremental inserts

    Based on Ed Raff's java implementation. See:
    https://github.com/EdwardRaff/jLZJD/blob/7f43f79b8ea0757daf872fb8d6f686767eefed35/src/main/java/com/edwardraff/jlzjd/MurmurHash3.java

    Attributes
    ----------
    seed : :obj:`int`, optional
        initial hash seed.

    """

    def __init__(self, seed=0):

        self.seed = seed
        self.c1 = 0xcc9e2d51
        self.c2 = 0x1b873593
        self.reset()


    def reset(self):
        """resets the hash buffer

        :return: None
        """
        self.data = bytearray([0] * 4)
        self._len = 0
        self._h1 = self.seed


    def __len__(self):
        """length of buffer

        :return: int length of underlying hash buffer
        """
        return self._len

    def push_byte(self, b):
        """adds a byte b to the buffer

        Note
        ----
        The following code may set fire to your comp from pure ugly.

        Parameters
        ----------
        b
            the byte.


        Returns
        -------
        data
            current byte buffer
        h1_as_if_done
            current representation of the hash (if it were done?)
        """
        #h1 = seed
        self.data[self._len % 4] = b
        self._len +=1
        #if (_len > 0 & & _len % 4 == 0) // we have a valid history of 4 items!
        if (self._len > 0) and (self._len % 4 ==0):


            k1 = (self.data[0] & 0xff) | ((self.data[1] & 0xff) << 8) | ((self.data[2] & 0xff) << 16) | (self.data[3] << 24)
            k1 *= self.c1

            #todo: doublecheck bit ops
            k1 = (k1 << 15) | ((k1 & 0xff) >> 17)
            k1 *= self.c2

            self._h1 ^= k1

            self._h1 = (self._h1 << 13) | ((self._h1 & 0xff) >> 19)  # ROTL32(h1,13)


            self._h1 = self._h1 * 5 + 0xe6546b64
            h1_as_if_done = self._h1

        # tail
        else:
            k1 = 0
            h1_as_if_done = self._h1
            val = self._len & 0x03
            if val == 3:
                k1 = (self.data[2] & 0xff) << 16
            elif val == 2:
                k1 |= (self.data[1] & 0xff) << 8
            # fallthrough
            elif val == 1:
                k1 |= (self.data[0] & 0xff)
                k1 *= self.c1;
                k1 = (k1 << 15) | (k1 >> 17)#; // ROTL32(k1, 15);
                k1 *= self.c2
                h1_as_if_done ^= k1

            #else:
            #    raise ValueError(val)
            # finalization
            h1_as_if_done ^= self._len

            # fmix(h1)
            h1_as_if_done ^= ((h1_as_if_done  & 0xffffffff) >> 16)
            h1_as_if_done *= 0x85ebca6b
            h1_as_if_done ^= ((h1_as_if_done  & 0xffffffff) >> 13)
            h1_as_if_done *= 0xc2b2ae35
            h1_as_if_done ^= ((h1_as_if_done  & 0xffffffff) >> 16)
        print(h1_as_if_done)

        return h1_as_if_done  # & 0xffffffff



if __name__ == "__main__":
    import numpy as np

    bytes = np.arange(20,dtype=np.uint8).tobytes()
    print('input bytes:', bytes)
    im3 = IncrementalMMH3()

    for byte in bytes:
        print(im3.push_byte(byte))

