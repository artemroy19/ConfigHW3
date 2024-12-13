import unittest
import tempfile
import os
import toml
from main import parse_toml, generate_output, evaluate_expression # Замените your_module


class TestTomlParser(unittest.TestCase):

    def test_parse_toml_valid(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".toml") as tmp:
            tmp.write("[section]\nkey = \"value\"\n")
            tmp.flush()
            filepath = tmp.name
        result = parse_toml(filepath)
        self.assertEqual(result, {'section': {'key': 'value'}})
        os.remove(filepath)

    def test_parse_toml_invalid(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".toml") as tmp:
            tmp.write("invalid toml")
            tmp.flush()
            filepath = tmp.name
        self.assertIsNone(parse_toml(filepath))
        os.remove(filepath)

    def test_parse_toml_not_found(self):
        self.assertIsNone(parse_toml("nonexistent_file.toml"))


class TestOutputGenerator(unittest.TestCase):

    def test_generate_output_with_expression_error(self):
        data = {'result': '+ 10 a'}  # Некорректное выражение
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            generate_output(data, tmp.name)
            with open(tmp.name, 'r') as f:
                output = f.read()
            self.assertIn("var result := '+ 10 a'", output)  # Выражение должно быть сохранено как строка
            os.remove(tmp.name)

class TestExpressionEvaluator(unittest.TestCase):

    def test_evaluate_expression_addition(self):
        self.assertEqual(evaluate_expression("+ 10 20"), 30)

    def test_evaluate_expression_subtraction(self):
        self.assertEqual(evaluate_expression("- 10 20"), 10)

    def test_evaluate_expression_multiplication(self):
        self.assertEqual(evaluate_expression("* 10 20"), 200)

    def test_evaluate_expression_min(self):
        self.assertEqual(evaluate_expression("min 10 20"), 10)


if __name__ == '__main__':
    unittest.main()

