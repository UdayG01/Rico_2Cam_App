import cv2

print("Testing DSHOW backend...")
for i in range(5):
    try:
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        opened = cap.isOpened()
        print(f"DSHOW Index {i}: {opened}")
        if opened:
            ret, frame = cap.read()
            print(f"  Frame read: {ret}")
        cap.release()
    except Exception as e:
        print(f"DSHOW Index {i} Error: {e}")

print("\nTesting MSMF backend...")
for i in range(5):
    try:
        cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
        opened = cap.isOpened()
        print(f"MSMF Index {i}: {opened}")
        if opened:
            ret, frame = cap.read()
            print(f"  Frame read: {ret}")
        cap.release()
    except Exception as e:
        print(f"MSMF Index {i} Error: {e}")
