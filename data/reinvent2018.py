#!/usr/bin/env python3
import os

track = os.path.join(os.getcwd(), 'data', 'reinvent2018.png')

target_points = [(6.461017873707842, 0.6880578326692007), (6.513886439910145, 0.6917869902861352),
                 (6.7062222853811955, 0.7038161614821337), (6.8417877118114365, 0.7243997550836263),
                 (7.006286573591471, 0.7588117589051223), (7.151475820681036, 0.8122097996316212),
                 (7.2214064017967035, 0.8751065652956163), (7.4680469146403015, 1.0037185508282644),
                 (7.528010351788048, 1.146150858759214), (7.528699863639062, 1.2748812463906218),
                 (7.689691981759969, 1.5345926580097675), (7.728888069470197, 1.8892638886926827),
                 (7.692518602130955, 2.228561087145163), (7.549869254110648, 2.4384057538460246),
                 (7.360110488915774, 2.763170903359196), (7.103613724760411, 2.9653756744292155),
                 (6.784508899007659, 3.1711012517827197), (6.496110449079708, 3.2346328046339803),
                 (6.085768651954058, 3.489472238868241), (5.5260599813661315, 3.4660003015732457),
                 (5.33654704033823, 3.3366623017827903), (5.163236667744558, 3.207524167660189),
                 (4.626543018483973, 3.1282963599586404), (4.092728535429521, 3.3703748558215287),
                 (4.001121969780925, 3.482763638518189), (3.6665939940763446, 3.4090644155940097),
                 (3.5707663664692615, 3.587777262672379), (3.433488173803766, 3.791733942750928),
                 (3.139644149294831, 4.096426738718088), (2.890125470779159, 3.7836970294088266),
                 (2.8110045575773057, 4.499832029419236), (2.5003276964136627, 4.498718163592657),
                 (2.5003276964136627, 4.498718163592657), (2.415839284266728, 4.728265904982661),
                 (2.204359067157784, 4.787654571338813), (1.9468757993904031, 4.815257834492364),
                 (1.7144196614082232, 5.327292903753738), (1.5586180971261494, 5.258828069196492),
                 (1.1209191146490554, 5.251590107522398), (0.9339249465944577, 5.061712212148723),
                 (0.6664027012058624, 4.788610860372954), (0.3639885210834488, 4.340023544041322),
                 (0.26810231700495724, 4.040801759705744), (0.24455771783760571, 3.888204037448009),
                 (0.26979304514547486, 3.8810593942904537), (0.2534210665736296, 3.7805895401723992),
                 (0.2607343572973675, 3.871452639704585), (0.21591246434980338, 3.743970932934269),
                 (0.7316196323127645, 3.819658838269335), (0.24017037950053255, 3.3547472166425614),
                 (0.6334741151623569, 3.617867807094588), (0.6116914571884705, 2.7967209786723224),
                 (0.8767142517759999, 2.6705225050239383), (0.9126237137711688, 2.5150506992691817),
                 (0.9380374746317686, 2.4195933679559642), (1.0212099341560645, 2.0181787127447155),
                 (1.0430635528690946, 1.9127067467720549), (1.0936256517149217, 1.668679245468863),
                 (1.2088473861872933, 1.1674873418524767), (1.2363710112296433, 1.117224217460086),
                 (1.7904703275551124, 0.5170919210197327), (2.419351943156177, 0.26963284584109304),
                 (3.6300023417267235, 0.6834498837610459), (4.189995119968753, 0.6836500863232341),
                 (4.500002230529587, 0.6837609167129147), (4.549995073956144, 0.6837787896136626),
                 (5.320002125723089, 0.6840540742077795), (5.420002112941809, 0.6840898251217875),
                 (5.7800020669292005, 0.684218528412216), (6.289747858140073, 0.6921400142174)]


class RangeDict(dict):
    def __getitem__(self, item):
        if not isinstance(item, range):
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError(item)
        else:
            return super().__getitem__(item)


