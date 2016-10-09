import pyocr
import pyocr.builders
from PIL import Image
import cv2
import matplotlib.pyplot as plt

RED, GREEN, BLUE = (255,0,0), (0,255,0), (0,0,255)

img = cv2.imread('test.png')
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert to grayscale
gray_img = cv2.GaussianBlur(gray_img,(3,3),0) # denoise image

H, W = gray_img.shape # (3600, 2454)




def draw_boxes(boxes, color=RED, thickness=2, img=img, fontscale=1, filename=None, show=False):
    _img = img.copy()
    for i,lnbox in enumerate(boxes): 
        p1,p2 = lnbox.position
        cv2.rectangle(_img, p1, p2, color, thickness)
        cv2.putText(_img, str(i), p1, cv2.FONT_HERSHEY_DUPLEX, fontscale, color, thickness)
    if filename != None:
        '''cvtColor to make saved cv2 and matplotlib conform, 
        see: http://www.pyimagesearch.com/2014/11/03/display-matplotlib-rgb-image/'''
        cv2.imwrite(filename, cv2.cvtColor(_img, cv2.COLOR_RGB2BGR) )
    if show:
        plt.figure(figsize=(15,30))
        plt.imshow(_img)
    return _img

def overlap(rect1, rect2, vmargin=15, hmargin=15):
    'testing if 2 rectangles overlap (up to a V/H margin)'
    (l1,b1),(r1,t1) = rect1
    assert l1<=r1 and b1<=t1 
    (l2,b2),(r2,t2) = rect2
    assert l2<=r2 and b2<=t2 
    if r1+hmargin<l2 or r2+hmargin<l1: return False
    if t1+vmargin<b2 or t2+vmargin<b1: return False
    return True

class ParagraphBox(object):
    '''box for paragraph segmentation, with similar interface as LineBox and TextBox in `pyocr` module '''
    def __init__(self, boxes, box_indices = None): # here the boxes could be wordboxes OR lineboxes
        self._boxes = boxes
        self.box_indices = box_indices # add this for debugging, should be removed afterwards...
        _rects = [box.position for box in self._boxes]
        l = min(rect[0][0] for rect in _rects)
        b = min(rect[0][1] for rect in _rects)
        r = max(rect[1][0] for rect in _rects)
        t = max(rect[1][1] for rect in _rects)
        self.position =  ((l,b), (r,t))
        
    def __get_content(self):
        txt = u' '.join([_box.content for _box in self._boxes])
        return txt
    content = property(__get_content)
    
    def is_main_content(self):
        '''returns if this paragraph is in main content or rather is in tilte/header/footer/etc.
        ATTENTION: here used a dirty way to test, need to further tune!!
        logic: 
        if the content is long enough (>200 chars), and width is between W/3 and W/2, then say the paragraph is in main content.
        '''
        ((l,b), (r,t)) = self.position
        width = abs(r-l)
        return len(txt)>200 and W/3.0 <= width <= W/2.0 

def get_paraboxes(boxes, mode='last', vmargin=15, hmargin=15, show=False, verbose=False, **kwargs):
    '''
    merging boxes to form paragraph boxes, 
    supposes boxes are well ordered (the output of pyocr is already quite well-ordered). 
    
    there are 2 modes to choose: 
    * 'last': stops growing paragraph when current box doesn't overlap with last box in buffer
    * 'any': stops growiing when current box doesn't overlap with any box in buffer
    '''
    paraboxes = [] # list of ParagraphBox objs
    buffer_indices = [] # list of wdbox/lnbox indices as buffer

    def add_para():
        _boxes = [boxes[k] for k in buffer_indices]
        parabox = ParagraphBox(_boxes, buffer_indices)
        if verbose:
            print '-----found para-----', len(paraboxes)
            print parabox.box_indices
            print parabox.content
        paraboxes.append(parabox)


    for i,box in enumerate(boxes):
        ctt = box.content.strip()
        if len(ctt) == 0: continue # skip too short contents --> these are probably errors
#         if len(ctt)==1 and not(ctt.isalpha() or ctt.isdigit()): continue

        if len(buffer_indices)==0:
            buffer_indices.append(i)
            continue

        cur_rect = box.position

        if mode=='last':
            stop_flag = overlap(cur_rect, boxes[buffer_indices[-1]].position, vmargin, hmargin)
        elif mode=='any':
            _rects = [boxes[k].position for k in buffer_indices] # all rects in (partial) paragraph
            stop_flag = any( overlap(rect, cur_rect, vmargin, hmargin) for rect in _rects )
        else:
            raise Error("invalid mode: %s, possible choices are: 'last', 'any'. " % mode)
        if stop_flag:
            buffer_indices.append(i)
        else: 
            add_para()
            buffer_indices = [i]
    add_para()
    
    if show:
        _img = draw_boxes(paraboxes,color=BLUE, thickness=5, fontscale=2)
        _img = draw_boxes(boxes, img=_img, color=RED, thickness=2, fontscale=1,**kwargs)
        plt.figure(figsize=(15,30))
        plt.imshow(_img)
        
    return paraboxes



if __name__ == '__main__':
    
    tools = pyocr.get_available_tools()
    if len(tools)==0: 
        raise Error('no ocr software is installed, please install tesseract!')
    tool = tools[0]
    
    print 'processing image with tesseract...', 
    wordboxes = tool.image_to_string(
        Image.fromarray(gray_img), # convert to the PIL format that pyocr accepts as input,
        lang='deu+fra',
        builder=pyocr.builders.WordBoxBuilder())
    print 'done'
    
    print 'creating paragraph boxes...',
    my_lineboxes = get_paraboxes(wordboxes, mode='last', hmargin=45,)
    _img = draw_boxes(my_lineboxes, show=False, filename=None)
    paraboxes = get_paraboxes(my_lineboxes, mode='any', vmargin=20)
    paraboxes = filter(lambda bx: len(bx.content)>1, paraboxes) # filter out paragraph boxes with content length<=1
    _img = draw_boxes(paraboxes, show=False, color=BLUE, filename='paraboxes.jpg')
    print 'done (paragraph seperation results are stored in paraboxes.jpg)'
    
    print ' ===============text paragraphs found in image==============='
    names = []
    text = []
    for pbox in paraboxes:
        txt = pbox.content
        text.append(txt)
        if pbox.is_main_content() and ':' in txt[:100]:
            names.append( txt.split(':')[0] )
        print '------------'
        print txt

    print '===============participant names==============='
    for nm in names: 
        print nm, ';', 
