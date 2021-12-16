import dlib
import cv2
import numpy as np
from imutils.face_utils import FaceAligner


def load_and_align(filepath, model_detector):
    """
    Loads an image from the given filepath. It then gives the resulting
    array containing an aligned image from a face detector

    Args:
        filepath : Relative filepath to an image

    Returns: either None or a numpy array consisting of the RGB aligned face
    """

    shape_predictor = dlib.shape_predictor(
        'Models/shape_predictor_68_face_landmarks.dat')

    # Resize and align the face for facenet detector (facenet expects 160 by 160 images)
    face_aligner = FaceAligner(
        shape_predictor, desiredFaceHeight=160, desiredFaceWidth=160)

    input_image = cv2.imread(filepath)
    
    #print(input_image)
    # cv2 returns None instead of throwing an error if an image is not found.
    if input_image is None:
        return None
    '''
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)  #GPU
    height, width, _ = input_image.shape

    # Discard any low resolution images
    if height < 160 or width < 160:
        return None

    # Resize any high resolution images while maintaining aspect ratio
    # 4k images usually take a really long time to process
    elif width > 1280 and height > 720:
        ratio = 1280/width
        input_image = cv2.resize(input_image, (1280, int(ratio*height)), interpolation=cv2.INTER_AREA)
    '''

    # convert images to grayscale for the detector
    # get all the attributes for the rectangle's of the detected faces in the image

    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
    h, w, _ = input_image.shape
    img_resize = cv2.resize(input_image, (320, 240))
    img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
    img_resize = img_resize - 127.0
    img_resize = img_resize / 128.0
    results = model_detector.predict(np.expand_dims(img_resize, axis=0))  # result=[background,face,x1,y1,x2,y2]
    gray_img = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY) #GPU

    rectangles = []
    for result in results:
        start_x = int(result[2] * w)
        start_y = int(result[3] * h)
        end_x = int(result[4] * w)
        end_y = int(result[5] * h)
        rect = dlib.rectangle(int(start_x), int(start_y), int(end_x), int(end_y))
        rectangles.append(rect)
    #cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    #cv2.imwrite(f'imgs/test_output_{args.net_type}.jpg', img)

    #print(len(rectangles))
    if len(rectangles) > 0:
        aligned_faces = []
        for rectangle in rectangles:
            #print("x1:{} y1:{}\nx2:{} y2:{}".format(rectangle.left(), rectangle.top(), rectangle.right(), rectangle.bottom()))
            aligned_face = face_aligner.align(input_image, gray_img, rectangle)
            #print(np.array(aligned_face))
            #cv2.waitKey()
            #cv2.destroyAllWindows()
            #print(input_image)

            #for l1 in aligned_face:
            #    print(l1)
            aligned_faces.append(aligned_face)

        # returns numpy array of shape (num-faces,160,160,3)
        return np.array(aligned_faces)
    else:
        return None
    '''
    for i in range(len(rectangles)):
        landmarks = np.matrix([[p.x, p.y] for p in shape_predictor(input_image,rectangles[i]).parts()])
        for idx, point in enumerate(landmarks):
            # 68点的坐标
            pos = (point[0, 0], point[0, 1])
            print(idx+1, pos)
            pos_info = str(point[0, 0]) + ' ' + str(point[0, 1]) + '\n'
            #file_handle.write(pos_info)
            # 利用cv2.circle给每个特征点画一个圈，共68个
            cv2.circle(input_image, pos, 3, color=(0, 255, 0))
            # 利用cv2.putText输出1-68
            #font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(img, str(idx+1), pos, font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        # If no faces are detected return None which is understood by the script calling it
    cv2.imshow("input",input_image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    '''


def standardize(image):
    """converts the pixel values range to the one suitable for facenet

    Args:
        image : numpy array of an rgb image with pixels in range [0,255]

    Returns:
        standardized_image: image standardized for the facenet model
    """
    mean = np.mean(image, axis=(1, 2, 3), keepdims=True)
    std_dev = np.std(image, axis=(1, 2, 3), keepdims=True)
    std_dev = np.maximum(std_dev, 1.0/np.sqrt(image.size))

    standardized_image = (image - mean)/std_dev
    return standardized_image


def normalize_emb(emb, axis=-1, eps=1e-10):
    """L2 normalizes the embeddings from the model

    Args:
        emb : numpy array of shape (1,128) containing the embedding from the model
        axis : axis on which to compute L2 norm
        eps : epsilon value to prevent division by zero

    Returns: numpy array consisting of 128 dimensional unit vector for the face embedding
    """
    normalized_emb = emb / np.sqrt(np.maximum(np.sum(np.square(emb), axis=axis, keepdims=True), eps))
    return normalized_emb


def compute_embedding(img_path, model, model_detector):
    """Computes the embedding(s) for the face(s) in the image at the given path

        NOTE: The model is not loaded in this function to prevent reading the *.h5 file
        to load the model everytime this function is called to compute an embedding for an image

    Args:
        img_path : relative path to the image
        model : keras model to compute embeddings

    Returns:
        embeddings: numpy array of shape (number of detected faces,dimension of embedding) containing the embeddings for the detected faces
    """
    # can be a single image or a batch of images or None depending on number of faces detected in the image
    images = load_and_align(img_path,model_detector)

    # It is safely interpreted by the calling function
    if images is None:
        return None

    images = standardize(images)

    embeddings = model.predict(images)
    embeddings = normalize_emb(embeddings)

    return embeddings
