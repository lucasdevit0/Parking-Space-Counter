import cv2 as cv
import pickle as pkl

#Picks upper left corner and lower right corner of parking section
'''Picks upper left corner and lower right corner of parking section with mouse-click event
   Output: section_pos.pkl file that stores (x,y) coordinates of picked corners
'''

video = 'parkinglot_timelapse.mp4'

# Get single video frame and save as jpg
def get_frame(video):
    
    cap = cv.VideoCapture(video)
    
    # Fastforward 30 frames (initial frames black)
    cap.set(cv.CAP_PROP_POS_FRAMES, 30) 
    
    ret,frame = cap.read()
    
    # save frame
    cv.imwrite('parkinglot_frame.jpg',frame)
    
    cap.release()
    cv.destroyAllWindows()
    

try:
    with open('section_pos.pkl', 'rb') as f: #unpickling
        sec_pos = pkl.load(f)
except:
    sec_pos = []
    

#Click events to store or delete section coordinates
def section_constructor(events, x, y,flags,params):
    
    if events == cv.EVENT_LBUTTONDOWN:   #add
        sec_pos.append((x,y))
        
    if events == cv.EVENT_RBUTTONDOWN:   # delete   
        sec_pos.pop()
                
    with open('section_pos.pkl', 'wb') as f:  #pickling
        pkl.dump(sec_pos, f)
        
        
while True:
    
    img = cv.imread('parkinglot_frame.jpg')
    
    for pos in sec_pos:
        cv.rectangle(img,pos,(pos[0]+10,pos[1]+10),(0,0,255),2)
        
    if cv.waitKey(25) & 0xFF == ord('q'):
            break
    
    cv.namedWindow('frame', cv.WINDOW_NORMAL)
    cv.setWindowProperty('frame', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    
    cv.imshow('img',img)
    cv.setMouseCallback('img',section_constructor)
    cv.waitKey(3)
