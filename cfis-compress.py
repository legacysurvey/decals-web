import os
import fitsio
from astrometry.util.fits import fits_table
import numpy as np
from astrometry.util.multiproc import multiproc

def one_file(fn):
    fn = fn.strip()
    fn = os.path.join('/data/CFIS', fn)
    outfn = fn.replace('tiles-dr2', 'compressed/tiles-dr2')
    if os.path.exists(outfn):
        print('Exists:', outfn)
    print(fn)
    img,hdr = fitsio.read(fn, header=True)
    wfn = fn.replace('.r.fits', '.r.weight.fits.fz')
    wt = fitsio.read(wfn)
    # that's it...
    img[wt == 0] = 0.

    # Blanton MAD sigmas: 2-3
    # qz -1e-4: files ~ 200 MB
    # qz -1e-3: files ~ 160 MB
    # qz -1e-2: files ~ 125 MB
    # qz -1e-1: files ~  88 MB
    finalfn = outfn
    tmpfn = outfn.replace('CFIS.', 'tmp.CFIS.')
    outfn = tmpfn + '[compress R 200 200; qz -1e-1]'
    fitsio.write(outfn, img, header=hdr, clobber=True)
    os.rename(tmpfn, finalfn)
        
    # cimg = fitsio.read(outfn)
    # print('RMS diff', np.sqrt(np.mean((cimg - img)**2)))
    # nz = np.sum(img != 0)
    # print('Non-zero pixels: %.3g %%' % (100. * nz / (img.shape[0]*img.shape[1])))
    # slice1 = (slice(0,-5,10),slice(0,-5,10))
    # slice2 = (slice(5,None,10),slice(5,None,10))
    # diff = np.abs(img[slice1] - img[slice2]).ravel()
    # diff = diff[diff != 0.]
    # mad = np.median(diff)
    # sig1 = 1.4826 * mad / np.sqrt(2.)
    # print('vs Blanton sigma', sig1)

def main():
    T = fits_table('data/cfis-r/cfis-tiles.fits')
    mp = multiproc(4)
    mp.map(one_file, T.filename)
    #map(one_file, [fn for fn in T.filename])

if __name__ == '__main__':
    main()
