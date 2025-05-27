from src.hash_table import HashTable, DELETED
import pytest
from pytest_unordered import unordered
from unittest.mock import patch


# def test_should_always_pass():
#     assert 2 + 2 == 4, "This is just a dummy test"


def test_should_create_hash_table():
    assert HashTable(capacity=100) is not None


def test_should_not_create_hash_table_with_zero_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=0)


def test_should_not_create_hash_table_with_negative_capacity():
    with pytest.raises(ValueError):
        HashTable(capacity=-100)


def test_should_not_create_hash_table_with_non_int_capacity():
    args = ["one", 2.5, True]
    for arg in args:
        with pytest.raises(ValueError):
            HashTable(capacity=arg)


def test_should_report_capacity_of_empty_hash_table():
    assert HashTable(capacity=100).capacity == 100


def test_should_report_capacity(hash_table):
    assert hash_table.capacity == 100


def test_should_report_length_of_empty_hash_table():
    hash_table = HashTable(capacity=100)
    assert len(hash_table) == 0


def test_should_report_length(hash_table):
    assert len(hash_table) == 4


def test_should_create_empty_value_slots():
    assert HashTable(capacity=3)._slots == [None, None, None]


def test_should_not_contain_none_value_when_created():
    assert None not in HashTable(capacity=10).values


def test_should_insert_key_value_pairs():
    hash_table = HashTable(capacity=100)
    hash_table["hello"] = "world"
    hash_table[98.6] = 37
    hash_table[True] = False
    hash_table["key"] = None
    assert len(hash_table) == 4


@pytest.fixture
def hash_table() -> HashTable:
    sample_data = HashTable(capacity=100)
    sample_data["hello"] = "world"
    sample_data[98.6] = 37
    sample_data[True] = False
    sample_data["key"] = None
    return sample_data


def test_should_find_value_by_key(hash_table):
    assert hash_table["hello"] == "world"
    assert hash_table[98.6] == 37
    assert hash_table[True] is False
    assert hash_table["key"] is None


def test_should_raise_error_on_missing_key():
    hash_table = HashTable(capacity=10)
    with pytest.raises(KeyError) as exception_info:
        hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_find_key(hash_table):
    assert "hello" in hash_table


def test_should_not_find_key(hash_table):
    assert "missing_key" not in hash_table


def test_should_get_value(hash_table):
    assert hash_table.get("hello") == "world"


def test_should_get_none_when_missing_key(hash_table):
    assert hash_table.get("missing_key") is None


def test_should_get_default_value_when_missing_key(hash_table):
    assert hash_table.get("missing_key", "default") == "default"


def test_should_get_value_with_default(hash_table):
    assert hash_table.get("hello", "default") == "world"


def test_should_delete_key_value_pair(hash_table):
    assert "hello" in hash_table
    assert ("hello", "world") in hash_table.pairs
    assert len(hash_table) == 4

    del hash_table["hello"]

    assert "hello" not in hash_table
    assert ("hello", "world") not in hash_table.pairs
    assert len(hash_table) == 3


def test_should_raise_key_error_when_deleting(hash_table):
    with pytest.raises(KeyError) as exception_info:
        del hash_table["missing_key"]
    assert exception_info.value.args[0] == "missing_key"


def test_should_update_value(hash_table):
    assert hash_table["hello"] == "world"

    hash_table["hello"] = "there"

    assert hash_table["hello"] == "there"
    assert hash_table[98.6] == 37
    assert hash_table[True] is False
    assert hash_table["key"] is None
    assert len(hash_table) == 4


def test_should_return_pairs(hash_table):
    assert hash_table.pairs == {
        ("hello", "world"),
        (98.6, 37),
        (True, False),
        ("key", None)
    }


def test_should_get_pairs_of_empty_hash_table():
    assert HashTable(capacity=10).pairs == set()


def test_should_return_copy_of_pairs(hash_table):
    # Test defensive copying
    assert hash_table.pairs is not hash_table.pairs


def test_should_not_include_blank_pairs(hash_table):
    assert None not in hash_table.pairs


def test_should_return_duplicate_values():
    hash_table = HashTable(capacity=100)
    hash_table["Harry"] = "Gryffindor"
    hash_table["Draco"] = "Slytherin"
    hash_table["Neville"] = "Gryffindor"
    assert hash_table.values.count("Gryffindor") == 2


def test_should_get_values(hash_table):
    # Don't take order into account when comparing
    assert unordered(hash_table.values) == ["world", 37, False, None]


def test_should_get_values_of_empty_hash_table():
    assert HashTable(capacity=100).values == []


def test_should_return_copy_of_values(hash_table):
    assert hash_table.values is not hash_table.values


def test_should_get_keys(hash_table):
    assert hash_table.keys == {"hello", 98.6, True, "key"}


def test_should_get_keys_of_empty_hash_table():
    assert HashTable(capacity=10).keys == set()  # empty set


def test_should_return_copy_of_keys(hash_table):
    assert hash_table.keys is not hash_table.keys


