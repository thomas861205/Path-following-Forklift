

# 1. K64F

The code that K64F runs is used to handle the RPC and the uLCD display.

RPC functions support the control of two continuous servo motors (wheels), which take commands from Udoo Neo.

uLCD displays the result of the picture on the box -- either Doraemon or Pikachu.

I add an addtional standard servo as a lifter to pick up the box. But when I do this, the other two continuous servos start to jiggle, which seems very 
strange to me since I have already adjust all servos so that when they are set to zero, all of them should be steady. So I dig into the 
parallax_stdservo.h and notice there are some difference between parallax_servo.h. Thus I add

```
#ifndef PARALLAX_STDSERVO_H
#define PARALLAX_STDSERVO_H
.
.
.
#endif
```
just like the code in parallax_servo.h. To my big surprise, somehow they stop jiggling! I also modified the bbcar_init.cpp and bbcar_rpc.cpp so that it can properly controll the lifter.

# 2. Udoo Neo

Udoo Neo runs the python code "[udoo_control_center.py](#udoo)"
, which includes the following functions (only list modified):

- [calibrate](#calibrate) from calibrate

- [draw_line](#draw_line)

- [Pikachu](#Pikachu) from kerasOnUbuntu

# 3. Not Integrated

- mqtt_clipu:

    - the code enable a device to be a publish and a subscriber at a same time. Basically what I do is just put mqtt_client and mqtt_publisher together. The crucial modification is to substitute "client.loop_forever()" to "client.loop_start()". The former is a blocking functon, which means you are always listening thus cannot publish on topics. The "loop_start()" runs in background, it gets triggered only when there is difference on subscribed topics.
#

## <a name="calibrate"></a> calibrate

I set

```
transform_ratio = 0.9
```

so that the picture contains more part of lines.

## <a name="draw_line"></a> draw_line

I create get_yellow, get_white, get_red so that I can adjust the range when I needed very easily.

## <a name="Pikachu"></a> Pikachu

Pikachu classifies the picture to two categories -- Doraemon or Pikachu.

## <a name="udoo"></a> udoo_control_center.py

in "main" function it start to do the opencv thing to make the boebot follow the road. There are some difference from lab's version:

- In get_contour_from_image:

    - I have a counter for redlines. If there are 20 consecutive frames contain redline, then stop the boe bot.

    - Remove those contours that are left to the yellow to avoid any unwanted contour.

    - Call contour_largest instead of contour_leftest to make better performance.

- In _control_center:

    - set "speed = int(20*abs(turn) + 50)" to make the delay of catching frames and moving less significant.

- Also I add a bunch of functions to make the RPC calls much easier.