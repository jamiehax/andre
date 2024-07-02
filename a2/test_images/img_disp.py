import cv2

img = cv2.imread("test_images/1.jpg")
cv2.imshow('1', img)
cv2.waitKey(5000)
cv2.destroyWindow('1')

img = cv2.imread("test_images/2.jpg")
cv2.imshow('2', img)
cv2.waitKey(5000)
cv2.destroyWindow('2')

cv2.destroyAllWindows()
