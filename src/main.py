
import numpy as np
import cv2 as cv
import pickle as pkl


global spot_pos, offset, width, height, threshold

spot_pos = []           # store the spot position
section_pos = []        # store the section position
offset = 22             # parking rectangle spot offset
width = 45              # width of parking space
height = 20             # height of parking space
threshold = 150         # threshold pixel value to detect parking spot


# Create videocapture object and read from input file
cap = cv.VideoCapture('parkinglot_timelapse.mp4')

# Check if camera opened successfully
if cap.isOpened()==False:
    print("Error opening video stream or file")

# Unpickling positions
with open('spot_pos.pkl', 'rb') as f:
        spot_pos = pkl.load(f)
# Unpickling positions
with open('section_pos.pkl', 'rb') as f:
        section_pos = pkl.load(f)

print(int(len(section_pos)/2))
for i in range(int(len(section_pos)/2)):
    print('hello world')
        
# Image processing
def process_frame(frame):
    imgGray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (5, 5),1)
    imgThresh = cv.adaptiveThreshold(imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
    return imgThresh

def checkParkingSpots(imgPro,frame):
    
    spaceCounter = 0
    redPos = []    # store the red coord spaces in frame
    greenPos = []  # store the green  coord spaces in frame
    
    for pos in spot_pos:
        x = pos[0]
        y = pos[1]-offset
        imgCrop = imgPro[y:y+height,x:x+width]
        count = cv.countNonZero(imgCrop) #nonzero pixel count
        
        # display count
        cv.putText(frame,str(count),(x + 2, y + 10),
                   fontFace = cv.FONT_HERSHEY_SIMPLEX , 
                   fontScale = 0.4, color = (255, 255, 255),
                   thickness = 1, 
                   lineType = cv.LINE_AA)
        
        # display colorcoded spot position
        if count > threshold:
            color = (0,0,255) # red
            redPos.append(pos)
        else:
            color = (0,255,0) # green
            greenPos.append(pos)
            spaceCounter += 1
        
        cv.rectangle(frame, (pos[0], pos[1] - offset),(pos[0] + width, pos[1] + height - offset), color, 2)
    
    # Text background upper left corner
    cv.rectangle(frame,(0,0),(600,500), (0,0,0),-1)
                
    # display free parking spaces
    cv.putText(frame,'Free Parking Spaces: {} / {}'.format(str(spaceCounter),len(spot_pos)),(50, 50),
                fontFace = cv.FONT_HERSHEY_SIMPLEX , 
                fontScale = 1, 
                color = (255, 255, 255),
                thickness = 4, 
                lineType = cv.LINE_AA)
    
    return redPos,greenPos
    

def checkParkingSections(imgPro,frame,redPos,greenPos):
#receives a frame, a list of all red spot positions, and a list of all green spot positions

    red_counter = 0    #number of red spot positions at specific parking section
    green_counter = 0  #number of green spot positions at specific parking section
    spaceDistribution = []  # stores (green_counter, red_counter) -> index 0  = Section 0

    
    # Display section position
    for i in range(int(len(section_pos) / 2)):
        
        pointer  = i * 2
        
        rect_point1 = section_pos[pointer]
        rect_point2 = section_pos[pointer + 1]

        # Display section position
        cv.rectangle(frame,rect_point1, rect_point2, (255,255,255), 2)
        
        # Display section label
        cv.putText(frame,'S{}'.format(int(pointer/2)), (rect_point1[0], rect_point1[1]-10),
                fontFace = cv.FONT_HERSHEY_SIMPLEX , 
                fontScale = 1, 
                color = (255, 255, 255),
                thickness = 4, 
                lineType = cv.LINE_AA)
        
        # Compute free spaces in each section
        for i in range(len(greenPos)):
            if greenPos[i][0] > rect_point1[0] and greenPos[i][0] < rect_point2[0]:
                green_counter += 1
        for i in range(len(redPos)):
            if redPos[i][0] > rect_point1[0] and redPos[i][0] < rect_point2[0]:
                red_counter += 1
        
        spaceDistribution.append((green_counter,red_counter))
        
        green_counter = 0
        red_counter = 0
    
    
    y_increment = 30
    y_pos = 70
    for i in range(12):
        y_pos += y_increment

        # display free parking spaces
        cv.putText(frame,'Free spaces in S{}: {}/{}'.format(i,spaceDistribution[i][0],spaceDistribution[i][0]+spaceDistribution[i][1]),
                   (50, y_pos),
                    fontFace = cv.FONT_HERSHEY_SIMPLEX , 
                    fontScale = 1, 
                    color = (255, 255, 255),
                    thickness = 2, 
                    lineType = cv.LINE_AA)
        
        
        
        

            
            
    
    
    
        
    
# def axisVis():
#     #upper left, upper right, lower left
#     pos = [(100,100),(1600,10),(100,1000)]

#     for i in range(3):
#         cv.putText(frame,'{}'.format(pos[i]),pos[i],
#                 fontFace = cv.FONT_HERSHEY_SIMPLEX , 
#                 fontScale = 0.5, 
#                 color = (255, 255, 255),
#                 thickness = 2, 
#                 lineType = cv.LINE_AA)
    
        
#Read until video is completed
while cap.isOpened():
    
    ret,frame = cap.read()
    if ret:
    
        imgPro = process_frame(frame)
        redPos, greenPos = checkParkingSpots(imgPro,frame)
        checkParkingSections(imgPro,frame, redPos, greenPos)
        
        cv.namedWindow('frame', cv.WINDOW_NORMAL)
        cv.setWindowProperty('frame', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        
        #axisVis()


        cv.imshow('frame',frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
    
cap.release()
cv.destroyAllWindows()


