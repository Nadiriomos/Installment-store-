from src.my_project.module1 import greet

def test_greet(capsys):
    greet("Nadir")
    captured = capsys.readouterr()
    assert "Hello, Nadir!" in captured.out
