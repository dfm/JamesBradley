import os

def download_data():
    urlbase = "http://telescope.livjm.ac.uk/data/archive/data/lt/Skycam/"
    list = [
        ("2014/20140614/", "a_e_20140615_111_1_1_1.fits.gz"),
        ("2014/20140614/", "a_e_20140615_112_1_1_1.fits.gz"),
        ("2014/20140614/", "a_e_20140615_113_1_1_1.fits.gz"),
        ("2014/20140614/", "a_e_20140615_114_1_1_1.fits.gz"),
        ("2014/20140614/", "a_e_20140615_115_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_111_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_112_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_113_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_114_1_1_1.fits.gz"),
        ("2014/20140615/", "a_e_20140615_115_1_1_1.fits.gz"),
        ]
    for urlend, urlfn in list:
        url = urlbase + urlend + urlfn
        if not os.path.isfile(urlfn):
            os.system("curl -O %s" % url)
    return list

if __name__ == "__main__":
    print download_data()
