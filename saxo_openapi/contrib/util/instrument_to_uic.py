# -*- coding: utf-8 -*-

"""Utility classes and/or functions."""

from saxo_openapi.definitions.orders import AssetType
import saxo_openapi.endpoints.referencedata as rd
import warnings
import sys

def InstrumentToUic(client,
                    AccountKey,
                    spec,
                    assettype=None,
                    full_search=False):

    ## check validity of full_search
    assert type(full_search) == bool, ("The argument `full_search` has to be a "
    "logical flag!")

    ## list all asstetypes and check argument validity
    all_types = AssetType().definitions.keys()

    ## search for uic in all assettypes:
    if full_search:
        assettype = all_types

    # check if assetype is valid
    else:
        if assettype is None:
            assettype = AssetType.FxSpot
            message = ("No value to the `assettype` argument was provided. "
            "Setting default value to 'FxSpot'.")
            warn = warnings.formatwarning(message,
                                          category=UserWarning,
                                          filename="instrument_to_uic.py",
                                          lineno=29,
                                          line=None)
            print(warn, file = sys.stdout)  # Print to stdout instead of stderr
        else:
            assert assettype in all_types, ("The argument `assettype` has to "
            "be a valid AssetType class object!")
        assettype = [assettype]

    ## perform the api query
    if 'Instrument' in spec:
        print("Fetching info for...:")
        rv = []
        message2 = "Found {number}"
        for asset in assettype:
            params = {
                'AccountKey': AccountKey,
                'AssetTypes': asset,
                'Keywords': spec.get('Instrument')
            }

            # create the request to fetch Instrument info
            r = rd.instruments.Instruments(params=params)
            current_request = client.request(r)
            rv.append(current_request)

            # print custom message to the console
            print("    {:<20}".format(asset), end = '')
            print(message2.format(number = len(current_request['Data'])))

        #print(rv)

        all_inst = []
        for asset in rv:
            for instrument in asset['Data']:

                all_inst.append({'Uic': instrument.get('Identifier'),
                                 'AssetType': instrument.get('AssetType'),
                                 'Symbol': instrument.get('Symbol'),
                                 'ExchangeId': instrument.get('ExchangeId'),
                                 'IssuerCountry': instrument.get('IssuerCountry'),
                                 'Description': instrument.get('Descritpion'),
                                 'CurrencyCode': instrument.get('CurrencyCode')})

    return all_inst
