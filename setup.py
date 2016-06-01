#!/usr/bin/env/python

from distutils.core import setup

setup(name='SketchFeatureExtractor',
		version='0.1',
		description='Sketch feature extraction package',
		author='Ozan Can Altiok, Kurmanbek Kaiyrbekov',
		author_email='oaltiok15@ku.edu.tr,kkaiyrbekov15@ku.edu.tr',
		url='https://github.com/ozymaxx/sketchfeatureextractor',
		packages=['sketchfe'],
		packages_dir={'sketchfe','src/sketchfe'},
		requires=['numpy','matplotlib','scipy'],
	)
