# resources.py
# This file is part of Fantasy City Planner.
# See fcp.py for license information


def resource_consistency_check(PLACES, RESOURCES, WEALTH, INHABITANTS):

    if(('WOOD' in RESOURCES)and(not 'SAWMILL' in PLACES)):
        print('inconsistency WOOD but not SAWMILL')
        PLACES.append('SAWMILL')

    if(('FISH' in RESOURCES)and((not 'RIVERX' in RESOURCES)and(not 'RIVERY' in RESOURCES))):
        print('inconsistency FISH but not RIVER')
        RESOURCES.append('RIVERX')

    if(('FISH' in RESOURCES)and(not 'MARKET' in PLACES)):
        print('inconsistency FISH but not MARKET')
        PLACES.append('MARKET')

    if(('LEATHER' in RESOURCES)and(not 'LEATHER_SHOP' in PLACES)):
        print('inconsistency LEATHER but not LEATHER_SHOP')
        PLACES.append('LEATHER_SHOP')

    if(('HORSE' in RESOURCES)and(not 'STABLE' in PLACES)):
        print('inconsistency HORSE but not STABLE')
        PLACES.append('STABLE')

    if((('SILK' in RESOURCES) or ('WOOL' in RESOURCES)) and(not 'TAILOR_SHOP' in PLACES)):
        print('inconsistency SILK or WOOL but not TAILOR_SHOP')
        PLACES.append('TAILOR_SHOP')

    if(('WEAPON_SHOP' in PLACES)and(not 'CAVE' in RESOURCES)):
        print('inconsistency WEAPON_SHOP but not CAVE')
        RESOURCES.append('CAVE')

    if(('SMITHY' in PLACES)and(not 'CAVE' in RESOURCES)):
        print('inconsistency SMITHY but not CAVE')
        RESOURCES.append('CAVE')

    if((('LEATHER' in RESOURCES) or ('PIG' in RESOURCES)) and(not 'BUTCHER_SHOP' in PLACES)):
        print('inconsistency LEATHER or PIG but not BUTCHER_SHOP')
        PLACES.append('BUTCHER_SHOP')

    if((WEALTH<5)and(not 'SANCTUARY' in PLACES)):
        print('inconsistency ORRIBLE WEALTH but not SANCTUARY')
        PLACES.append('SANCTUARY')

    if((WEALTH>4)and(not 'BAKERY' in PLACES)):
        print('inconsistency HUMAN WEALTH but not BAKERY')
        PLACES.append('BAKERY')

    if((WEALTH>4)and(not 'BARRACK' in PLACES)):
        print('inconsistency HUMAN WEALTH but not BARRACK')
        PLACES.append('BARRACK')

    if((WEALTH>5)and(not 'HERBALISTS' in PLACES)):
        print('inconsistency HIGH WEALTH but not HERBALISTS')
        PLACES.append('HERBALISTS')

    if((WEALTH>6)and(not 'BUTCHER_SHOP' in PLACES)):
        print('inconsistency HIGH WEALTH but not BUTCHER_SHOP')
        PLACES.append('BUTCHER_SHOP')

    if((WEALTH>7)and(not 'WALL' in PLACES)):
        print('inconsistency HIGH WEALTH but no WALL')
        RESOURCES.append('WALL')

    if((WEALTH>3)and(PLACES.count('INN')<WEALTH/2)):
        print('inconsistency FEW INN despite GOOD WEALTH')
        for i in range(0,int(WEALTH/2-PLACES.count('INN'))):
            PLACES.append('INN')

    if((WEALTH>3)and(PLACES.count('CHURCH')<WEALTH)):
        print('inconsistency FEW CHURCH despite GOOD WEALTH')
        for i in range(0,WEALTH-PLACES.count('CHURCH')):
            PLACES.append('CHURCH')

    if((WEALTH>7)and(not 'MARKET' in PLACES)):
        print('inconsistency HIGH WEALTH but not MARKET')
        PLACES.append('MARKET')

    if((WEALTH>7)and(not 'CHURCH' in PLACES)):
        print('inconsistency HIGH WEALTH but not CHURCH')
        PLACES.append('CHURCH')

    if((WEALTH>7)and(not 'THEATRE' in PLACES)and(INHABITANTS>2000)):
        print('inconsistency HIGH WEALTH but not THEATRE and lot of INHABITANTS')
        PLACES.append('THEATRE')

    if((WEALTH>7)and(not 'ARENA' in PLACES)and(INHABITANTS>2500)):
        print('inconsistency HIGH WEALTH but not ARENA and lot of INHABITANTS')
        PLACES.append('ARENA')

    if((WEALTH>8)and(not 'WHOREHOUSE' in PLACES)):
        print('inconsistency VERY HIGH WEALTH but not WHOREHOUSE')
        PLACES.append('WHOREHOUSE')

    if((WEALTH>8)and(not 'CATHEDRAL' in PLACES)):
        print('inconsistency VERY HIGH WEALTH but not CATHEDRAL')
        PLACES.append('CATHEDRAL')

    if((WEALTH>8)and(not 'CASTLE' in PLACES)):
        print('inconsistency VERY HIGH WEALTH but not CASTLE')
        PLACES.append('CASTLE')

    if((INHABITANTS>3000)and(not 'CASTLE' in PLACES)):
        print('inconsistency VERY HIGH INHABITANTS but not CASTLE')
        PLACES.append('CASTLE')

    if((INHABITANTS>3000)and(not 'MARKET' in PLACES)):
        print('inconsistency VERY HIGH INHABITANTS but not MARKET')
        PLACES.append('MARKET')


    if((INHABITANTS>3000)and(PLACES.count('BAKERY')<(INHABITANTS/2000))):
        print('inconsistency VERY HIGH INHABITANTS but too FEW BAKERY')
        for i in range(0,int((INHABITANTS/2000)-PLACES.count('BAKERY'))):
            PLACES.append('BAKERY')

    if((INHABITANTS>3000)and(PLACES.count('BUTCHER_SHOP')<(INHABITANTS/2000))):
        print('inconsistency VERY HIGH INHABITANTS but too FEW BUTCHER_SHOP')
        for i in range(0,int((INHABITANTS/3000)-PLACES.count('BUTCHER_SHOP'))):
            PLACES.append('BUTCHER_SHOP')



    #now some other paramethers from   http://www222.pair.com/sjohn/blueroom/demog.htm
    # (PLACE, SV)
    '''
    OTHER_PLACE=(
        ('BAKERY',800),
        ('BARBER_SHOP',350),
        ('BATHER',1900),
        ('BEER_SHOP',1400),
        ('BLEACHER_SHOP',2100),
        ('BOOKBINDERS_SHOP',3000),
        ('BOOK_SHOP',6300),
        ('BUCKLE_MAKER_SHOP',1400),
        ('BUTCHER_SHOP',1200),
        ('CARPENTERY',550),
        ('CHANDLERS',700),
        ('CHICKEN_BUTCHER_SHOP',1000),
        ('COOPERS',700),
        ('COPYIST',2000),
        ('CUTLER',2300),
        ('DOCTOR',1700),
        ('FISHMONGER',1200),
        ('FURRIERS',250),
        ('GLOVEMAKER_SHOP',2400),
        ('HARNESS_MAKERS',2000),
        ('HAY_MERCHANT',2300),
        ('HEADGEAR',950),
        ('ILLUMINATOR',3900)
        ('INN',2000),
        ('JEWELRY',400),
        ('LOCKSMITH',1900),
        ('MAGIC_SHOPS',2800),
        ('MAIDSERVANTS',250),
        ('MASONS',500),
        ('MERCERS',700),
        ('OLD-CLOTHES',400),
        ('PAINTERS',1500),
        ('PASTRYCOOKS',500),
        ('PLASTERER',1400),
        ('PURSE_SHOP',1100),
        ('ROOFER',1800),
        ('ROPEMAKER',1900),
        ('RUGMAKER',2000),
        ('SADDLERY',1000),
        ('SCABBARDMAKERS',850),
        ('SCULPTOR',2000),
        ('SHOEMAKERS',150),
        ('SMITHY',1500),
        ('SPICE_SHOP',1400),
        ('TAILOR_SHOP',250),
        ('TANNER_SHOP',2000),
        ('TAVERN',400),
        ('WATERCARRIERS',850),
        ('WEAVERS',600),
        ('WINE-SELLERS',900),
        ('WOODCARVER_SHOP',2400),
        ('WOODSELLERS',2400),
    )
    '''
    OTHER_PLACE=(
        ('BAKERY',800),
        ('BEER_SHOP',1400),
        ('BOOKBINDERS_SHOP',3000),
        ('BOOK_SHOP',6300),
        ('BUTCHER_SHOP',1200),
        ('CHICKEN_BUTCHER_SHOP',1000),
        ('COPYIST',2000),
        ('DOCTOR',1700),
        ('FISHMONGER',1200),
        ('INN',2000),
        ('JEWELRY',2000),
        ('MAGIC_SHOPS',2800),
        ('SADDLERY',1000),
        ('SCULPTOR',2000),
        ('SMITHY',1500),
        ('SPICE_SHOP',1400),
        ('TAILOR_SHOP',800),
        ('TANNER_SHOP',2000),
        ('TAVERN',400),
    )

    for other in OTHER_PLACE:
        if(PLACES.count(other[0])<INHABITANTS/other[1]):
            for i in range(0,int((INHABITANTS/other[1])-PLACES.count(other[0]))):
                PLACES.append(other[0])


