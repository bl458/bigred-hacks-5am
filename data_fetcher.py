#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 yqiu <yqiu@f24-suntzu>
#
# Distributed under terms of the MIT license.
# TODO:
# [x] combine RESS buildings
# [x] combine IVES HALL, EAST WEST ....
# [x] fix psb
# [x] create power graphs in python
# [x] cache systems

import pandas as pd
import buildings as bds
import re
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.style.use('ggplot')

no_data = []

def create_url(bd):
    ur1 = "http://portal.emcs.cornell.edu/"
    # ur2 = "?cmd=csv&s=1d&b=1474084800&e=1474171200"
    ur2 = "?cmd=csv&s=1d&b=1474171200&e=1474257600"
    return ur1 + bd + ur2

def time_series(df,bdg):
    # df is a dataframe with timestamp, kw cols
    cols = df.columns.values
    df[cols[0]] = df[cols[0]].apply(lambda x: pd.to_datetime(x,format='%d-%b-%Y %H:%M:%S'))
    df[cols[1]] = df[cols[1]].astype(float)
    print df[cols[0]]
    print df[cols[1]]
    try:
        ax = df.plot(x=cols[0],y=cols[1])
    except:
        print bdg, " no work for time series plot"
        import sys
        sys.exit()
    fig = ax.get_figure()
    fig.savefig('plots/' + bdg + '.png')

def parse_csv():
    builds = bds.builds

    pdic = {}
    for bdg in builds:
        psb = bdg == "Physical Sciences"

        bd = "".join(bdg.split())

        url = create_url(bd)
        if bdg == 'American Indian Program House': bdg = 'AKWEKON'
        bdg = bdg.upper()

        print url, "is the url"
        data = pd.read_csv(url)

        # rename unnamed to timestamp
        new_cols = data.columns.values
        new_cols[0] = 'timestamp'
        data.columns = new_cols

        # drop columns except for timestamp and electric
        data_keep = data.filter(regex='kW|timestamp')
        # if only 1 col (timestamp) so no elec pass
        if len(data_keep.columns.values[:]) <= 1:
            continue

        elec = data_keep.columns.values[:]
        # for i in xrange(1,len(elec)):
        #     data_keep = data_keep[ data_keep[elec[i]] != "nodata" ]
        data_keep = data_keep[ data_keep[elec[1]] != "nodata" ]

        # time_series(data_keep)
        # import sys; sys.exit()
        ############################## psb ###########
        # images
        if psb:
            data_keep = data_keep[ data_keep[elec[2]] != "nodata" ]
            print data_keep[elec[1]], "is data 1"
            print data_keep[elec[2]], "is data 2"
            data_keep['sum_kw_system'] = data_keep[elec[1]].astype(float) + data_keep[elec[2]].astype(float)
            print data_keep['sum_kw_system']
            elec = data_keep.columns.values[:]
            data_keep.drop(elec[1], axis=1, inplace=True)
            data_keep.drop(elec[2], axis=1, inplace=True)
            print data_keep
            # import sys; sys.exit()


        data_latest = data_keep.tail(1)
        # print data_latest
        # print data_latest.iloc[0]['sum_kw_system']
        # import sys; sys.exit()
        try:
            if psb:
                pdic[bdg] = data_latest.iloc[0]['sum_kw_system']
                time_series(data_keep,bdg)
            else:
                pdic[bdg] = float(data_latest.iloc[0][elec[1]])
                time_series(data_keep,bdg)
        except:
            print "in except"
            print bdg
            print data_latest
            no_data.append(bdg)
    return pdic

def sum_exception(dct,rgx,new):
    """ modifies dict with the power values of all regex matched
    buildings summed into one pair
    :dct: dictionary of building,power k-v pairs
    :rgx: regex expression
    """
    cumPow = 0
    print [ k for k in dct.keys() if re.match(rgx,k) ]
    for mvs in [ k for k in dct.keys() if
                re.match(rgx,k) ]:
        cumPow += dct[mvs]
        del dct[mvs]
    dct[new] = cumPow
    # print dct[new]


def main():
    pdic = parse_csv()
    sum_exception(pdic,"^MARTHA VANRENSSELAER\s.+","MARTHA VANRENSSELAER")
    print len(pdic)
    sum_exception(pdic,"^VET\s.+","VET SCHOOL")
    print len(pdic)
    sum_exception(pdic,"^IVES\s.+","IVES")
    print len(pdic)
    sum_exception(pdic,"^FRIEDMAN\s.+","FRIEDMAN WRESTLING CENTER")
    print len(pdic)
    # sum_exception(pdic)
    sum_exception(pdic,"^SCHURMAN\s.+","SCHURMAN")
    print len(pdic)
    sum_exception(pdic,"^WING HALL.*","WING HALL")
    print len(pdic)
    print no_data, " is no data"
    # print pdic
    return pdic

    # test plotting
    # url = "http://portal.emcs.cornell.edu/BoldtTower?cmd=csv&s=1d&b=1474171200&e=1474257600"
    # data = pd.read_csv(url)
    # new_cols = data.columns.values
    # new_cols[0] = 'timestamp'
    # print new_cols
    # print data.columns
    # print data.columns[0]
    # data.columns = new_cols
    # data_keep = data.filter(regex='kW|timestamp')

    # elec = data_keep.columns.values[:]
    # data_keep = data_keep[ data_keep[elec[1]] != "nodata" ]

    # time_series(data_keep,"Boldt Tower")


if __name__ == "__main__":
    main()
