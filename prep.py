import ast
import os


def modify_function(filename, class_name, function_name, new_code):
    with open(filename, 'r') as file:
        tree = ast.parse(file.read())

    print(tree.body)
    # Find the specified class in the AST
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            # Find the specified function inside the class and modify its body
            for body_node in node.body:
                if isinstance(body_node, ast.FunctionDef) and body_node.name == function_name:
                    body_node.body = ast.parse(new_code).body

    # Generate modified code from the AST
    modified_code = ast.unparse(tree)

    # Write the modified code back to the file
    with open(filename, 'w') as file:
        file.write(modified_code)


def prep():
    os.environ["COQUI_TOS_AGREED"] = "1"
    modify_function("/usr/local/lib64/python3.9/site-packages/TTS/utils/manage.py",
                    "ModelManager",
                    "ask_tos",
                    "return True")
    print("--PREP DONE--")


prep()
