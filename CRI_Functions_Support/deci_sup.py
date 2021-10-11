#import dec_exe_file
import CRI_Functions_Support.dec_exe_file

def dec_sup (al_ot,dis,CR,alot_os,tvhead):
    Msg2 = ' '
    Msg3 = ' '
    Msg4 = ' '
    Msg5 = ' '
    #print('Alpha OT :', alot_os)
    #print('Distance between : ',dis)
    if dis < 0.2429:

        Msg1 = '--CAUTION--'
        if al_ot > 180 and al_ot < 360:
            Msg2 = 'We are the give away ship'
            if CR > 0.6:
                Msg3 = 'Action Required'
                if alot_os > 5 and alot_os < 67.5:
                    Msg4 = 'large angle crossing at STb : '
                    if tvhead > 180 and tvhead <360:
                        Msg5 = 'Rudder 40 for 1 min to STb'
                    elif tvhead > 0 and tvhead < 180:
                        Msg5 = 'Rudder 40 for 1 min to Port'
                elif alot_os > 247.5 and alot_os <355:
                    Msg4 = 'large angle crossing at port : '
                    if tvhead > 180 and tvhead <360:
                        Msg5 ='Rudder 40 for 1 min to STb'
                    elif tvhead > 0 and tvhead < 180:
                        Msg5 ='Rudder 40 for 1 min to Port'
                elif alot_os > 67.5 and alot_os < 112.5:
                    Msg4 = 'Small angle cross at Stb : '
                    Msg5 = 'Speed Decrease by 35%'
                elif alot_os > 210 and alot_os <247.5:
                    Msg4 = 'Small angle cross at port :'
                    Msg5 = 'Speed Decrease by 35%'
                else:
                    Msg5 = 'NIL'
                    Msg4 = 'NIL'
            else:
                Msg3 = 'No Action Required'

        else:
            Msg2 = 'We are not the give away ship'
    else:
        Msg1 = 'Keep The Original Course'

    data = Msg1,Msg2,Msg3,Msg4,Msg5

    return data

