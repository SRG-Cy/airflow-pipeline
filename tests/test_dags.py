import ast
import os

DAG_DIR = os.path.join(os.path.dirname(__file__), '..', 'dags')

def test_dag_syntax():
    for filename in os.listdir(DAG_DIR):
        if filename.endswith('.py'):
            filepath = os.path.join(DAG_DIR, filename)
            with open(filepath) as f:
                source = f.read()
            ast.parse(source)  # raises SyntaxError if invalid

def test_dag_file_exists():
    dag_files = [f for f in os.listdir(DAG_DIR) if f.endswith('.py')]
    assert len(dag_files) > 0, "No DAG files found!"