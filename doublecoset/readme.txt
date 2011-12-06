To get GraphViz visualisation:

write a program called mygraph.py which ends with a line like
	print(str(mygraph))

run
	mygraph.py > mygraph.gv
	neato -Tpng mygraph.gv > mygraph.png

your image will be in mygraph.png
