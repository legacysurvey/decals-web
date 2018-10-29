from glob import glob
from astrometry.util.fits import *
from astrometry.util.util import * #Tan #, Sin
import numpy as np
import fitsio

# from desiutil.brick import Bricks
# Bricks(2.0).to_table().write('vlass-bricks-1.fits', format='fits')
# Bricks(4.0).to_table().write('vlass-bricks-2.fits', format='fits')
# Bricks(8.0).to_table().write('vlass-bricks-3.fits', format='fits')
# Bricks(16.0).to_table().write('vlass-bricks-4.fits', format='fits')
# Bricks(32.0).to_table().write('vlass-bricks-5.fits', format='fits')

# wget -v -r -nH --cut-dirs 2 -np -R *.rms.subim.fits https://archive-new.nrao.edu/vlass/quicklook/VLASS1.1/T29t02/
# (but then I moved files around, eliminating one level of subdir, sort of by accident)
# (also, this wget doesn't work at NERSC)


fns = glob('data/vlass/VLASS1.1/*/*.fits')
fns.sort()
print(len(fns), 'files')

T = fits_table()
T.filename = np.array([fn.replace('data/vlass/', '') for fn in fns])
T.tile = []
T.brickname = []
T.ra = np.zeros(len(T), np.float32)
T.dec = np.zeros(len(T), np.float32)
T.ra1 = np.zeros(len(T), np.float32)
T.dec1 = np.zeros(len(T), np.float32)
T.ra2 = np.zeros(len(T), np.float32)
T.dec2 = np.zeros(len(T), np.float32)


for i,fn in enumerate(fns):
    print('File', fn)
    hdr = fitsio.read_header(fn)
    hdr.delete('SPW')
    qhdr = fitsio_to_qfits_header(hdr)
    wcs = Tan(qhdr)
    print('WCS:', wcs)
    H,W = wcs.shape
    rr,dd = wcs.pixelxy2radec([1, W, (W+1)/2., (W+1)/2.],
                              [(H+1)/2., (H+1)/2., 1., H])
    print('RA', rr[:2], 'Dec', dd[2:])

    rc,dc = wcs.radec_center()

    T.ra[i] = rc
    T.dec[i] = dc
    T.ra1[i] = rr[1]
    T.ra2[i] = rr[0]
    T.dec1[i] = dd[2]
    T.dec2[i] = dd[3]

    T.tile.append(hdr['FILNAM04'])
    T.brickname.append(hdr['FILNAM05'])

T.tile = np.array(T.tile)
T.brickname = np.array(T.brickname)
    
T.writeto('data/vlass/vlass-tiles.fits')
