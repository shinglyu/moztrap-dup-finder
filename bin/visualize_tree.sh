dot -Tpdf "$1" -o "$1.pdf"
evince "$1.pdf"
