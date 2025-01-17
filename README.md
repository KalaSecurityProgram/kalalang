# Kala Compiler

The **Kala Compiler** is a custom compiler designed to transform `.kala` source files into assembly `.s` files. It introduces a simple, expressive language inspired by modern programming paradigms, supporting lists, control flow constructs, and object-oriented programming.

## Features

- **List Handling**: Define and manipulate lists with indexing and updates.
- **Control Flow**: Supports `if`, `while`, and `for` constructs with robust block handling.
- **Object-Oriented Programming**: Define classes and methods for modular code.
- **Custom Syntax**: Simple and readable syntax for beginners and advanced users alike.
- **Assembly Translation**: Converts `.kala` code into low-level assembly for execution.

## Kala Syntax Examples

### List Declaration and Manipulation
```kala
list myList = [1, 2, 3, 4, 5]
print myList[0]
myList[0] = 10
```

### Control Flow
#### If Statement
```kala
if myList[0] == 10 {
    print "First element is 10"
}
```
#### While Loop
```kala
while myList[0] < 15 {
    print "Incrementing"
    myList[0] = myList[0] + 1
}
```
#### For Loop
```kala
for i in range(0, 5) {
    print "Index: "
    print i
}
```

### Object-Oriented Programming
```kala
class MyClass {
    method greet() {
        print "Hello from MyClass!"
    }
}

MyClass instance
instance.greet()
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd kala-compiler
   ```
2. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the compiler:
   ```bash
   python kala_compiler.py <input_file.kala> <output_file.s>
   ```

## Usage

To compile a `.kala` file into assembly:
```bash
python kala_compiler.py example.kala example.s
```

## Project Structure

- `kala_compiler.py`: The main compiler script.
- `examples/`: Sample `.kala` files demonstrating the language features.
- `README.md`: Project documentation.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

The Kala Compiler is licensed under the GNU General Public License v3. See [LICENSE](LICENSE) for details.
