# conftest.py — marks backend/ as pytest's root directory.
# Its mere presence here (even empty) causes pytest to add this folder
# to sys.path during test collection, which is what makes
# `from app.main import app` resolvable from inside tests/.