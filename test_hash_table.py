from hash_table import HashTable
import unittest


class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.test_table = HashTable()

    def fill_table_with_one_item(self):
        test_key = "test_key"
        test_value = "test_value"
        self.test_table[test_key] = test_value

    def fill_table_with_four_items(self):
        test_key = "test_key"
        test_value = "test_value"
        for i in range(4):
            self.test_table[test_key+str(i)] = test_value+str(i)

    def test_init_to_create_an_empty_table(self):
        self.assertIsInstance(self.test_table, HashTable)
        expected_value = 4
        self.assertTrue(self.test_table.free_space() == expected_value)

    def test_hashing_private_method_to_hash_a_given_key_to_a_possible_index_to_be_written_to(self):
        # Hashing formula: sum of the unicode codes of all characters of the key modular divided to the current table size.
        key_to_hash = "a"
        expected_index = 1
        returned_index = self.test_table._HashTable__hash(key_to_hash)
        self.assertEqual(expected_index, returned_index)

    def test_check_index_private_method_to_check_given_index_and_return_the_first_possible_free_index_if_the_given_is_not_available(self):
        index_to_check = 0
        expected_first_free_index = 0
        returned_index = self.test_table._HashTable__check_index(index_to_check)
        self.assertEqual(expected_first_free_index, returned_index)
        self.fill_table_with_four_items()
        self.fill_table_with_one_item()
        index_to_check = 0
        expected_first_free_index = 5
        returned_index = self.test_table._HashTable__check_index(index_to_check)
        self.assertEqual(expected_first_free_index, returned_index)

    def test_free_space_method_on_filled_table(self):
        self.fill_table_with_one_item()
        expected_value = 3
        self.assertTrue(self.test_table.free_space() == expected_value)

    def test_set_item_to_create_a_key_value_pair_in_the_table(self):
        self.assertNotIn("test_value", self.test_table.values())
        self.assertNotIn("test_key", self.test_table.keys())
        self.fill_table_with_one_item()
        self.assertEqual(self.test_table["test_key"], "test_value")

    def test_set_item_to_update_value_for_existing_key(self):
        self.fill_table_with_one_item()
        self.test_table["test_key"] = "new_test_value"
        self.assertEqual(self.test_table["test_key"], "new_test_value")

    def test_accessing_item_with_proper_data(self):
        self.fill_table_with_one_item()
        self.assertEqual(self.test_table["test_key"], "test_value")

    def test_accessing_value_with_non_existent_key_for_key_error(self):
        with self.assertRaises(Exception) as error:
            print(self.test_table["non_existent_key"])
        self.assertEqual(type(error.exception), KeyError)

    def test_get_method_with_proper_data(self):
        self.fill_table_with_one_item()
        self.assertEqual(self.test_table.get("test_key"), "test_value")

    def test_get_method_to_disregard_default_parameter_if_proper_data_is_given(self):
        self.fill_table_with_one_item()
        self.assertEqual(self.test_table.get("test_key", default="test_default_value"), "test_value")

    def test_get_item_method_to_return_none_value_if_non_existent_key_used(self):
        self.assertEqual(self.test_table.get("non_existent_key"), None)

    def test_get_item_method_to_return_default_value_if_non_existent_key_used(self):
        self.assertEqual(self.test_table.get("non_existent_key", default="default_value"), "default_value")

    def test_len_magic_method(self):
        self.assertEqual(len(self.test_table), 0)
        self.fill_table_with_one_item()
        self.assertEqual(len(self.test_table), 1)

    def test_contains_magic_method_with_in_and_not_in(self):
        self.fill_table_with_one_item()
        item_to_check = "test_key"
        expected_result = True
        returned_result = item_to_check in self.test_table
        self.assertEqual(expected_result, returned_result)

        self.test_table.clear()
        expected_result = False
        returned_result = item_to_check in self.test_table
        self.assertEqual(expected_result, returned_result)

        self.test_table.clear()
        expected_result = True
        item_to_check = "test_key"
        returned_result = item_to_check not in self.test_table
        self.assertEqual(expected_result, returned_result)

    def test_dynamic_resizing_if_no_free_space_left(self):
        self.fill_table_with_four_items()
        expected_free_space = 0
        expected_capacity_value = 4
        self.assertEqual(self.test_table.free_space(), expected_free_space)
        self.assertEqual(self.test_table.capacity(), expected_capacity_value)
        self.fill_table_with_one_item()
        expected_free_space = 3
        expected_capacity_value = 8
        self.assertEqual(self.test_table.free_space(), expected_free_space)
        self.assertEqual(self.test_table.capacity(), expected_capacity_value)

    def test_keys_method_to_return_a_tuple_of_all_current_keys_in_the_table(self):
        expected_keys = ("test_key0", "test_key1", "test_key2", "test_key3")
        self.fill_table_with_four_items()
        self.assertEqual(self.test_table.keys(), expected_keys)

    def test_values_method_to_return_a_tuple_of_all_current_values_in_the_table(self):
        expected_values = ("test_value0", "test_value1", "test_value2", "test_value3")
        self.fill_table_with_four_items()
        self.assertEqual(self.test_table.values(), expected_values)

    def test_items_method_to_return_a_tuple_of_all_current_items_in_the_table(self):
        expected_items = (("test_key0", "test_value0"), ("test_key1", "test_value1"), ("test_key2", "test_value2"), ("test_key3", "test_value3"))
        self.fill_table_with_four_items()
        self.assertEqual(self.test_table.items(), expected_items)

    def test_clear_method_to_reset_the_table_to_new_empty_table(self):
        self.assertTrue(len(self.test_table) == 0)
        self.fill_table_with_four_items()
        self.assertTrue(len(self.test_table) == 4)
        self.test_table.clear()
        self.assertTrue(len(self.test_table) == 0)

    def test_pop_method_to_remove_a_items_pair_by_key_and_return_its_value(self):
        self.fill_table_with_one_item()
        key_to_be_removed = "test_key"
        expected_value = "test_value"
        self.assertEqual(self.test_table.pop(key_to_be_removed), expected_value)

    def test_pop_method_to_return_default_value_if_key_is_not_present(self):
        false_key = "false_key"
        self.assertNotIn(false_key, self.test_table.keys())
        default_value = "default_value"
        returned_value = self.test_table.pop(false_key, default=default_value)
        self.assertEqual(returned_value, default_value)

    def test_pop_method_to_key_raise_error_if_false_key_and_no_default_value(self):
        false_key = "false_key"
        with self.assertRaises(Exception) as error:
            self.test_table.pop(false_key, default=None)
        self.assertEqual(KeyError, error.exception.__class__)

    def test_popitem_method_to_remove_the_last_inserted_items_pair(self):
        self.assertTrue(len(self.test_table) == 0)
        self.fill_table_with_one_item()
        self.assertTrue(len(self.test_table) == 1)
        self.test_table.popitem()
        self.assertTrue(len(self.test_table) == 0)

    def test_popitem_method_to_return_a_tuple_of_the_removed_items_pair(self):
        self.fill_table_with_one_item()
        expected_result = ("test_key", "test_value")
        returned_result = self.test_table.popitem()
        self.assertEqual(expected_result, returned_result)

    def test_popitem_method_to_raise_key_error_if_trying_to_pop_items_pair_from_empty_table(self):
        with self.assertRaises(Exception) as error:
            self.test_table.popitem()
        self.assertEqual(KeyError, error.exception.__class__)

    def test_copy_method_to_create_a_new_identical_instance_of_the_existent_table(self):
        self.fill_table_with_four_items()
        new_table = self.test_table.copy()
        self.assertIsInstance(new_table, HashTable)
        self.assertTrue(self.test_table.items() == new_table.items())
        self.assertTrue(len(self.test_table) == len(new_table) == 4)

    def test_setdefault_method_to_return_the_value_of_the_specified_key(self):
        self.fill_table_with_one_item()
        expected_result = "test_value"
        returned_result = self.test_table.setdefault("test_key")
        self.assertEqual(expected_result, returned_result)

    def test_setdefault_method_to_inserts_an_non_existent_key_with_the_specified_default_value_as_value(self):
        non_existent_key = "non_existent_key"
        default_value = "default_value"
        self.test_table.setdefault(non_existent_key, value=default_value)
        expected_table_len = 1
        self.assertEqual(len(self.test_table), expected_table_len)
        expected_items_in_table = (("non_existent_key", "default_value"),)
        found_items_in_table = self.test_table.items()
        self.assertEqual(expected_items_in_table, found_items_in_table)

    def test_setdefault_method_to_inserts_an_non_existent_key_with_None_value_if_no_default_value_is_specified(self):
        non_existent_key = "non_existent_key"
        self.test_table.setdefault(non_existent_key)
        expected_items_in_table = (("non_existent_key", None),)
        found_items_in_table = self.test_table.items()
        self.assertEqual(expected_items_in_table, found_items_in_table)

    def test_repr_method(self):
        self.fill_table_with_one_item()
        expected_result = "{'test_key': 'test_value'}"
        self.assertEqual(expected_result, self.test_table.__repr__())


if __name__ == '__main__':
    unittest.main()
