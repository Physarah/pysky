# pysky
A wrapper to parse the EUCLID NASA science centre sky background model in python 

### Example Usage 

```
model = Euclid(coordinates = SkyCoord('0h39m15.9s', '0d53m17.016s', frame='icrs'),
                wavelength = 200*u.micron,
                date = datetime.datetime(2019, 4, 13),
                observing_location = 'L2',
                code_version = 'Wright',
                median = True)
```
Then to access attributes of the class

```
model.zodiacal_light
```
