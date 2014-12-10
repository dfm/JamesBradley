import os
from datetime import datetime
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

def download_data():
    urlbase = "http://telescope.livjm.ac.uk/data/archive/data/lt/Skycam/"
    list = [
        ("2013/20130614/", "a_e_20130614_114_1_1_1.fits.gz"),
        ("2014/20140614/", "a_e_20140614_113_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_105_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_106_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_107_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_108_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_109_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_110_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_111_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_112_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_113_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_114_1_1_1.fits.gz"),
        ]
    for urlend, urlfn in list:
        url = urlbase + urlend + urlfn
        if not os.path.isfile(urlfn):
            os.system("curl -O %s" % url)
    return list

def _normalize(vec):
    v = vec - np.mean(vec)
    return v / np.sqrt(np.sum(v * v))

def _get_time(str):
    return datetime.strptime(str, "%Y-%m-%dT%H:%M:%S")

def cross_correlate_files(fn1, fn2, hw=128):
    print fn1, fn2
    hdulist1 = fits.open(fn1)
    hdulist2 = fits.open(fn2)
    if (hdulist1[0].header["NAXIS1"] != hdulist2[0].header["NAXIS1"]) or (hdulist1[0].header["NAXIS2"] != hdulist2[0].header["NAXIS2"]):
        print hdulist1[0].header["NAXIS1"], hdulist2[0].header["NAXIS1"], hdulist1[0].header["NAXIS2"], hdulist2[0].header["NAXIS2"]
        assert False
    x1 = hdulist1[0].header["NAXIS1"] / 2 - hw
    x2 = x1 + hw + hw
    y1 = hdulist1[0].header["NAXIS2"] / 2 - hw
    y2 = y1 + hw + hw
    vec1 = _normalize(hdulist1[0].data[y1:y2, x1:x2])
    vec2 = _normalize(hdulist2[0].data[y1:y2, x1:x2])
    t1 = _get_time(hdulist1[0].header["DATE-OBS"])
    t2 = _get_time(hdulist2[0].header["DATE-OBS"])
    cc = np.sum(vec1 * vec2)
    return t1, t2, cc

def compare(list, jj, prefix, truth):
    dts = []
    ccs = []
    for ii in np.arange(jj + 1, len(list)):
        t1, t2, cc = cross_correlate_files(list[jj][1], list[ii][1])
        dts.append((t2 - t1).total_seconds())
        ccs.append(cc)
    dts = np.array(dts)
    ccs = np.array(ccs)
    maxj = np.argmax(ccs)
    qq = np.polyfit(dts[maxj-1:maxj+2], np.log(ccs[maxj-1:maxj+2]), 2)
    dtplot = np.arange(np.min(dts), np.max(dts), 1.)
    ccplot = np.exp(np.polyval(qq, dtplot))
    plt.clf()
    plt.plot(dts, ccs)
    plt.plot(dtplot, ccplot)
    plt.axvline(truth)
    plt.savefig("%s.png" % prefix)
    plt.xlim(truth - 4., truth + 4.)
    plt.ylim(0.95 * np.max(ccplot), 1.05 * np.max(ccplot))
    plt.savefig("%s_zoom.png" % prefix)

if __name__ == "__main__":
    list = download_data()
    compare(list, 1, "sd", 86164.0905)
    compare(list, 0, "sy", 365. * 86164.0905)
