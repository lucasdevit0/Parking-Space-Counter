# Parking Space Counter using Python, OpenCV and Pickle
<img src="img/parkingcv_final.png" width="1000"> 

## Video Used

Tom Berrigan https://www.youtube.com/watch?v=yojapmOkIfg&list=LL&index=10

* Download this video in 1080p
* Rename it to parkinglot_timeplapse.mp4 
* Place it in project folder

## Packages
```sh
pip install cv2
pip install pickle
```

### Get started
```sh
run spot_picker.py
```
Mark parking spaces with left click, delete with right click.
Output: spot_pos.pkl (stores (x,y) of each space)

```sh
run section_picker.py
```
Mark parking sections with left click, delete with right click. 
Output: spot_pos.pkl (stores (x,y) of each space)


## Code inspired by:

Murtaza's Workshop - Robotics and AI https://www.youtube.com/watch?v=caKnQlCMIYI
