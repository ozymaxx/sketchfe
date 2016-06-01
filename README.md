#Sketch Feature Extractor Python Implementation
We implemented the sketch feature extraction mechanism mentioned in the following paper:
[http://rationale.csail.mit.edu/publications/Ouyang2009IJCAI.pdf](http://rationale.csail.mit.edu/publications/Ouyang2009IJCAI.pdf)

##Usage
* Download the files
* Run "python setup.py install"
* You can try running the following code to see if it is working:

```
import FeatureExtractor
idm = FeatureExtractor.IDMFeatureExtractor()
idm.extractimage_test()
```

##The format of the symbol sketches
A sketch is defined as a set of strokes including ink points. You can keep the sektches in 3 different formats, described below.

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

* Points as rows

    1\t9\t0\t4.6\n6\t5\t0\t8\n10.2\t44.4\t1\t9\n3\t77\t1\t12\n5\t7\t1\t13


There will be more feature extraction methods in the following versions.