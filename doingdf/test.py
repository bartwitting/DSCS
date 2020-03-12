import datetime

now = datetime.datetime.now()



#ranges

decibel_low= range(0,50)
decibel_medium= range(50,70)
decibel_noise= range(70,90)
decibel_loud= range(90,151)

decibel_list= [("decibel_low",decibel_low), ("decibel_medium",decibel_medium), ("decibel_noise",decibel_noise), ("decibel_loud",decibel_loud)]

people_little= range(0,10)
people_medium= range(10,20)
people_busy= range(20,30)
people_crowded= range(30,101)

people_list= [('people_little',people_little), ('people_medium',people_medium), ('people_busy',people_busy), ('people_crowded',people_crowded)]

temperature_freezing= range(-10, 5)
temperature_cold= range(5,15)
temperature_warm= range(15,25)
temperature_hot= range(25,45)

temperature_list = [('temperature_freezing',temperature_freezing), ('temperature_cold',temperature_cold) , ('temperature_warm',temperature_warm), ('temperature_hot',temperature_hot)]

rain_little= range(0,20)
rain_some= range(20,40)
rain_medium= range(40,60)
rain_much= range(60,80)
rain_heavy = range(80,101)

rain_list= [('rain_little',rain_little ), ('rain_some',rain_some), ('rain_medium',rain_medium), ('rain_much',rain_much), ('rain_heavy',rain_heavy)]

clouds_little= range(0,20)
clouds_some= range(20,40)
clouds_medium= range(40,60)
clouds_much= range(60,80)
clouds_only= range(80,101)

clouds_list= [('clouds_little',clouds_little), ('clouds_some',clouds_some), ('clouds_medium',clouds_medium), ('clouds_much',clouds_much), ('clouds_only',clouds_only)]

time_early= range(9,11)
time_beforelunch= range(11,13)
time_afterlunch= range(13,17)
time_closing= range(17,18)

time_list= [('time_early',time_early), ('time_beforelunch',time_beforelunch), ('time_afterlunch',time_afterlunch), ('time_closing',time_closing)]

def Parameter_ranges(decibel, people, temperature, rain, clouds, time):
    ruis_range= str
    mensen_range = str
    temp_range = str
    regen_range = str
    wolk_range = str
    uur_range = str

    for ruis in decibel_list:
        for db in ruis[1]:
            if db == decibel:
                ruis_range = ruis[0]

    for mensen in people_list:
        for mens in mensen[1]:
            if mens==people:
                mensen_range = mensen[0]

    for temp in temperature_list:
        for c in temp[1]:
            if c==temperature:
                temp_range = temp[0]

    for regen in rain_list:
        for m in regen[1]:
            if m==rain:
                regen_range = regen[0]

    for wolk in clouds_list:
        for w in wolk[1]:
            if w==clouds:
                wolk_range = wolk[0]

    for uur in time_list:
        for s in uur[1]:
            if s==time:
                uur_range = uur[0]

    return ruis_range, mensen_range, temp_range, regen_range, wolk_range, uur_range
