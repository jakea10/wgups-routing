# hash_table.py

from typing import NamedTuple, Any


DELETED = object()  # Sentinel value used to mark a slot as deleted for linear probing (we're using lazy deletion)


class Pair(NamedTuple):
    """Represents a key-value pair stored in the hash table."""
    key: Any
    value: Any


class HashTable:
    """
    A custom implementation of a hash table providing efficient insert, lookup, delete
    and update operations. It uses linear probing for collision resolution.

    This hash table dynamically resizes and rehashes its contents when the load factor
    exceeds a predefined threshold.
    """
    def __init__(
            self,
            capacity: int = 8,
            load_factor_threshold: float = 0.6
        ):
        """
        Initializes a new HashTable instance.

        Args:
            capacity (int): The initial number of slots in the hash table. Must be a positive integer.
            load_factor_threshold (float): The maximum load factor before the hash table resizes.
                                           Must be a number between (0 and 1].

        Raises:
            ValueError: If capacity is not a positive integer or load_factor_threshold is out of range.
        """
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer")
        if not (0 < load_factor_threshold <= 1):
            raise ValueError("Load factor must be a number between (0 and 1]")
        self._slots = capacity * [None]  # Internal list representing the hash table slots
        self._load_factor_threshold = load_factor_threshold


    def __len__(self):
        """
        Returns the number of key-value pairs currently stored in the hash table.
        """
        return len(self.pairs)
    

    def __setitem__(self, key, value):
        """
        Inserts or updates a key-value pair in the hash table.

        If the load factor exceeds the threshold, the table will resize and rehash
        its contents before insertion.

        Args:
            key: The key to insert or update.
            value: The value associated with the key.
        """
        if self.load_factor >= self._load_factor_threshold:
            self._resize_and_rehash()

        # Iterate through potential slots using linear probing.
        for index, pair in self._probe(key):
            if pair is DELETED:
                continue  # Collsion has occurred before, continue probing.
            if pair is None or pair.key == key:  # Found an empty slot or the key already exists.
                self._slots[index] = Pair(key, value)
                break


    def __getitem__(self, key):
        """
        Retrieves the value associated with a given key.

        Args:
            key: The key to search for.

        Returns:
            The value associated with the key.

        Raises:
            KeyError: If the key is not found in the hash table.
        """
        for _, pair in self._probe(key):
            if pair is None:  # Reached an empty slot, key is not present.
                raise KeyError(key)
            if pair is DELETED:
                continue  # Skip over deleted slots and continue probing.
            if pair.key == key:  # Found the key.
                return pair.value
        raise KeyError(key)  # Should not be reached if `_probe` covers all slots and key isn't found.
    

    def __delitem__(self, key):
        """
        Deletes a key-value pair from the hash table.

        Args:
            key: The key of the item to delete.

        Raises:
            KeyError: If they key is not found in the hash table.
        """
        for index, pair in self._probe(key):
            if pair is None:  # Reached an empty slot, key is not present.
                raise KeyError(key)
            if pair is DELETED:
                continue  # Skip over deleted slots and continue probing.
            if pair.key == key:  # Found the key
                self._slots[index] = DELETED  # Mark the slot as deleted.
                return
        raise KeyError(key)  # Key not found after probing all relevant slots.
    

    def __contains__(self, key):
        """
        Checks if a key exists in the hash table.

        Args:
            key: The key to check for.

        Returns:
            True if the key is found, False otherwise.
        """
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
        
    
    def __iter__(self):
        """
        Returns an iterator over the keys in the hash table.
        """
        yield from self.keys
    

    def __str__(self):
        """
        Returns a string representation of the hash table, similar to a dictionary.
        """
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"
    

    def __repr__(self):
        """
        Returns a developer-friendly string representation of the hash table.
        """
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"
    

    def __eq__(self, other):
        """
        Compares this hash table with another object for equality.

        Two hash tables are considered equal if they are the same instance or
        contain the same set of key-value pairs.
        """
        if self is other:  # Same object in memory
            return True
        if type(self) is not type(other):  # Different types
            return False
        return set(self.pairs) == set(other.pairs)  # Compare sets of pairs for equality.
    

    def _index(self, key) -> int:
        """
        Calculates the initial hash index for a given key.

        Args:
            key: They key to hash.

        Returns:
            The initial index in the hash table's slots.
        """
        return hash(key) % self.capacity


    def _probe(self, key):
        """
        Generates a sequence of (index, pair) tuples for linear probing.

        This method yields indices and the corresponding slots in the hash table,
        starting from the initial hashed index and wrapping around if necessary.

        Args:
            key: The key for which to probe.

        Yields:
            tuple: A tuple containing the current index and the content of that slot.
        """
        index = self._index(key)
        for _ in range(self.capacity):
            yield index, self._slots[index]
            index = (index + 1) % self.capacity  # Move to next slot; modulo wraps index around origin if necessary.

    def _resize_and_rehash(self):
        """
        Resizes the hash table to double its current capacity and rehashes all existing pairs.
        """
        copy = HashTable(capacity=self.capacity * 2)  # Create a new, larger hash table.
        for key, value in self.pairs:
            copy[key] = value  # Insert existing pairs into the new table, triggering rehashing.
        self._slots = copy._slots  # Replace the current slots with the new, rehashed slots.


    def get(self, key, default = None):
        """
        Retrieves the value associated with a key, or a default value if the key is not found.

        Args:
            key: The key to search for.
            default: The value to return if the key is not found (defaults to None).

        Returns:
            The value associated with the key, or the default value.
        """
        try:
            return self[key]
        except KeyError:
            return default
    

    def copy(self):
        """
        Creates a shallow copy of the hash table.

        Returns:
            HashTable: a new HashTable instance with the same key-value pairs.
        """
        return HashTable.from_dict(dict(self.pairs), self.capacity)
    

    def clear(self):
        """
        Removes all key-value pairs from the hash table, effectively emptying it.
        """
        self._slots = self.capacity * [None]
    

    @property
    def pairs(self):
        """
        Returns a set of all (key, value) pairs currently in the hash table.
        Deleted and empty slots are excluded.
        """
        return {
            pair for pair in self._slots
            if pair not in (None, DELETED)
        }
    

    @property
    def values(self):
        """
        Returns a list of all values currently in the hash table.
        """
        return [pair.value for pair in self.pairs]
    

    @property
    def keys(self):
        """
        Returns a set of all keys currently in the hash table.
        """
        return {pair.key for pair in self.pairs}
    

    @property
    def capacity(self):
        """
        Returns the total number of slots in the hash table.
        """
        return len(self._slots)
    

    @property
    def load_factor(self):
        """
        Calculates and returns the current load factor of the hash table.

        The load factor is the ratio of occupied or deleted slots to the total capacity.
        """
        occupied_or_deleted = [slot for slot in self._slots if slot]
        return len(occupied_or_deleted) / self.capacity


    @classmethod
    def from_dict(cls, dictionary: dict, capacity: int = None):
        """
        Creates a HashTable instance from a given dictionary.

        Args:
            dictionary(dict): The dictionary to populate the hash table with.
            capacity(int, optional): The initial capacity for the hash table. If None, capacity will be len(dictionary) * 2.
        """
        hash_table = cls(capacity or len(dictionary) * 2)
        for key, value in dictionary.items():
            hash_table[key] = value
        return hash_table
    

if __name__ == "__main__":
    # ----------------------------------------------------------
    # ad hoc testing
    # ----------------------------------------------------------

    # Visualize dynamic resizing
    ht = HashTable()

    for i in range(50):
        num_pairs = len(ht)
        num_empty = ht.capacity - num_pairs
        print(
            f"{num_pairs:>2}/{ht.capacity:>2}",
            ("▣ " * num_pairs) + ("□ " * num_empty)
        )
        ht[i] = i
