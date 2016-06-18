#Sketch Feature Extractor Python 2.7 Implementation
We implemented the sketch feature extraction mechanism mentioned in the following paper:
[http://rationale.csail.mit.edu/publications/Ouyang2009IJCAI.pdf](http://rationale.csail.mit.edu/publications/Ouyang2009IJCAI.pdf)

##Usage
* Download the files
* Run ```python setup.py build``` to build the code
* Run ```python setup.py install``` to install the module (this action may require sudo privileges)
* You can try running the following code to see if it is working:

```
from sketchfe import FeatureExtractor
idm = FeatureExtractor.IDMFeatureExtractor()
idm.extractimage_test()
```

##The format of the symbol sketches
A sketch is defined as a set of strokes including ink points. You can keep the sketches in 3 different formats, described below.

The following examples refer to the same sketch.

* JSON
```
{"id":"asdasd",
 "strokes":
	[{"id":"1","points":[{"pid":"qwe","time":4.6,"x":1,"y":9},{"pid":"aty","time":8,"x":6,"y":5}]},
	{"id":"21","points":[{"pid":"uio","time":9,"x":10.2,"y":44.4},{"pid":"asd","time":12,"x":3,"y":77},{"pid":"cvb","time":13,"x":5,"y":7}]
	}]
}
```

* XML
```
<sketch id="1">
	<point id="1" time="4.6" x="1" y="9" />
	<point id="2" time="8" x="6" y="5" />
	<point id="3" time="9" x="10.2" y="44.4" />
	<point id="4" time="12" x="3" y="77" />
	<point id="5" time="13" x="5" y="7" />
	<stroke id="1">
		<arg type="point">1</arg>
		<arg type="point">2</arg>
	</stroke>
	<stroke id="2">
		<arg type="point">3</arg>
		<arg type="point">4</arg>
		<arg type="point">5</arg>
	</stroke>
</sketch>
```

* Points as table
```
    1\t9\t0\t4.6\n6\t5\t0\t8\n10.2\t44.4\t1\t9\n3\t77\t1\t12\n5\t7\t1\t13
```

There will be more feature extraction methods in the upcoming versions.

##Loading sketches from files
This library has built-in functions to load sketches from XML, JSON and text files containing points as table (see the previous section for the content organization of these types). Some examples regarding the usage of these functions are given below.

* Loading a sketch from an XML file
```
from sketchfe import shapecreator
filename = "sketch.xml" #the name of the sketch file
with open(filename,'rb') as f:
     filecontent = f.read()
     loadedSketch = shapecreator.buildSketch(filecontent,'xml')
```

* Loading a sketch from a JSON file
```
from sketchfe import shapecreator
filename = "sketch.json" #the name of the sketch file
with open(filename,'rb') as f:
     filecontent = f.read()
     loadedSketch = shapecreator.buildSketch(filecontent,'json')
```

* Loading a sketch from a points table text file
```
from sketchfe import shapecreator
filename = "sketch.txt" #the name of the sketch file
with open(filename,'rb') as f:
     filecontent = f.read()
     loadedSketch = shapecreator.buildSketch(filecontent,'school')
```

##Extracting Features
By creating an instance of `IDMFeatureExtractor` , which is the sub-class of `FeatureExtractor`, you can extract features of a sketch represented as an instance of `Sketch` class. The following code snippet basically extracts feature of a `Sketch` instance `sk`:

```
import sketchfe.FeatureExtractor.IDMFeatureExtractor
featextractor = IDMFeatureExtractor()
features = featextractor.extract(sk) # features includes the feat. representation as an array
```

###Contact
* oaltiok15@ku.edu.tr - Ozan Can Altıok
* kkaiyrbekov15@ku.edu.tr - Kurmanbek Kaiyrbekov

http://iui.ku.edu.tr - Koç University Intelligent User Interfaces Laboratory
