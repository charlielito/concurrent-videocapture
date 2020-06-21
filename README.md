# concurrent-videocapture
Opencv VideoCapture that runs concurrently in a thread for faster processing

## Installation

You can install `concurrent_videocapture` from pip using

```
pip install concurrent_videocapture
```

or using

```
pip install git+https://github.com/charlielito/concurrent-videocapture
```

## Usage
It follows the same api than `cv2.VideoCapture`, so the change in code is minimal. The following example just opens the Camera 0 and shows the image in a cv2 window while simulating a heavy image processing function with `time.sleep`.

```python
import cv2
import time
from concurrent_videocapture import ConcurrentVideoCapture
# Use it a the standard cv2.VideoCapture Class
cap = ConcurrentVideoCapture(0)
while True:
    init = time.time()
    grabbed, frame = cap.read()

    # Simulate heavy image processing function
    time.sleep(0.3)
    if not grabbed:
        break
    cv2.imshow("video", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    fps = 1/(time.time() - init)
    print('Fps: {}'.format(fps))
cap.release()
```

### Additional parameters
Sometimes it is useful to perform some preprocessing to the image in the thread where the camera is read. For that we can use in the constructor the parameter `transform_fn`, which is a function that is applied to each frame. The flag `return_rgb` is for converting each frame to RGB since opencv by default returns the frames in GBR format. The next example will flip horizontally the image and return it as RGB:

```python
import cv2
from concurrent_videocapture import ConcurrentVideoCapture

cap = ConcurrentVideoCapture(0, transform_fn=lambda image:cv2.flip(image, 1), return_rgb=True)
while True:
    grabbed, frame = cap.read()

    if not grabbed:
        break
    cv2.imshow("video", frame)
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
cap.release()
```
