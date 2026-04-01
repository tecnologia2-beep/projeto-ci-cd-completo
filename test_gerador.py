import pytest
from app import gerar_codigo


def test_grupo_existente(monkeypatch):

    def mock_conectar():
        class MockCursor:
            def execute(self, query, params):
                pass

            def fetchone(self):
                return (3,)

            def close(self):
                pass

        class MockConn:
            def cursor(self):
                return MockCursor()

            def close(self):
                pass

        return MockConn()

    monkeypatch.setattr("app.conectar", mock_conectar)

    codigo, sec = gerar_codigo("C", "A", "BR")

    assert sec == 4
    assert codigo == "BRC0004A"


def test_grupo_novo(monkeypatch):

    def mock_conectar():
        class MockCursor:
            def execute(self, query, params):
                pass

            def fetchone(self):
                return (None,)

            def close(self):
                pass

        class MockConn:
            def cursor(self):
                return MockCursor()

            def close(self):
                pass

        return MockConn()

    monkeypatch.setattr("app.conectar", mock_conectar)

    codigo, sec = gerar_codigo("Z", "A", "BR")

    assert sec == 1
    assert codigo == "BRZ0001A"


def test_zerofill(monkeypatch):

    def mock_conectar():
        class MockCursor:
            def execute(self, query, params):
                pass

            def fetchone(self):
                return (9,)

            def close(self):
                pass

        class MockConn:
            def cursor(self):
                return MockCursor()

            def close(self):
                pass

        return MockConn()

    monkeypatch.setattr("app.conectar", mock_conectar)

    codigo, sec = gerar_codigo("C", "A", "BR")

    assert codigo == "BRC0010A"


def test_pais_invalido():
    with pytest.raises(ValueError):
        gerar_codigo("C", "A", "BRA")


def test_parametros_vazios():
    with pytest.raises(ValueError):
        gerar_codigo("", "A", "BR")
