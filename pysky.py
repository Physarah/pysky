import urllib
import xmltodict
import warnings
import datetime
import re
import astropy.units as u
from astropy.coordinates import SkyCoord
from xml.etree.ElementTree import parse
from xml.etree import ElementTree


class Euclid(object):
    """
    Parse the output of the Euclid background model:
    https://irsa.ipac.caltech.edu/applications/BackgroundModel/docs/dustProgramInterface.html

    Example Usage:
    -------------

    model = Euclid(coordinates = SkyCoord('0h39m15.9s', '0d53m17.016s', frame='icrs'),
                    wavelength = 200*u.micron,
                    date = datetime.datetime(2019, 4, 13),
                    observing_location = 'L2',
                    code_version = 'Wright',
                    median = True)

    model.zodiacal_light

    Inputs:
    ------
       coordinates (astropy.coordinates.sky_coordinate.SkyCoord): coordinates of the field
       wavelength (astropy.units.quantity.Quantity): wavelength of observation
       date (datetime.datetime): date of observation, limited to 2018 to 2029 for L2 position
       observing_location (str): observing location. Either the L2 or Earth
       code_version (str): can be Wright or Kelsall, depending on what model you'd like
       median (bool): if True, will find median zodiacal over a likely viewing range

    Usefull Atributes:
    -----------------

         request (collections.OrderedDict): dictionary of the request output
         zodiacal_light (astropy.units.quantity.Quantity): zodiacal light background (MJy/sr)
         ism (astropy.units.quantity.Quantity): interstellar medium background (MJy/sr)
         stars (astropy.units.quantity.Quantity): stellar background (MJy/sr)
         cib (astropy.units.quantity.Quantity): cosmic infrared background (MJy/sr)
         total_background (astropy.units.quantity.Quantity): total background (MJy/sr).
    """

    def __init__(self, coordinates, wavelength, date, observing_location, code_version, median):

        self.wavelength = (wavelength.to(u.micron)).value

        try:
            transform_coords = coordinates.transform_to('icrs')
            self.locstr = transform_coords.to_string('hmsdms')
        except:
            raise ValueError(
                "{} is not an astropy.coordinates.sky_coordinate.SkyCoord".format(type(coordinates)))

        try:
            self.year, self.day = self.get_year_date(date)
            if self.year < 2018 or self.year > 2029:
                raise ValueError(
                    "This date is not between 2018 and 2029. Please try another date.")
        except:
            pass

        if observing_location == "Earth":
            self.obslocin = '3'
        elif observing_location == "L2":
            self.obslocin = '1'
        else:
            raise ValueError(
                "{} is an incorrect input. Please choose 'Earth' or 'L2'".format(observing_location))

        if code_version == "Wright":
            self.obsverin = '0'

        elif code_version == 'Kelsall':
            self.obsverin = "3"

        else:
            raise ValueError(
                "{} is an incorrect input. Please choose 'Wright' or 'Kelsall'".format(code_version))

        if median:
            self.ido_viewin = '1'
        else:
            self.ido_viewin = '0'

        try:
            self.request = self.send_request(self.parse_url())
            self.request_status = self.request['results']['@status']
            self.zodiacal_light = float((re.findall(
                '\d*\.?\d+', self.request['results']['result']['statistics']['zody'])[0]))*u.megajansky * u.sr**-1
            self.ism = float((re.findall(
                '\d*\.?\d+', self.request['results']['result']['statistics']['ism'])[0]))*u.megajansky * u.sr**-1
            self.stars = float((re.findall(
                '\d*\.?\d+', self.request['results']['result']['statistics']['stars'])[0]))*u.megajansky * u.sr**-1
            self.cib = float((re.findall(
                '\d*\.?\d+', self.request['results']['result']['statistics']['cib'])[0]))*u.megajansky * u.sr**-1
            self.total_background = float((re.findall(
                '\d*\.?\d+', self.request['results']['result']['statistics']['totbg'])[0]))*u.megajansky * u.sr**-1
        except:
            warnings.warn("Sorry, something went wrong. Try again.")

    def parse_url(self):
        base_url = "https://irsa.ipac.caltech.edu/cgi-bin/BackgroundModel/nph-bgmodel?"
        url = base_url + "locstr={}&wavelength={}&year={}&day={}&obslocin={}&ido_viewin={}".format(self.locstr,
                                                                                                   self.wavelength,
                                                                                                   self.year,
                                                                                                   self.day,
                                                                                                   self.obslocin,
                                                                                                   self.obsverin,
                                                                                                   self.ido_viewin)
        return(url.replace(" ", ""))

    def get_year_date(self, date):
        year = date.year
        day = date.timetuple().tm_yday
        return(year, day)

    def send_request(self, url):
        contents = urllib.request.urlopen(url)
        xmldoc = parse(contents)
        tree = xmldoc.getroot()
        xml_str = ElementTree.tostring(tree).decode()
        dictionary_out = xmltodict.parse(xml_str)
        return(dictionary_out)
