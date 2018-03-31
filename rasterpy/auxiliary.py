import os
from osgeo import osr

osr.UseExceptions()


def crsConvert(crsIn, crsOut):
    """
    convert between epsg, wkt, proj4 and opengis spatial references

    if type 'osr' is selected the function will return a spatial reference object of type osr.SpatialReference()
    :param crsIn: a osr.SpatialReference object, an opengis URL (e.g. 'http://www.opengis.net/def/crs/EPSG/0/4326') or a string of type WKT, PROJ4 or EPSG
    :param crsOut: either 'wkt', 'proj4', 'epsg', 'osr', 'opengis' or 'prettyWkt' (a wkt string formatted for readability)
    :return: a string or integer code describing the required CRS
    """
    if isinstance(crsIn, osr.SpatialReference):
        srs = crsIn.Clone()
    else:
        srs = osr.SpatialReference()
        try:
            if 'opengis.net/def/crs/EPSG/0/' in str(crsIn):
                crsIn = int(os.path.basename(crsIn.strip('/')))
            srs.ImportFromEPSG(crsIn)
        except (TypeError, RuntimeError):
            try:
                srs.ImportFromWkt(crsIn)
            except (TypeError, RuntimeError):
                try:
                    srs.ImportFromProj4(crsIn)
                except (TypeError, RuntimeError):
                    raise TypeError('crsIn not recognized; must be of type WKT, PROJ4 or EPSG')
    if crsOut == 'wkt':
        return srs.ExportToWkt()
    elif crsOut == 'prettyWkt':
        return srs.ExportToPrettyWkt()
    elif crsOut == 'proj4':
        return srs.ExportToProj4()
    elif crsOut == 'epsg':
        srs.AutoIdentifyEPSG()
        return int(srs.GetAuthorityCode(None))
    elif crsOut == 'opengis':
        srs.AutoIdentifyEPSG()
        return 'http://www.opengis.net/def/crs/EPSG/0/{}'.format(srs.GetAuthorityCode(None))
    elif crsOut == 'osr':
        return srs
    else:
        raise ValueError('crsOut not recognized; must be either wkt, proj4, opengis or epsg')