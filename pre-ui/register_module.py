
import os
import cv2
import numpy as np
from scipy.ndimage import zoom
from skimage import io, transform
from skimage.transform import SimilarityTransform, warp

def register(pth, IHC=0, E=1, zc=None, szz=None, sk=1, tpout='tif', regE=None):
    # Rough registration of a series of 2D tumor sections cut along the z axis. Images will be warped into near-alignment
    np.warnings.filterwarnings('ignore')
    if zc is None:
        zc = int(len(os.listdir(pth)) / 2)
    if regE is None:
        regE = {'szE': 201, 'bfE': 100, 'diE': 155}
    
    imlist = os.listdir(pth)
    imlist = [f for f in imlist if f.endswith('.tif') or f.endswith('.jp2') or f.endswith('.jpg')]
    
    tp = imlist[0][-3:]
    if szz is None:
        szz = [0, 0]
        for imname in imlist:
            inf = cv2.imread(os.path.join(pth, imname), cv2.IMREAD_UNCHANGED)
            height, width = inf.shape[:2]
            szz = [max(szz[0], height), max(szz[1], width)]
    
    padall = 250  # padding around all images
    if IHC == 1:
        rsc = 4
    elif IHC == 10:
        rsc = 2
    else:
        rsc = 6
    iternum = 5  # max iterations of registration calculation
    
    outpthG = os.path.join(pth, 'registered/')
    outpthE = os.path.join(outpthG, 'elastic registration/')
    matpth = os.path.join(outpthE, 'save_warps/')
    os.makedirs(outpthG, exist_ok=True)
    os.makedirs(matpth, exist_ok=True)
    if E:
        os.makedirs(outpthE, exist_ok=True)
        os.makedirs(os.path.join(matpth, 'D/'), exist_ok=True)
        os.makedirs(os.path.join(matpth, 'D/Dnew/'), exist_ok=True)
    
    nm = imlist[zc][:-3]
    imzc, TAzc = get_ims(pth, nm, tp)
    imzc, imzcg, TAzc = preprocessing(imzc, TAzc, szz, padall, IHC)
    print('Reference image:', nm)
    
    io.imsave(os.path.join(outpthG, nm + tpout), imzc)
    if E:
        io.imsave(os.path.join(outpthE, nm + tpout), imzc)
        D = np.zeros((imzc.shape[0], imzc.shape[1], 2))
        np.save(os.path.join(matpth, 'D/', nm + 'mat'), D)
    
    img = imzcg
    TA = TAzc
    krf = zc
    img0 = imzcg
    TA0 = TAzc
    krf0 = zc
    img00 = imzcg
    TA00 = TAzc
    krf00 = zc
    
    for kk in range(len(mv)):
        t1 = time.time()
        print('Image', kk, 'of', len(imlist)-1)
        print('  reference image:', imlist[rf[kk]][:-4])
        print('  moving image:', im)
