# -*- coding: utf-8 -*-
"""
@author: ozan & kurmanbek
oaltiok15@ku.edu.tr
kkaiyrbekov15@ku.edu.tr
"""

import xml.etree.ElementTree as ET
import json
import Point
import Stroke
import Sketch

# returns sketch from json string
def jsonshape(string):
    # parse json string
    shapejson = json.loads(string)
    
    # init an empty sketch
    sketch = Sketch.Sketch(sketch_id=shapejson['id'],strokes=[])	
    
    # for each stroke
    for stroke in shapejson['strokes']:
        # init an empty stroke
        st = Stroke.Stroke(stroke['id'])
        
        # for each point in a stroke
        for point in stroke['points']:
            # add the point to the stroke
            st.addPoint( Point.Point(point['pid'], float(point['time']), float(point['x']), float(point['y']) ) )
            
        # add the stroke to the sketch
        sketch.addStrokes(st)
    
    return sketch

# returns sketch from high school students' sketch data
def loadfromschooldata(string):
    # init an empty sketch
    sketch = Sketch.Sketch(sketch_id='shape',strokes=[])
    
    # find lines
    lines = string.splitlines()
    laststroke = -1
    pointid = 0
    strokelist = []
    
    # for each line
    for line in lines:
        # obtain point parameters
        numbers = line.split('\t')
        
        # if a new stroke is found
        if int(numbers[2]) > laststroke:
            # init a new empty stroke
            laststroke = laststroke + 1
            strokelist.append( Stroke.Stroke( str(laststroke) ) )
            
        # add the point to its corresponding stroke
        strokelist[laststroke].addPoint( Point.Point('p'+str(pointid), float(numbers[3]), float(numbers[0]), float(numbers[1]) ) )
        pointid = pointid + 1
        
    # finally add the strokes to the sketch
    for stroke in strokelist:
        sketch.addStrokes(stroke)
        
    return sketch
    
def extractFromXML( string ):
    root = ET.fromstring( string )
    points = getPoints(root)
    strokes = getStrokes(points, root)
    sketch = Sketch.Sketch( root.get('id'), strokes)
    return sketch

#Gets all points from an XML file  
def getPoints( root ):
    points = dict()
    #for each point insert point data to dictionary
    for child in root:
        if child.tag == 'point':
            pid = child.get('id')
            x = child.get('x')
            y = child.get('y')
            t = child.get('time')
            points[pid] = Point.Point( pid, float(t), float(x), float(y) )
    
    return points

#Gets all strokes with corresponding points from XML file
def getStrokes(points, root):
    strokes = []
    #find all stroke elements
    for st in root.findall('stroke'):
        stroke_id = st.get('id')
        stroke = Stroke.Stroke( stroke_id )
        #for each stroke get point id's
        for pnt in st.findall('arg'):
            pid = pnt.text
            stroke.addPoint( points[pid] )
        strokes.append( stroke )
        
    return strokes
    
def buildSketch(inputtype,content):
    # decide on the input format according to the value of inputtype
    if inputtype == 'json':
        return jsonshape(content)
    elif inputtype == 'xml':
        return extractFromXML(content)
    elif inputtype == 'school':
        return loadfromschooldata(content)

