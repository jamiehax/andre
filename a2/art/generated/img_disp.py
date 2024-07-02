import cv2

img = cv2.imread("a2/art/generated/output.jpg")
cv2.imshow('you (lowkey)', img)

# kill the windows
# cv2.destroyWindow('you (lowkey)')

cv2.waitKey(5000)
cv2.destroyAllWindows()
