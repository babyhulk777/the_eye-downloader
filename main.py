import time

from eye import *

ti = time.perf_counter()

g = GetPage('the-eye.eu/public/Books/Gutenberg.org/')
g.download()

tf = time.perf_counter() - ti

print(tf)
