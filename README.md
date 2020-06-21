# concurrent-videocapture
Cv2 VideoCapture that runs concurrently in a thread for faster processing

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