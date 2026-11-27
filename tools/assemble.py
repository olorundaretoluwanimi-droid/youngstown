# index.html = the series engine base (research/base.js.html, from the Rochester page, minus the film strip) + tools/court.js (this episode)
import re, os
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = open(os.path.join(D, 'tools/base.html'), encoding='utf-8').read()
open(os.path.join(D, 'index.html'), 'w', encoding='utf-8').write(b + open(os.path.join(D, 'tools/court.js'), encoding='utf-8').read())
