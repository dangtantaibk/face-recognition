import cv2
import numpy as np

# Load ảnh và chuyển sang ảnh xám
img1 = cv2.imread('/Users/taidang/Desktop/1.jpeg')
img2 = cv2.imread('/Users/taidang/Desktop/2.jpeg')
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Tìm kiếm các điểm đặc trưng của hai ảnh
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

# Xác định các cặp điểm tương ứng giữa hai ảnh
index_params = dict(algorithm=0, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# Lọc các cặp điểm không chính xác
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# Tính ma trận biến đổi giữa hai ảnh
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Tính số lượng cặp điểm tương ứng và độ tin cậy của việc nhận diện địa điểm chụp
num_matches = len(good_matches)
confidence = float(mask.sum()) / float(mask.size)

print("Number of matching points: ", num_matches)
print("Confidence: ", confidence)

# Vẽ kết quả
img3 = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=2)
cv2.imshow('Matching result', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()
