import cv2 as cv
import pickle as pkl

'''Picks lower right corner of every parking spot with mouse-click event
   Output: spot_pos.pkl file that stores (x,y) coordinates of picked parking spots
'''

offset = 22             # parking rectangle spot offset
width = 45              # width of parking space
height = 20             # height of parking space

try:
    with open('spot_pos.pkl', 'rb') as f:
        spot_pos = pkl.load(f)
except:
    spot_pos = []

#Click events to store or delete spots coordinates
def spot_constructor(events, x, y,flags,params):
    
    if events == cv.EVENT_LBUTTONDOWN:   #add
        spot_pos.append((x,y))
        
    if events == cv.EVENT_RBUTTONDOWN:   # delete   
        
        for i, pos in enumerate(spot_pos):
            x1 = pos[0]
            y1 = pos[1] - offset
            if x1 < x < x1 + width and y1 < y < y1 + height:
                spot_pos.pop(i)
                
    with open('spot_pos.pkl', 'wb') as f:  #pickling
        pkl.dump(spot_pos, f)
        
while True:
    
    img = cv.imread('parking_img.png')

    for pos in spot_pos:
        cv.rectangle(img,pos,(pos[0]+width,pos[1]-height),(0,0,255),2)
    
    if cv.waitKey(25) & 0xFF == ord('q'):
            break
        
    cv.imshow('img',img)
    cv.setMouseCallback('img',spot_constructor)
    cv.waitKey(3)



        