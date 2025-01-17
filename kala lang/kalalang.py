############################################################################
#
# This file is part of the Kalalang compiler.
#
# The Kalalang compiler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the 
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# The Kalalang compiler is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# the Kalalang compiler.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

################################
import sys
import os
import argparse
import logging
################################

class KalaCompiler:
    def __init__(self):
        self.block_stack = []  # Stack to manage nested blocks

    def compile(self, input_file, output_file):
        """
        Compile a .kala file into assembly (.s).
        """
        # Check if the input file exists
        if not os.path.exists(input_file):
            logging.error("Input file does not exist.")
            return False

        # Check if the output file exists
        if os.path.exists(output_file):
            logging.error("Output file already exists.")
            return False

        # Ensure the input file has a .kala extension
        if not input_file.endswith(".kala"):
            logging.error("Input file must have a .kala extension.")
            return False

        # Ensure the output file has a .s extension
        if not output_file.endswith(".s"):
            logging.error("Output file must have a .s extension.")
            return False

        # Read and parse the input file
        try:
            with open(input_file, "r") as f:
                code = f.read()

            # Transform Kala syntax to assembly code
            asm_code = self.parse_kala_code(code)

            # Write the assembly code to the output file
            with open(output_file, "w") as f:
                f.write(asm_code)

        except Exception as e:
            logging.error(f"Error during compilation: {e}")
            return False

        logging.info("Compilation successful.")
        return True

    def parse_kala_code(self, code):
        """
        Transform Kala syntax into assembly code.
        """
        asm_code = ""  # Assembly output

        for line in code.splitlines():
            line = line.strip()

            # Skip comments
            if line.startswith("#"):
                continue

            # Parse Kala-specific syntax
            if line.startswith("list "):
                # Handle lists
                name, elements = self.parse_list_declaration(line)
                asm_code += f"{name}: .data {', '.join(elements)}\n"

            elif line.startswith("class "):
                # Handle class declarations
                asm_code += self.parse_class(line)

            elif line.startswith("method "):
                # Handle methods
                asm_code += self.parse_method(line)

            elif line.startswith("print "):
                # Handle print statements
                asm_code += self.parse_print(line)

            elif line.startswith("if "):
                # Handle if statements
                asm_code += self.parse_if(line)

            elif line.startswith("while "):
                # Handle while loops
                asm_code += self.parse_while(line)

            elif line.startswith("for "):
                # Handle for loops
                asm_code += self.parse_for(line)

            elif line == "}":
                # Handle block closure
                asm_code += self.parse_block_close()

            else:
                # Default case: emit raw assembly
                asm_code += f"; {line} (unrecognized syntax)\n"

        return asm_code

    def parse_list_declaration(self, line):
        """
        Parse a Kala list declaration.
        Syntax: list list_name = [element1, element2, ...]
        """
        try:
            _, rest = line.split("list ", 1)
            name, elements = rest.split("=", 1)
            name = name.strip()
            elements = elements.strip().strip("[]").split(",")
            elements = [elem.strip() for elem in elements]
            return name, elements
        except Exception as e:
            logging.error(f"Error parsing list declaration: {e}")
            return None, []

    def parse_class(self, line):
        """
        Parse a Kala class declaration.
        Syntax: class ClassName { ... }
        """
        class_name = line.split("class ", 1)[1].strip(" {")
        self.block_stack.append(f"class_{class_name}")
        return f"; Start of class {class_name}\n"

    def parse_method(self, line):
        """
        Parse a Kala method declaration.
        Syntax: method MethodName { ... }
        """
        method_name = line.split("method ", 1)[1].strip(" {")
        self.block_stack.append(f"method_{method_name}")
        return f"; Start of method {method_name}\n"

    def parse_print(self, line):
        """
        Parse a Kala print statement.
        Syntax: print "message"
        """
        try:
            _, message = line.split("print ", 1)
            message = message.strip("\"")
            return f"mov $1, %rax\nmov $1, %rdi\nlea {message}, %rsi\nsyscall\n"
        except Exception as e:
            logging.error(f"Error parsing print statement: {e}")
            return ""

    def parse_if(self, line):
        """
        Parse a Kala if statement.
        Syntax: if condition { ... }
        """
        try:
            condition = line.split("if ", 1)[1].strip(" {")
            self.block_stack.append("if")
            return f"cmp {condition}, 0\nje else_label\n"
        except Exception as e:
            logging.error(f"Error parsing if statement: {e}")
            return ""

    def parse_while(self, line):
        """
        Parse a Kala while loop.
        Syntax: while condition { ... }
        """
        try:
            condition = line.split("while ", 1)[1].strip(" {")
            self.block_stack.append("while")
            return f"while_label:\ncmp {condition}, 0\nje end_while_label\n"
        except Exception as e:
            logging.error(f"Error parsing while loop: {e}")
            return ""

    def parse_for(self, line):
        """
        Parse a Kala for loop.
        Syntax: for var in range(start, end) { ... }
        """
        try:
            _, rest = line.split("for ", 1)
            var, range_part = rest.split("in range(", 1)
            start, end = range_part.strip("){} ").split(",")
            var = var.strip()
            self.block_stack.append("for")
            return (f"mov {start}, %{var}\nfor_label:\ncmp %{var}, {end}\n"
                    f"jge end_for_label\n")
        except Exception as e:
            logging.error(f"Error parsing for loop: {e}")
            return ""

    def parse_block_close(self):
        """
        Handle closing of a block (}).
        """
        if not self.block_stack:
            logging.error("Mismatched block closure detected.")
            return ""

        block_type = self.block_stack.pop()
        if block_type.startswith("class_"):
            return f"; End of class {block_type.split('_', 1)[1]}\n"
        elif block_type.startswith("method_"):
            return f"; End of method {block_type.split('_', 1)[1]}\n"
        elif block_type == "if":
            return "else_label:\n"
        elif block_type == "while":
            return "jmp while_label\nend_while_label:\n"
        elif block_type == "for":
            return "jmp for_label\nend_for_label:\n"

        return ""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kala Compiler")
    parser.add_argument("input_file", help="Path to the .kala source file")
    parser.add_argument("output_file", help="Path to the output .s file")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    compiler = KalaCompiler()
    if compiler.compile(args.input_file, args.output_file):
        logging.info("Compilation completed successfully.")
    else:
        logging.error("Compilation failed.")
        sys.exit(1)