def test():
    # define example strings having the same sketch
    str1 = '{"id":"asdasd","strokes":[{"id":"1","points":[{"pid":"qwe","time":4.6,"x":1,"y":9},{"pid":"aty","time":8,"x":6,"y":5}]},{"id":"21","points":[{"pid":"uio","time":9,"x":10.2,"y":44.4},{"pid":"asd","time":12,"x":3,"y":77},{"pid":"cvb","time":13,"x":5,"y":7}]}]}'
    str2 = '1\t9\t0\t4.6\n6\t5\t0\t8\n10.2\t44.4\t1\t9\n3\t77\t1\t12\n5\t7\t1\t13'
    str3 = '''<sketch id="082c633c-8c97-4a91-9b0a-c0ef7a96a394"><point id="166dc1f4-39c7-4b19-b43a-e594b5f18b65" time="1215472858134" x="355.6561533139875" y="93.95012710811879"/><point id="17fb8702-2b57-430a-99fb-9fcd68c2dbbf" time="1215472858165" x="355.1377273407388" y="95.5054050278649"/><point id="223e6103-51e7-4caa-9cf7-50fe86d79313" time="1215472858165" x="355.1377273407388" y="100.68966476035189"/><point id="82245cd6-ab44-49aa-adec-dec7727f0ee2" time="1215472858181" x="355.6561533139875" y="106.91077643933627"/><point id="167e3da7-ee8c-4730-8e0b-a8c67780cdd1" time="1215472858181" x="356.1745792872362" y="114.16874006481808"/><point id="6652cafd-3bf5-460b-9ed3-850706a39dd8" time="1215472858196" x="356.6930052604849" y="121.42670369029986"/><point id="a5dfe37f-689a-4fee-a888-e5d92804baa3" time="1215472858196" x="357.7298572069823" y="129.20309328903036"/><point id="0ab1c2ed-1fbd-4b43-a744-770fd13b7af5" time="1215472858212" x="358.248283180231" y="139.57161275400435"/><point id="a0661c27-76e6-446d-80c9-573379c5f43b" time="1215472858212" x="359.2851351267284" y="149.94013221897833"/><point id="8961134c-cf59-4c87-8d4d-ab20d23999b8" time="1215472858228" x="359.80356109997706" y="160.30865168395232"/><point id="a0db68a1-acfe-4cd2-96c7-b9336bc2aa46" time="1215472858228" x="359.80356109997706" y="171.71402309542373"/><point id="5aa1e79f-5036-4ae8-9317-2b6ba251ef57" time="1215472858243" x="359.80356109997706" y="178.97198672090553"/><point id="d672850c-97eb-4131-927e-ad5e04c7dbf1" time="1215472858243" x="359.80356109997706" y="186.748376319636"/><point id="57c70801-b79d-47d8-9aad-c719dd9876dc" time="1215472858259" x="359.80356109997706" y="193.4879139718691"/><point id="30d9cf19-2411-4eab-817b-6f8f24a81cb0" time="1215472858259" x="359.80356109997706" y="199.19059967760478"/><point id="b592860d-0a47-4d88-97c5-d3b9175d30bf" time="1215472858275" x="359.80356109997706" y="205.9301373298379"/><point id="f4088bd5-d4d9-452d-96aa-606c44df5f88" time="1215472858275" x="359.80356109997706" y="211.6328230355736"/><point id="b2751b0c-8ead-47ab-95d9-85e80c375ecd" time="1215472858290" x="359.80356109997706" y="215.78023082156318"/><point id="af5da362-108a-4a9f-a835-97f254f5364f" time="1215472858290" x="359.80356109997706" y="218.8907866610554"/><point id="7a200101-1552-416c-a0c7-2bdd10737fd9" time="1215472858306" x="359.80356109997706" y="222.00134250054757"/><point id="8dd17341-26ce-47e3-ab42-8442dd962d6d" time="1215472858306" x="359.80356109997706" y="224.07504639354238"/><point id="eebd4f33-5a40-414c-95d7-70e7b6f0fe6a" time="1215472858321" x="359.80356109997706" y="225.11189834003977"/><point id="39fe817c-87f3-40ec-915b-2ba181186b8d" time="1215472858337" x="359.80356109997706" y="226.14875028653717"/><point id="ef251b77-182e-48db-916a-050177bc5112" time="1215472859446" x="357.7298572069823" y="93.95012710811879"/><point id="b9675966-d629-449f-8ee8-4de507494414" time="1215472859556" x="360.8404130464745" y="94.46855308136749"/><point id="9e450f67-2596-478b-a209-99e24b4db477" time="1215472859571" x="366.5430987522102" y="94.98697905461619"/><point id="64f328c9-9dce-4259-8034-e0b96fa4a733" time="1215472859571" x="373.2826364044433" y="94.98697905461619"/><point id="d880da00-b2f3-49cb-8715-40e56c801770" time="1215472859587" x="380.5406000299251" y="94.98697905461619"/><point id="234542b9-9e39-4f93-aeeb-ada1205c34f3" time="1215472859587" x="387.28013768215817" y="94.98697905461619"/><point id="0887fa1c-e3d8-4a79-98d1-8d656d9805b9" time="1215472859603" x="394.53810130764" y="95.5054050278649"/><point id="94fcefc4-6a44-46c6-b46c-d5fce1b1c58e" time="1215472859603" x="404.38819479936524" y="95.5054050278649"/><point id="e9204bc1-b605-450f-a889-e3892b3b4738" time="1215472859618" x="411.64615842484704" y="96.02383100111359"/><point id="1e84ef56-99bc-4e00-834c-c655eb5972eb" time="1215472859618" x="419.94097399682624" y="96.02383100111359"/><point id="9225a4f2-e2bd-46aa-970f-36e9dca2b5e0" time="1215472859634" x="427.19893762230805" y="96.02383100111359"/><point id="de8eb720-697e-4ce3-9fdc-4f96ac5b2bc0" time="1215472859634" x="432.383197354795" y="96.02383100111359"/><point id="0d9c3eeb-a2fc-4380-b2f0-aa6588eeacfe" time="1215472859650" x="437.56745708728204" y="96.02383100111359"/><point id="c3d12078-b457-4415-9660-e9c4e22762f1" time="1215472859650" x="440.1595869535255" y="96.02383100111359"/><point id="63f5b3ff-5022-4292-a051-d44cb78bcccb" time="1215472859665" x="443.2701427930177" y="96.02383100111359"/><point id="596f9934-9956-4a72-892f-0e81bc48a701" time="1215472859665" x="444.8254207127638" y="96.02383100111359"/><point id="ca255b77-40d4-468f-82fb-87ef806c9fe3" time="1215472859978" x="443.7885687662664" y="96.02383100111359"/><point id="033469ae-8aa1-4100-9ce4-008291f34c19" time="1215472860400" x="446.89912460575863" y="98.61596086735709"/><point id="2370f924-34d1-4801-9898-be135d970eb3" time="1215472860493" x="447.4175505790073" y="99.6528128138545"/><point id="ab16dd47-caa8-45ce-a21c-56f6ed2281e3" time="1215472860493" x="447.4175505790073" y="102.76336865334667"/><point id="179efede-ca85-483b-b407-a19492edd5d4" time="1215472860509" x="447.4175505790073" y="105.87392449283888"/><point id="0f6f1097-cc04-4a4c-92a6-09e3ff38c75a" time="1215472860509" x="447.4175505790073" y="108.46605435908238"/><point id="d8d5a3a1-e9a6-4e37-8ecb-25e99734c149" time="1215472860525" x="447.4175505790073" y="111.05818422532587"/><point id="943226a5-bc1e-4a76-82ff-e6966f9e3998" time="1215472860525" x="447.4175505790073" y="114.16874006481808"/><point id="7ce83d0d-ec03-4922-85ee-043ccc4392ba" time="1215472860540" x="447.4175505790073" y="116.76086993106158"/><point id="68a3a03f-6fd4-4cb6-8e0c-812f05a9a5a2" time="1215472860540" x="447.4175505790073" y="119.87142577055377"/><point id="cd36f3d9-39a0-4242-a23d-9b0daaacc4fe" time="1215472860556" x="447.4175505790073" y="122.46355563679727"/><point id="9be20fb7-968c-473c-a3ff-5ef26504adc5" time="1215472860556" x="447.4175505790073" y="123.50040758329466"/><point id="1aabe697-6a70-4b94-afca-cacac6553c26" time="1215472860571" x="447.4175505790073" y="124.53725952979207"/><point id="36740c61-5540-49c5-817f-b7b5b1b9b2a2" time="1215472861681" x="362.9141169394693" y="143.20059456674525"/><point id="d6fab79d-df49-4b95-83e1-ab6e88636db3" time="1215472861806" x="363.9509688859667" y="143.20059456674525"/><point id="b4b0c160-0127-41fb-81f1-a9c10718c325" time="1215472861821" x="364.9878208324641" y="142.68216859349656"/><point id="35923212-4586-46a5-850f-1a6b36bb8af8" time="1215472861837" x="366.0246727789615" y="142.16374262024786"/><point id="46db8bcc-3fff-40e8-8172-23385318186e" time="1215472861837" x="367.06152472545887" y="141.64531664699916"/><point id="9946c32c-f833-4c39-b727-b3ca9fe2a200" time="1215472861853" x="369.13522861845365" y="141.64531664699916"/><point id="98abdc10-0dfe-4d99-a94b-522ea0d8ebcc" time="1215472861853" x="371.72735848469716" y="141.64531664699916"/><point id="b8663492-5955-42d2-83bd-0839b616e870" time="1215472861868" x="375.8747662706868" y="140.60846470050174"/><point id="50bee1db-adf5-49ef-b56a-c5e5bf2599cf" time="1215472861868" x="380.02217405667636" y="140.60846470050174"/><point id="6d3c052a-1e9f-4003-92c2-9b76462596ed" time="1215472861884" x="384.169581842666" y="140.60846470050174"/><point id="f8138e94-8426-4b82-8c47-ac4bfd84a6f2" time="1215472861884" x="388.31698962865556" y="140.60846470050174"/><point id="cc4149c5-84be-4b40-9fe6-d60b2446a2a9" time="1215472861900" x="393.5012493611425" y="140.60846470050174"/><point id="d55a4e1c-1e17-4b49-97f1-21276052d78c" time="1215472861900" x="398.68550909362955" y="140.60846470050174"/><point id="82693e1c-f26d-48aa-9c30-215b92c549ef" time="1215472861915" x="403.35134285286784" y="140.60846470050174"/><point id="75ca0d0e-3f61-4390-8bab-fa4ab7ab4f15" time="1215472861915" x="408.53560258535487" y="140.60846470050174"/><point id="be7bb772-3361-488e-a6a7-9fb7e9078f8d" time="1215472861931" x="413.20143634459316" y="140.60846470050174"/><point id="590e1b4a-03e7-442f-a53d-d769f53b1c08" time="1215472861931" x="418.3856960770801" y="141.12689067375044"/><point id="8b730284-068b-4690-b4a9-79e50df91fda" time="1215472861946" x="422.53310386306975" y="141.12689067375044"/><point id="502e8c88-ed15-459d-8443-8db4ea986d42" time="1215472861946" x="426.6805116490593" y="141.12689067375044"/><point id="6bed6954-0590-4741-afba-300f283fc1b4" time="1215472861962" x="429.7910674885515" y="141.12689067375044"/><point id="ad72e4cf-c884-482b-ba73-6433f7eea0a8" time="1215472861962" x="433.93847527454113" y="141.12689067375044"/><point id="ff035dd0-3b97-43e3-92e6-ba95815e8d22" time="1215472861978" x="438.0858830605307" y="141.12689067375044"/><point id="71d3a753-317e-4f04-93e5-71bbf0d30934" time="1215472861978" x="441.19643890002294" y="141.12689067375044"/><point id="5c36ef50-1f97-49fb-9f3b-d04fcb5ac95b" time="1215472861993" x="442.751716819769" y="141.12689067375044"/><point id="260fffc5-0fff-4518-b6b9-c96ce441a05d" time="1215472861993" x="444.8254207127638" y="141.12689067375044"/><point id="0bdd6b80-2a11-4e14-ae99-151b7ddac51e" time="1215472862009" x="446.3806986325099" y="141.12689067375044"/><point id="6accd807-a578-4594-8113-ed57bbdd2c5c" time="1215472862009" x="448.4544025255047" y="141.12689067375044"/><point id="06b612be-f69c-4dde-859e-b6d880bf65c3" time="1215472862025" x="450.52810641849953" y="141.12689067375044"/><point id="04f23655-7f68-4b1e-91b5-41fe6a81d69b" time="1215472862025" x="452.0833843382456" y="141.12689067375044"/><point id="a2d248f0-317b-4565-b73c-dd5af475bf9e" time="1215472862040" x="453.120236284743" y="141.12689067375044"/><point id="6bb21c90-d05c-4f1c-bc9e-1da3532f4d63" time="1215472862290" x="452.0833843382456" y="141.12689067375044"/><stroke id="65a28830-4053-4e35-878c-41e42d8004d9" visible="true"><arg type="point">166dc1f4-39c7-4b19-b43a-e594b5f18b65</arg><arg type="point">17fb8702-2b57-430a-99fb-9fcd68c2dbbf</arg><arg type="point">223e6103-51e7-4caa-9cf7-50fe86d79313</arg><arg type="point">82245cd6-ab44-49aa-adec-dec7727f0ee2</arg><arg type="point">167e3da7-ee8c-4730-8e0b-a8c67780cdd1</arg><arg type="point">6652cafd-3bf5-460b-9ed3-850706a39dd8</arg><arg type="point">a5dfe37f-689a-4fee-a888-e5d92804baa3</arg><arg type="point">0ab1c2ed-1fbd-4b43-a744-770fd13b7af5</arg><arg type="point">a0661c27-76e6-446d-80c9-573379c5f43b</arg><arg type="point">8961134c-cf59-4c87-8d4d-ab20d23999b8</arg><arg type="point">a0db68a1-acfe-4cd2-96c7-b9336bc2aa46</arg><arg type="point">5aa1e79f-5036-4ae8-9317-2b6ba251ef57</arg><arg type="point">d672850c-97eb-4131-927e-ad5e04c7dbf1</arg><arg type="point">57c70801-b79d-47d8-9aad-c719dd9876dc</arg><arg type="point">30d9cf19-2411-4eab-817b-6f8f24a81cb0</arg><arg type="point">b592860d-0a47-4d88-97c5-d3b9175d30bf</arg><arg type="point">f4088bd5-d4d9-452d-96aa-606c44df5f88</arg><arg type="point">b2751b0c-8ead-47ab-95d9-85e80c375ecd</arg><arg type="point">af5da362-108a-4a9f-a835-97f254f5364f</arg><arg type="point">7a200101-1552-416c-a0c7-2bdd10737fd9</arg><arg type="point">8dd17341-26ce-47e3-ab42-8442dd962d6d</arg><arg type="point">eebd4f33-5a40-414c-95d7-70e7b6f0fe6a</arg><arg type="point">39fe817c-87f3-40ec-915b-2ba181186b8d</arg></stroke><stroke id="74f765d4-806f-48d1-bdab-c47de35e09fb" visible="true"><arg type="point">ef251b77-182e-48db-916a-050177bc5112</arg><arg type="point">b9675966-d629-449f-8ee8-4de507494414</arg><arg type="point">9e450f67-2596-478b-a209-99e24b4db477</arg><arg type="point">64f328c9-9dce-4259-8034-e0b96fa4a733</arg><arg type="point">d880da00-b2f3-49cb-8715-40e56c801770</arg><arg type="point">234542b9-9e39-4f93-aeeb-ada1205c34f3</arg><arg type="point">0887fa1c-e3d8-4a79-98d1-8d656d9805b9</arg><arg type="point">94fcefc4-6a44-46c6-b46c-d5fce1b1c58e</arg><arg type="point">e9204bc1-b605-450f-a889-e3892b3b4738</arg><arg type="point">1e84ef56-99bc-4e00-834c-c655eb5972eb</arg><arg type="point">9225a4f2-e2bd-46aa-970f-36e9dca2b5e0</arg><arg type="point">de8eb720-697e-4ce3-9fdc-4f96ac5b2bc0</arg><arg type="point">0d9c3eeb-a2fc-4380-b2f0-aa6588eeacfe</arg><arg type="point">c3d12078-b457-4415-9660-e9c4e22762f1</arg><arg type="point">63f5b3ff-5022-4292-a051-d44cb78bcccb</arg><arg type="point">596f9934-9956-4a72-892f-0e81bc48a701</arg><arg type="point">ca255b77-40d4-468f-82fb-87ef806c9fe3</arg></stroke><stroke id="bb9063a8-f778-4004-bbc0-976a62a6d950" visible="true"><arg type="point">033469ae-8aa1-4100-9ce4-008291f34c19</arg><arg type="point">2370f924-34d1-4801-9898-be135d970eb3</arg><arg type="point">ab16dd47-caa8-45ce-a21c-56f6ed2281e3</arg><arg type="point">179efede-ca85-483b-b407-a19492edd5d4</arg><arg type="point">0f6f1097-cc04-4a4c-92a6-09e3ff38c75a</arg><arg type="point">d8d5a3a1-e9a6-4e37-8ecb-25e99734c149</arg><arg type="point">943226a5-bc1e-4a76-82ff-e6966f9e3998</arg><arg type="point">7ce83d0d-ec03-4922-85ee-043ccc4392ba</arg><arg type="point">68a3a03f-6fd4-4cb6-8e0c-812f05a9a5a2</arg><arg type="point">cd36f3d9-39a0-4242-a23d-9b0daaacc4fe</arg><arg type="point">9be20fb7-968c-473c-a3ff-5ef26504adc5</arg><arg type="point">1aabe697-6a70-4b94-afca-cacac6553c26</arg></stroke><stroke id="e650eac7-9f76-4b40-90c1-ba1f346613e1" visible="true"><arg type="point">36740c61-5540-49c5-817f-b7b5b1b9b2a2</arg><arg type="point">d6fab79d-df49-4b95-83e1-ab6e88636db3</arg><arg type="point">b4b0c160-0127-41fb-81f1-a9c10718c325</arg><arg type="point">35923212-4586-46a5-850f-1a6b36bb8af8</arg><arg type="point">46db8bcc-3fff-40e8-8172-23385318186e</arg><arg type="point">9946c32c-f833-4c39-b727-b3ca9fe2a200</arg><arg type="point">98abdc10-0dfe-4d99-a94b-522ea0d8ebcc</arg><arg type="point">b8663492-5955-42d2-83bd-0839b616e870</arg><arg type="point">50bee1db-adf5-49ef-b56a-c5e5bf2599cf</arg><arg type="point">6d3c052a-1e9f-4003-92c2-9b76462596ed</arg><arg type="point">f8138e94-8426-4b82-8c47-ac4bfd84a6f2</arg><arg type="point">cc4149c5-84be-4b40-9fe6-d60b2446a2a9</arg><arg type="point">d55a4e1c-1e17-4b49-97f1-21276052d78c</arg><arg type="point">82693e1c-f26d-48aa-9c30-215b92c549ef</arg><arg type="point">75ca0d0e-3f61-4390-8bab-fa4ab7ab4f15</arg><arg type="point">be7bb772-3361-488e-a6a7-9fb7e9078f8d</arg><arg type="point">590e1b4a-03e7-442f-a53d-d769f53b1c08</arg><arg type="point">8b730284-068b-4690-b4a9-79e50df91fda</arg><arg type="point">502e8c88-ed15-459d-8443-8db4ea986d42</arg><arg type="point">6bed6954-0590-4741-afba-300f283fc1b4</arg><arg type="point">ad72e4cf-c884-482b-ba73-6433f7eea0a8</arg><arg type="point">ff035dd0-3b97-43e3-92e6-ba95815e8d22</arg><arg type="point">71d3a753-317e-4f04-93e5-71bbf0d30934</arg><arg type="point">5c36ef50-1f97-49fb-9f3b-d04fcb5ac95b</arg><arg type="point">260fffc5-0fff-4518-b6b9-c96ce441a05d</arg><arg type="point">0bdd6b80-2a11-4e14-ae99-151b7ddac51e</arg><arg type="point">6accd807-a578-4594-8113-ed57bbdd2c5c</arg><arg type="point">06b612be-f69c-4dde-859e-b6d880bf65c3</arg><arg type="point">04f23655-7f68-4b1e-91b5-41fe6a81d69b</arg><arg type="point">a2d248f0-317b-4565-b73c-dd5af475bf9e</arg><arg type="point">6bb21c90-d05c-4f1c-bc9e-1da3532f4d63</arg></stroke></sketch>
'''
    
    # parse the strings & construct the sketch objects
    sketch1 = buildSketch('json',str1)
    sketch2 = buildSketch('school',str2)
    sketch3 = buildSketch('xml',str3)
    
    # show the sketches' content
    print('Sketch 1:')
    for stroke in sketch1.strokes:
        print('A stroke')
        for point in stroke.points:
            print(point.time, point.x, point.y)
            
    print
    
    print('Sketch 2:')
    for stroke in sketch2.strokes:
        print('A stroke')
        for point in stroke.points:
            print(point.time,point.x,point.y)
            
    print
            
    print('Sketch 3:')
    for stroke in sketch3.strokes:
        print('A stroke')
        for point in stroke.points:
            print(point.time,point.x,point.y)
            
    return sketch1,sketch2,sketch3
