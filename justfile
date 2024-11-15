install-deps:
    brew install graphviz
    export GRAPHVIZ_PREFIX=$(brew --prefix graphviz)
    export CFLAGS="-I$GRAPHVIZ_PREFIX/include"
    export LDFLAGS="-L$GRAPHVIZ_PREFIX/lib"

install:
    pip install -r requirements.txt

freeze:
    pip freeze > requirements.txt

run:
    python sodai.py