waypoints = [(2.909995283569139, 0.6831924746239328), (3.3199952311658905, 0.6833390533713652),
             (3.41999521838461, 0.6833748042853732), (3.6300023417267235, 0.6834498837610459),
             (4.189995119968753, 0.6836500863232341), (4.500002230529587, 0.6837609167129147),
             (4.549995073956144, 0.6837787896136626), (5.320002125723089, 0.6840540742077795),
             (5.420002112941809, 0.6840898251217875), (5.7800020669292005, 0.684218528412216),
             (6.289747858140073, 0.6921400142174), (6.460906484698166, 0.7123063542781353),
             (6.5136980596947165, 0.7210294115664316), (6.704287871536597, 0.799598672280553),
             (6.836281775656231, 0.8817004790362547), (6.991663362669656, 1.0062653214908401),
             (7.1142074641408275, 1.1693225137564909), (7.165830682349035, 1.263426756737598),
             (7.280019741788613, 1.7628308313393968), (7.272892208655982, 1.8132370038722583),
             (7.265960701310593, 1.8622568749360433), (7.1045747673751585, 2.3014874894475916),
             (7.011749008840918, 2.419260292916218), (6.727273712845888, 2.6474924751765463),
             (6.536921216759571, 2.7266447610626687), (6.079802178702642, 2.773360773339069),
             (5.919813651266964, 2.772005974951175), (5.719827991972368, 2.7703124769663074),
             (5.670000926947205, 2.7698905365406308), (5.200034627604903, 2.765910816276192),
             (5.049876033335467, 2.7646392587170006), (5.002030872389276, 2.768980714618128),
             (4.942709994269048, 2.775327848322301), (4.561340171137485, 2.898322513024676),
             (4.258533108743229, 3.166955220685885), (4.092728535429521, 3.3703748558215287),
             (4.001121969780925, 3.482763638518189), (3.774000078716213, 3.761411273431655),
             (3.6823935130676184, 3.8738000561283137), (3.5490587458571623, 4.037383660336441),
             (3.2758532950668884, 4.333295323360169), (3.1911463583891155, 4.385684825652305),
             (3.0954945192403103, 4.435922305057415), (2.9549738926202442, 4.484413606024224),
             (2.8089822299540046, 4.500038654567632), (2.8110045575773057, 4.499832029419236),
             (2.5003276964136627, 4.498718163592657), (2.249377566090162, 4.491428972830993),
             (1.990177178741659, 4.483900142037221), (1.7395172672798365, 4.476619381080485),
             (1.1871156114665855, 4.391792930201858), (1.1054389398706574, 4.3402307341807065),
             (0.7316196323127645, 3.819658838269335), (0.7080468873794841, 3.5295953182618844),
             (0.8747319412102282, 2.7251244177375193), (0.8863119620897287, 2.6692358445815714),
             (0.9180990438541362, 2.5158220758940644), (0.9380374746317692, 2.4195933679559642),
             (1.0212099341560652, 2.0181787127447155), (1.043063552869095, 1.912706746772055),
             (1.0936256517149223, 1.6686792454688633), (1.219724413480236, 1.169889412099395),
             (1.2404620134668318, 1.1182110370035536), (1.286611404297767, 1.0270193376917442),
             (1.3195344250237366, 0.9895904728963364), (1.3897426105955222, 0.9097735962139227),
             (1.4563853812178036, 0.8435308547287804), (1.4996428710531535, 0.8193608401945228),
             (2.0400025449490777, 0.6828814442283201), (2.7500024542019887, 0.6831352757177762)]


targets_refs = RangeDict({
    range(0, 22+1): ('avg', 12),
    range(23, 24+1): ('end', 13),
    range(25, 28+1): ('wtd_avg', 13),
    range(29, 29+1): ('avg', 13),
    range(30, 31+1): ('end', 16),
    range(32, 32+1): ('end', 15),
    range(33, 35+1): ('wtd_avg', 15),
    range(36, 42+1): ('avg', 15),
    range(43, 43+1): ('avg', 14),
    range(44, 44+1): ('avg', 12),
    range(45, 45+1): ('avg', 11),
    range(46, 46+1): ('avg', 9),
    range(47, 47+1): ('avg', 8),
    range(48, 48+1): ('end', 5),
    range(49, 49+1): ('avg', 6),
    range(50, 59+1): ('avg', 4),
    range(60, 61+1): ('wtd_avg', 9),
    range(62, 69+1): ('end', 12)
})