import numpy as np
import cv2
import os


def compute_disparity(img1, pts1, img2, pts2, desc1, desc2, cvBFSpp):
    """
    compute disparity
    Input
        img1 - image 1
        pts1 - coordinate of the points in image1
        img2 - image 2
        pts2 - coordinate of the points in image2
        desc1 -
        desc2 -
        cvBFSpp -
    Output
        pts_disparity - Coordinates and disparity saved in the left image
    """
    # Coordinates and disparity saved in the left image
    pts_disparity = []

    if pts1 is None or pts2 is None or desc1 is None or desc2 is None:
        print('[compute_disparity]==>pts1 is None or pts2 is None or desc1 is None or desc2 is None')
        return
    rows, cols = img1.shape
    matches = cvBFSpp.match(desc1.T, desc2.T)
    for match in matches:
        pt1 = pts1[:, match.queryIdx]
        pt2 = pts2[:, match.trainIdx]

        # ptL\ptR coordinates of corresponding points
        ptL = np.array([int(round(pt1[0])), int(round(pt1[1]))])
        ptR = np.array([int(round(pt2[0])), int(round(pt2[1]))])

        # compute disparity
        if abs(ptR[1] - ptL[1]) < 5:
            disparity = abs(ptR[0] - ptL[0])

            # save disparity with coordinates
            pt_disparity = [ptL[0], ptL[1], disparity]
            pts_disparity.append(pt_disparity)

    return pts_disparity


def compute_depth_with_disparity(pts_disparity, f=2.8846781815220919e+02, bf=1.4461438566692193e+01):
    """
    compute depth using disparity
    Input
        f - focal distance
        bf - to compute the length of baseline
        pts_disparity - Coordinates and disparity saved in the left image
    Output
        pts_depth - Coordinates and depth saved in the left image
    """
    # length of baseline
    Tx = bf / f
    pts_depth = []
    for pt_disparity in pts_disparity:
        # compute depth
        depth = f * Tx / pt_disparity[2] * 100

        # save depth with coordinates
        pt_depth = [pt_disparity[0], pt_disparity[1], depth]
        pts_depth.append(pt_depth)

    return pts_depth


def mark_depth(pts_depth, height=400, width=640, channels=1):
    """
    mark depth in image and show image in window
    Input
        pts_depth - Coordinates and depth saved in the left image
        height - height of image
        width - width of image
        channels - channels of rgb
    """

    image = cv2.imread("d1001678159715218574.png")
    # image = np.zeros((height, width, channels), dtype="uint8")
    for pt_depth in pts_depth:
        x_start, x_end = pt_depth[0]-1, pt_depth[0]+2
        y_start, y_end = pt_depth[1]-1, pt_depth[1]+2
        image[y_start:y_end, x_start:x_end] = int(pt_depth[2])

    # cv2.imwrite("./results/" + "demo.jpg", image)
    cv2.imshow("demo", image)
    # cv2.imwrite("./dst2.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


def revise_depth_show(pts_depth):
    """
    revise the depth of single image and show in window
    Input
        pts_depth - Coordinates and depth saved in the left image
    """

    # import image
    image = cv2.imread("d1001678159715218574.png")
    ratio_values = []
    cv2.imshow("demo_old", image)
    height, width = image.shape[0], image.shape[1]

    for pt_depth in pts_depth:
        depth_new = pt_depth[2]
        depth_old = image[pt_depth[1], pt_depth[0]][0]

        # Obtain the specific deep value of the corresponding point and save
        if depth_old > 1e-3:
            ratio_value = depth_new / depth_old
            ratio_values.append(ratio_value)
        else:
            continue

    # obtain the mean value of
    ratio_mean = np.mean(ratio_values)

    for h in range(height):
        for w in range(width):

            # assign a value to each pixel
            pixel = int(image[h, w][0] * ratio_mean)
            if pixel >= 256:
                image[h, w] = 255
            else:
                image[h, w] = pixel

    cv2.imshow("demo_new", image)


def revise_depth(pts_depth, path):
    """
    revise the depth of images and save
    Input
        pts_depth - Coordinates and depth saved in the left image
    """
    # import image
    image = cv2.imread(path)

    ratio_values = []
    height, width = image.shape[0], image.shape[1]

    for pt_depth in pts_depth:
        depth_new = pt_depth[2]
        depth_old = image[pt_depth[1], pt_depth[0]][0]

        # Obtain the specific deep value of the corresponding point and save
        ratio_value = depth_new / depth_old

        # avoid infinity
        if ratio_value > 100:
            continue
        else:
            ratio_values.append(ratio_value)

    # obtain the mean value of all the ratios
    ratio_mean = np.mean(ratio_values)

    # correct each pixel using uint16
    image_n = image.astype(np.uint16)
    image_new = np.zeros(image.shape)

    for h in range(height):
        for w in range(width):
            pixel = ratio_mean * image_n[h, w][0] * 65535 / 500
            if pixel >= 65535:
                image_new[h, w] = 65535
            else:
                image_new[h, w] = pixel

    # average value changed
    """img = image_new / 65535 * 255 - image
    img_mean = np.mean(img)
    print(name + "Average pixel value change====> %d" % int(img_mean))"""

    # path to save the result
    path_image_name = path.replace("DEPTH", "new_DEPTH")
    path_unit = path_image_name.split("/")
    path_image_new = '/'.join(path_unit[:-1])

    # path don't exist ,then create
    if not os.path.exists(path_image_new):
        os.makedirs(path_image_new)

    # save the result
    cv2.imwrite(path_image_name, image_new.astype(np.uint16))


def get_list_path():
    list_path_left = []
    # read the path of image
    f = open('remapl.txt', 'r', encoding='utf-8')
    listsl = f.readlines()
    for list in listsl:
        list = list[:-1]
        list_path_left.append(list)

    list_path_right = []
    # read the path of image
    f = open('remapr.txt', 'r', encoding='utf-8')
    listsr = f.readlines()
    for list in listsr:
        list = list[:-1]
        list_path_right.append(list)

    list_path_depth = []
    # read the path of image
    f = open('depth.txt', 'r', encoding='utf-8')
    listsd = f.readlines()
    for list in listsd:
        list = list[:-1]
        list_path_depth.append(list)

    f.close()
    return list_path_left, list_path_right, list_path_depth












