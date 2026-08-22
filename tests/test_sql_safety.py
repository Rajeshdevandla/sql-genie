import unittest

from core.sql_generator import is_safe_query


class SqlSafetyTests(unittest.TestCase):
    def test_allows_simple_select(self):
        self.assertEqual(is_safe_query("SELECT id, deleted_at FROM users"), (True, None))

    def test_rejects_mutating_statement(self):
        safe, reason = is_safe_query("DELETE FROM users")
        self.assertFalse(safe)
        self.assertIn("DELETE", reason)

    def test_rejects_second_statement(self):
        safe, reason = is_safe_query("SELECT * FROM users; DROP TABLE users")
        self.assertFalse(safe)
        self.assertIn("Multiple", reason)

    def test_allows_one_trailing_semicolon(self):
        self.assertEqual(is_safe_query("SELECT * FROM users;"), (True, None))


if __name__ == "__main__":
    unittest.main()