def test_should_convert_to_dict(hash_table):
    dictionary = dict(hash_table.pairs)
    assert set(dictionary.keys()) == hash_table.keys
    assert set(dictionary.items()) == hash_table.pairs
    assert list(dictionary.values()) == unordered(hash_table.values)


def test_should_iterate_over_keys(hash_table):
    for key in hash_table.keys:
        assert key in ("hello", 98.6, True, "key")


def test_should_iterate_over_values(hash_table):
    for key in hash_table.values:
        assert key in ("world", 37, False, None)


def test_should_iterate_over_pairs(hash_table):
    for key, value in hash_table.pairs:
        assert key in hash_table.keys
        assert value in hash_table.values


def test_should_iterate_over_instance(hash_table):
    for key in hash_table:
        assert key in ("hello", 98.6, True, "key")


def test_should_use_dict_literal_for_str(hash_table):
    del hash_table["key"]  # for less permutations to check
    assert str(hash_table) in {
        "{'hello': 'world', 98.6: 37, True: False}",
        "{'hello': 'world', True: False, 98.6: 37}",
        "{98.6: 37, 'hello': 'world', True: False}",
        "{98.6: 37, True: False, 'hello': 'world'}",
        "{True: False, 'hello': 'world', 98.6: 37}",
        "{True: False, 98.6: 37, 'hello': 'world'}",
    }


def test_should_create_hash_table_from_dict():
    dictionary = {"hello": "world", 98.6: 37, True: False}
    hash_table: HashTable = HashTable.from_dict(dictionary)

    assert hash_table.capacity == len(dictionary) * 2
    assert hash_table.keys == set(dictionary.keys())
    assert hash_table.pairs == set(dictionary.items())
    assert unordered(hash_table.values) == list(dictionary.values())


def test_should_create_hash_table_from_dict_with_custom_capacity():
    dictionary = {"hello": "world", 98.6: 37, True: False}
    hash_table: HashTable = HashTable.from_dict(dictionary, 50)

    assert hash_table.capacity == 50


def test_should_have_canonical_string_representation(hash_table):
    del hash_table["key"]  # for less permutations to check
    assert repr(hash_table) in {
        "HashTable.from_dict({'hello': 'world', 98.6: 37, True: False})",
        "HashTable.from_dict({'hello': 'world', True: False, 98.6: 37})",
        "HashTable.from_dict({98.6: 37, 'hello': 'world', True: False})",
        "HashTable.from_dict({98.6: 37, True: False, 'hello': 'world'})",
        "HashTable.from_dict({True: False, 'hello': 'world', 98.6: 37})",
        "HashTable.from_dict({True: False, 98.6: 37, 'hello': 'world'})",
    }


def test_should_compare_equal_to_itself(hash_table):
    assert hash_table == hash_table


def test_should_compare_equal_to_copy(hash_table):
    assert hash_table is not hash_table.copy()
    assert hash_table == hash_table.copy()


def test_should_compare_equal_different_key_value_order():
    h1 = HashTable.from_dict({'a': 1, 'b': 2, 'c': 3})
    h2 = HashTable.from_dict({'b': 2, 'c': 3, 'a': 1})
    assert h1 == h2


def test_should_compare_unequal(hash_table):
    other = HashTable.from_dict({'different': 'value'})
    assert hash_table != other


def test_should_compare_unequal_another_data_type(hash_table):
    assert hash_table != 42


def test_should_clear_key_value_pairs(hash_table):
    assert len(hash_table) == 4
    hash_table.clear()
    assert len(hash_table) == 0


@pytest.fixture
def collision_ht() -> HashTable:
    with patch('builtins.hash', return_value=24):
        ht = HashTable(capacity=100)
        ht['easy'] = 'Requires little effort'
        ht['medium'] = 'Requires some skill and effort'
        ht['difficult'] = 'Needs much skill'
    return ht


def test_should_handle_collisions_on_create(collision_ht: HashTable):
    # linear probe
    assert collision_ht._slots[24] == ('easy', 'Requires little effort')
    assert collision_ht._slots[25] == ('medium', 'Requires some skill and effort')
    assert collision_ht._slots[26] == ('difficult', 'Needs much skill')


def test_should_handle_collisions_on_read(collision_ht: HashTable):
    with patch('builtins.hash', return_value=24):
        assert collision_ht['easy'] == 'Requires little effort'
        assert collision_ht['medium'] == 'Requires some skill and effort'
        assert collision_ht['difficult'] == 'Needs much skill'


def test_should_handle_collisions_on_update(collision_ht: HashTable):
    with patch('builtins.hash', return_value=24):
        collision_ht['difficult'] = 'Requires much skill'
        assert collision_ht['difficult'] == 'Requires much skill'


def test_should_handle_collisions_on_delete(collision_ht: HashTable):
    with patch('builtins.hash', return_value=24):
        del collision_ht['medium']
        assert collision_ht._slots[25] is DELETED