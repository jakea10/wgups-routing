# hash_table.py

from typing import NamedTuple, Any


DELETED = object()  # sentinel value for linear probing


class Pair(NamedTuple):
    key: Any
    value: Any


class HashTable:
    def __init__(
            self,
            capacity: int = 8,
            load_factor_threshold: float = 0.6
        ):
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Capacity must be a positive integer")
        if not (0 < load_factor_threshold <= 1):
            raise ValueError("Load factor must be a number between (0 and 1]")
        self._slots = capacity * [None]
        self._load_factor_threshold = load_factor_threshold


    def __len__(self):
        return len(self.pairs)
    

    def __setitem__(self, key, value):
        if self.load_factor >= self._load_factor_threshold:
            self._resize_and_rehash()

        for index, pair in self._probe(key):
            if pair is DELETED:
                continue  # collsion has occurred before
            if pair is None or pair.key == key:  # new key or update
                self._slots[index] = Pair(key, value)
                break


    def __getitem__(self, key):
        for _, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                return pair.value
        raise KeyError(key)
    

    def __delitem__(self, key):
        for index, pair in self._probe(key):
            if pair is None:
                raise KeyError(key)
            if pair is DELETED:
                continue
            if pair.key == key:
                self._slots[index] = DELETED
                return
        raise KeyError(key)
    

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
        
    
    def __iter__(self):
        yield from self.keys
    

    def __str__(self):
        pairs = []
        for key, value in self.pairs:
            pairs.append(f"{key!r}: {value!r}")
        return "{" + ", ".join(pairs) + "}"
    

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}.from_dict({str(self)})"
    

    def __eq__(self, other):
        if self is other:  # same id()
            return True
        if type(self) is not type(other):
            return False
        return set(self.pairs) == set(other.pairs)
    

    def _index(self, key) -> int:
        return hash(key) % self.capacity


    def _probe(self, key):
        index = self._index(key)
        for _ in range(self.capacity):
            yield index, self._slots[index]
            index = (index + 1) % self.capacity  # modulo wraps index around origin if necessary

    def _resize_and_rehash(self):
        copy = HashTable(capacity=self.capacity * 2)
        for key, value in self.pairs:
            copy[key] = value
        self._slots = copy._slots


    def get(self, key, default = None):
        try:
            return self[key]
        except KeyError:
            return default
    

    def copy(self):
        return HashTable.from_dict(dict(self.pairs), self.capacity)
    

    def clear(self):
        self._slots = self.capacity * [None]
    

    @property
    def pairs(self):
        return {
            pair for pair in self._slots
            if pair not in (None, DELETED)
        }
    

    @property
    def values(self):
        return [pair.value for pair in self.pairs]
    

    @property
    def keys(self):
        return {pair.key for pair in self.pairs}
    

    @property
    def capacity(self):
        return len(self._slots)
    

    @property
    def load_factor(self):
        occupied_or_deleted = [slot for slot in self._slots if slot]
        return len(occupied_or_deleted) / self.capacity


    @classmethod
    def from_dict(cls, dictionary: dict, capacity: int = None):
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
