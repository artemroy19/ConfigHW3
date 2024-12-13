import toml
import argparse
import re

def parse_toml(toml_path):
    """Парсит TOML файл и возвращает словарь."""
    try:
        with open(toml_path, 'r') as f:
            return toml.load(f)
    except FileNotFoundError:
        return None
    except toml.TomlDecodeError as e:
        print(f"   ")
        return None


def generate_output(data, output_path):
    output = ""
    for key, value in data.items():
        if isinstance(value, dict):
            output += f"{key}(\n"
            for sub_key, sub_value in value.items():
                output += f" {sub_key} = {represent_value(sub_value)},\n" 
            output += ")\n"
        else:
            if isinstance(value, str) and value.startswith("."): 
                try:
                    result = evaluate_expression(value[1:]) 
                    output += f"var {key} := {result}\n"
                except (ValueError, KeyError) as e:
                    print(f"Ошибка вычисления выражения для {key}: {e}")
                    output += f"var {key} := '{value}'\n" 
            else:
                output += f"var {key} := {represent_value(value)}\n"

    try:
        with open(output_path, 'w') as f:
            f.write(output)
        print(f"Выходной файл успешно создан: {output_path}")
    except Exception as e:
        print(f"Ошибка записи в выходной файл: {e}")


def represent_value(value):
    if isinstance(value, str):
        return f"'{value}'"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, dict):
        return represent_dict(value)
    elif isinstance(value, list):
        return '[' + ', '.join(map(represent_value, value)) + ']' 
    else:
        return str(value)

def represent_dict(value):
    output = ""
    output += "(\n"
    for k, v in value.items():
        output += f" {k} = {represent_value(v)},\n" 
    output += ")"
    return output



def evaluate_expression(expression):
    """Вычисляет константное выражение в префиксной форме."""
    tokens = expression.split()
    stack = []
    for token in reversed(tokens):
        if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            stack.append(int(token))
        elif token == '+':
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op1 + op2)
        elif token == '-':
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op2 - op1)
        elif token == '*':
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op1 * op2)
        elif token == 'min':
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(min(op1, op2))
        elif token == 'mod':
            op1 = stack.pop()
            op2 = stack.pop()
            stack.append(op2 % op1)
        else: 
            try:
                
                stack.append(data[token])
            except KeyError:
                raise ValueError(f"Неизвестная переменная: {token}")

    if len(stack) != 1:
        raise ValueError("Неправильное выражение")
    return stack[0]



def main():
    parser = argparse.ArgumentParser(description="Конвертер TOML в учебный конфигурационный язык.")
    parser.add_argument("input", help="Путь к входному TOML файлу")
    parser.add_argument("output", help="Путь к выходному файлу")
    args = parser.parse_args()

    global data 
    data = parse_toml(args.input)
    if data:
        generate_output(data, args.output)

if __name__ == "__main__":
    main()