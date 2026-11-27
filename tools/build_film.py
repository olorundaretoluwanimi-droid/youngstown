#!/usr/bin/env python3
"""lines.json + cleaned narration durations + the shot list below → film.json (scenes, voice starts, subtitles, credits) and audio/cues.json.
Told as a court case: black + distant whistle, the charge (cold open), the Mill Town title (8 s, spliced in at the finish), then nine parts,
each opening on a case caption card (the knock lands on it) that carries the part's first line. Witness cards hold in silence.
Shot values: a dict (one scene for the line), or {'cont': True, ...} to keep the previous scene and add items / pans / mills / set values.
'at' values: seconds after the line starts, or a negative fraction of the line."""
import json, os, copy
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = json.load(open(os.path.join(D, 'audio/lines.json'), encoding='utf-8'))
DUR = json.load(open(os.environ.get('DURFILE') or os.path.join(D, 'audio/vo/dur.json')))
GAP, QGAP, OPEN, TITLE, END = 0.55, 1.4, 1.0, 8.0, 16.0
PRECARD, XF = 1.1, .7   # extra quiet before each case card; the card dissolves into the part's first picture
PART = {'hook': 0, 'p1': 1, 'p2': 2, 'p3': 3, 'p4': 4, 'p5': 5, 'p6': 6, 'p7': 7, 'p8': 8, 'p9': 9}
CARD = {'p1': ('Opening Statement', 'what Youngstown was'), 'p2': ('Exhibit A', 'what the town built'), 'p3': ('Exhibit B', 'the merger'),
        'p4': ('The Witnesses', 'a town tries to buy its mill'), 'p5': ('Exhibit C', 'the promise'), 'p6': ('The Trial', 'Youngstown, March 1980'),
        'p7': ('The Defence', 'U.S. Steel’s case'), 'p8': ('The Verdict', 'what the courts decided'), 'p9': ('The Jury', 'you')}
QUIET = {'h08', 'a12', 'b11', 'c12', 'd14', 'e16', 'f12', 'g12', 'h21', 'j11', 'j12'}

def I(k, **o): return dict(k=k, **o)
def hero(img, tag, **k): return dict(type='hero', img=img, tag=tag, **k)
def hclip(c, tag, **k): return dict(type='hero', clip=c, tag=tag, **k)
def clip(clips, tag, **k): return dict(type='clip', clips=clips if isinstance(clips, list) else [clips], tag=tag, **k)
def doc(head, text, **k): return dict(type='doc', head=head, text=text, **k)
def hot(date, who, text, **k): return dict(type='hotline', date=date, who=who, text=text, **k)
def typ(lines, **k): return dict(type='type', lines=lines, **k)
def cont(**k): return dict(cont=True, **k)
def EX(no, side='p', x=1560, y=800, at=-.45): return I('ex', no=no, side=side, x=x, y=y, at=at)
ST44 = 'FILM · STEEL TOWN · OFFICE OF WAR INFORMATION, 1944 (NATIONAL ARCHIVES, PUBLIC DOMAIN)'
NARA = ' · 1918 (NATIONAL ARCHIVES, PUBLIC DOMAIN)'
PALMER = 'ALFRED T. PALMER · REPUBLIC STEEL, YOUNGSTOWN · 1941 (LIBRARY OF CONGRESS, PUBLIC DOMAIN)'
SIXTH = '631 F.2d 1264 (6th Cir. 1980) · PUBLIC RECORD'
NDO = '492 F. Supp. 1 (N.D. Ohio 1980) · PUBLIC RECORD'
LYND = 'AS QUOTED IN STAUGHTON LYND, THE FIGHT AGAINST SHUTDOWNS (1982)'
FED = 'FEDERAL BUILDING, DOWNTOWN YOUNGSTOWN (1917) · 2009 · PHOTO: BFDHD (CC BY-SA 3.0)'
SIGN = 'YOUNGSTOWN SHEET AND TUBE, ABANDONED · 2006 · PHOTO: STU_SPIVACK (CC BY-SA 2.0)'
CAMP = 'CAMPBELL WORKS AT NIGHT · POSTCARD Y-68 (PUBLIC DOMAIN)'
STATEMENT = ('Youngstown Sheet and Tube Company, a subsidiary of Lykes Corporation, announced today that it is implementing steps immediately to concentrate '
             'a major portion of its steel production at the *Indiana* *Harbor* *Works* near Chicago. … The production cut-back at the Campbell Works will require '
             'the lay-off or termination of *approximately* *5,000* *employees* in the Youngstown area.')
TOWNS_ALL = [['Warren', 0], ['Niles', 0], ['McDonald', 0], ['Girard', 0], ['Youngstown', 0], ['Campbell', 0], ['Struthers', 0], ['Lowellville', 0]]
S = {
 # ── the charge ──
 'h01': hero('campbell_night', CAMP, era='c', fadeIn=1.2, items=[I('stamp', text='19 SEP 1977', x=1520, y=180, s=60, at=-.25)]),
 'h02': doc('YOUNGSTOWN SHEET AND TUBE COMPANY · STATEMENT', STATEMENT, head2='READ TO THE UNION PRESIDENTS · MONDAY, 19 SEPTEMBER 1977', img='yst_sign',
            cite='TEXT ' + LYND, until=-.98, stamp='5,000', stampAt=-.8),
 'h03': cont(),
 'h04': dict(type='line', at=.1, draw=2.6, marks=[[1930, 'PEAK · 1930'], [2020, '2020']]),
 'h05': hero('yst_sign', SIGN, items=[I('stamp', text='1979', x=1560, y=200, s=70, at=.2)]),
 'h06': hero('fed_bldg', FED, items=[I('drop', text='LOCAL 1330 v. U.S. STEEL', x=960, y=760, s=84, al='center', at=-.25)]),
 'h07': typ(['The charge.', 'The evidence.', 'The witnesses.', 'The defence.', 'The verdict.'], s=78, step=.75, clip='c_gate', dim=.82, at=.6),
 'h08': hclip('c_shift', ST44, items=[I('drop', text='This is Mill Town.', x=960, y=860, s=80, al='center', at=-.5)]),
 # ── part 1 · opening statement ──
 'a02': dict(type='river', riverDur=3.2, cam=[[0, 960, 540, 1.0, 0]], towns=[['Warren', .3], ['Niles', -.25], ['Girard', -.35], ['Youngstown', -.5], ['Campbell', -.62], ['Struthers', -.7], ['Lowellville', -.8]]),
 'a03': hero('birdseye1882', 'PANORAMIC VIEW OF YOUNGSTOWN · 1882 (LIBRARY OF CONGRESS, PUBLIC DOMAIN)', era='a', z=[1.0, 1.18], fx=.5, fy=.45),
 'a04': hero('oreyard1930', 'ORE YARD, YOUNGSTOWN SHEET AND TUBE · c. 1930 (PUBLIC DOMAIN)', era='b',
             items=[I('stamp', text='1900', x=1560, y=200, s=70, at=.3), I('count', to=600000, pre='$', x=1450, y=860, s=100, at=-.5, dur=1.2, label='RAISED BY YOUNGSTOWN MEN')]),
 'a05': hero('bf1918', 'BLAST FURNACE AND POWER PLANT, YOUNGSTOWN SHEET AND TUBE' + NARA, era='b', fy=.4),
 'a06': dict(type='pano', img='ohioworks1905', tag='OHIO STEEL WORKS AND FURNACES, WEST SIDE · 1905 (LIBRARY OF CONGRESS, PUBLIC DOMAIN)', bh=540, grade='b',
             items=[I('stamp', text='1901', x=1640, y=880, s=70, at=.4), I('txt', text='UNITED STATES STEEL CORPORATION', x=120, y=900, s=34, f='Mono', w=600, at=-.6)]),
 'a07': dict(type='river', riverDur=.01, cam=[[0, 960, 540, 1.0, 0], [3, 930, 600, 1.6, 0]], towns=TOWNS_ALL, mills=[['ohio', .0], ['mcd', .5]]),
 'a08': cont(mills=[['brier', .4]], items=[I('stamp', text='20 SEP 1918', x=1540, y=200, s=60, at=-.4)]),
 'a09': hero('n_bf3', 'BLAST FURNACES, YOUNGSTOWN SHEET AND TUBE' + NARA, era='b', cap='A YOUNGSTOWN FURNACE IN 1918 · NOT JENNY',
             items=[I('drop', text='“Jenny”', x=1500, y=560, s=130, al='center', at=-.55)]),
 'a10': dict(type='river', riverDur=.01, cam=[[0, 930, 600, 1.35, 0], [4, 960, 540, 1.0, 0]], towns=TOWNS_ALL, mills=[['ohio', 0], ['mcd', 0], ['brier', 0], ['camp', .3]]),
 'a11': dict(type='pano', img='panorama1910', tag='YOUNGSTOWN · c. 1910 (LIBRARY OF CONGRESS, PUBLIC DOMAIN)', bh=540, grade='b',
             items=[I('count', to=170002, x=1460, y=900, s=96, at=.3, dur=1.6, label='PEOPLE · 1930 CENSUS')]),
 'a12': typ(['What did the mills give this town?', 'And what did the town give back?'], s=66, step=1.6, img='flag1918', fx=.7, dim=.8,
            tag='CENTRAL SQUARE, CROWD OF 30,000 · 1918 (NATIONAL ARCHIVES, PUBLIC DOMAIN)'),
 # ── part 2 · exhibit A ──
 'b02': hclip('c_houses', ST44, items=[I('stamp', text='1944', x=1560, y=200, s=70, at=.4)]),
 'b03': clip(['c_shift'], ST44, caps=['YOUNGSTOWN · 1944']),
 'b04': clip(['c_bridge', 'c_family'], ST44, caps=['GOING TO WORK · 1944', 'AT HOME · 1944']),
 'b05': clip(['c_pour', 'c_iron'], ST44, caps=['MOLTEN IRON · 1944', 'MOLTEN IRON · 1944']),
 'b06': hero('n_crowd', 'STEELWORKERS AT YOUNGSTOWN SHEET AND TUBE' + NARA, era='b', items=[EX('A-1', at=-.5)]),
 'b07': clip(['c_home', 'c_football'], ST44, caps=['A STEELWORKER’S HOME · 1944', 'FRIDAY NIGHT · 1944']),
 'b08': hero('n_charge', 'CHARGING MOLTEN IRON INTO AN OPEN HEARTH, SHEET AND TUBE' + NARA, era='b',
             items=[I('count', to=27000, pre='≈ ', x=1440, y=250, s=100, at=.6, dur=1.4, label='SHEET & TUBE · 1950'), EX('A-2', at=-.6)]),
 'b09': hclip('c_face', ST44),
 'w02': dict(type='witness', img='st_worker', imgTag='A STEELWORKER IN STEEL TOWN, 1944 · NOT ED MANN'),
 'b10': hero('palmer_slag2', PALMER, era='s', box=[460, 50, 1000, 870], fy=.5, items=[EX('A-3', x=1420, y=820, at=-.55)]),
 'b11': typ(['So who owned all this?'], s=96, clip='c_committee', dim=.8),
 # ── part 3 · exhibit B ──
 'c02': typ(['Youngstown Sheet and Tube', '+ Lykes Corporation'], s=88, step=.9, sub='a shipping company from New Orleans', img='larry1918', era='b', dim=.84,
            items=[I('stamp', text='1969', x=1560, y=200, s=80, at=.5)]),
 'c03': hero('viaduct_pc', 'VIADUCT AT YOUNGSTOWN SHEET AND TUBE · POSTCARD (PUBLIC DOMAIN)', era='c', items=[EX('B-1')]),
 'c04': hero('molds1918', 'STRIPPING MOLDS FROM STEEL INGOTS, SHEET AND TUBE' + NARA, era='b', items=[EX('B-2')]),
 'c05': hero('n_bf4', 'STEEL MANUFACTURE AT YOUNGSTOWN SHEET AND TUBE' + NARA, era='b', box=[460, 50, 1000, 870]),
 'c06': doc('NATIONAL LABOR RELATIONS BOARD · SWORN STATEMENT', 'Bill Sferra, president of Local 1418 at the Campbell Works, stated under oath that Sheet & Tube executives '
            'told him on August 11 and 25, *“We’ll* *make* *it.”* Ed Mann, president of Local 1462 at Brier Hill, said he was told *“it* *was* *tough* *but* *they* *were* *going* *to* *make* *it.”*',
            head2='AUGUST 1977', cite=LYND),
 'c07': typ(['Monday, 19 September 1977.'], s=96, redLine=0, clip='c_goggles', dim=.82),
 'c08': doc('YOUNGSTOWN SHEET AND TUBE COMPANY · STATEMENT', STATEMENT, head2='19 SEPTEMBER 1977', cite='TEXT ' + LYND, at=.1, until=-.95, items=[EX('B-3', x=1640, y=880, at=-.3)]),
 'c09': hero('yst_sign', SIGN, z=[1.15, 1.3], fx=.3),
 'c10': typ(['Black Monday.'], s=170, redLine=0, img='campbell_night', era='c', dim=.75),
 'c11': typ(['185 clergy.', 'One letter.'], s=110, step=.9, sub='Thanksgiving, 1977', img='centralsq_pc', era='c', dim=.82),
 'c12': typ(['Could the town buy', 'its own mill back?'], s=96, step=.8, img='n_ladle', era='b', dim=.82),
 # ── part 4 · the witnesses ──
 'd02': typ(['Bishop James Malone', 'Bishop John Burt'], s=90, step=1.4, sub='Catholic, Youngstown  ·  Episcopal, Ohio', clip='c_orch', dim=.85),
 'd03': hero('campbell_night', CAMP, era='c', z=[1.1, 1.3], items=[I('txt', text='TO BE REOPENED · OWNED BY ITS WORKERS AND ITS COMMUNITY', x=960, y=1000 - 80, s=30, f='Mono', w=600, al='center', at=-.6)]),
 'd04': typ(['Hundreds of millions', 'of dollars.'], s=100, step=.6, clip='c_mill', dim=.8),
 'd05': dict(type='passbook', img='flag1918', countAt=99),
 'd06': cont(set={'countAt': .1}),
 'd07': hero('usgs1970', 'YOUNGSTOWN FROM THE AIR · 31 MARCH 1970 (USGS, PUBLIC DOMAIN)', era='b', box=[460, 50, 1000, 870], z=[1.0, 1.3]),
 'd08': typ(['29 March 1979'], s=110, redLine=0, sub='a press conference'),
 'd09': doc('U.S. DEPARTMENT OF COMMERCE · ECONOMIC DEVELOPMENT ADMINISTRATION',
            'The *“overriding* *difficulty”* in the Coalition’s proposal was that in Phases I and II it would require *$245* *million* of Federal government loan guarantees, '
            '*“well* *in* *excess* *of* *the* *$100* *million* amount which had been set as the maximum loan guarantee for any one company under the special steel program.”',
            head2='LETTER OF FRIDAY, 30 MARCH 1979 · TO BISHOP MALONE AND THE MAYOR OF YOUNGSTOWN', cite=LYND + ' · NOT THE FULL LETTER', stamp='30 MAR 1979', stampAt=-.3),
 'd10': typ(['The answer was no.'], s=120),
 'd11': typ(['Pittsburgh: 75 miles.'], s=100, sub='the national union kept its distance', clip='c_skyline', dim=.8),
 'd12': dict(type='river', riverDur=.01, cam=[[0, 960, 540, 1.0, 0]], towns=TOWNS_ALL, mills=[['ohio', 0], ['mcd', 0], ['brier', 0, -.75], ['camp', 0, 'off']],
             closed={'camp': 'CLOSED · 1977', 'brier': 'CLOSED · 1979'}),
 'd13': cont(items=[I('stamp', text='1,500', x=1560, y=880, s=70, at=.2)]),
 'd14': dict(type='river', riverDur=.01, cam=[[0, 960, 540, 1.0, 0], [3, 910, 590, 1.7, 0]], towns=TOWNS_ALL, mills=[['ohio', 0], ['mcd', 0], ['brier', 0, 'off'], ['camp', 0, 'off']],
             closed={'camp': 'CLOSED · 1977', 'brier': 'CLOSED · 1979'}),
 # ── part 5 · exhibit C ──
 'e02': dict(type='pano', img='ohioworks1905', tag='OHIO WORKS · 1905 (LIBRARY OF CONGRESS, PUBLIC DOMAIN)', bh=540, grade='b', from_=0,
             items=[I('count', to=3500, pre='≈ ', x=1500, y=900, s=90, at=.3, dur=1.2, label='WORKERS · OHIO + McDONALD'), EX('C-1', x=300, y=880, at=-.3)]),
 'e03': hot('', '', '', head='U.S. STEEL · YOUNGSTOWN WORKS · HOT LINE', head2='RECORDED MESSAGES, 1977–1979 · LATER READ INTO THE COURT RECORD', cite=SIXTH),
 'e04': hot('1 SEP 1977', 'Bill Ashton, superintendent', 'Hello, this is Bill Ashton. In response to many rumors, I want to tell you that there are *no* *immediate* *plans* '
            '*to* *permanently* *shut* *down* either the Ohio Works or McDonald Mills.', head2='COMPLAINT ¶10a · ' + SIXTH),
 'e05': hot('1 SEP 1977', 'Bill Ashton, superintendent', 'Ohio Works and McDonald Mills are faced with very serious profit problems … '
            'The continued operation of these plants is *absolutely* *dependent* *upon* *their* *being* *profit-makers.*', head2='COMPLAINT ¶10a · ' + SIXTH),
 'e06': typ(['Bill Kirwan'], s=110, sub='superintendent, Youngstown Works, from 1 February 1978', clip='c_tap', dim=.84),
 'e07': hot('7 APR 1978', 'Bill Kirwan, superintendent', 'Hello, this is Bill Kirwan. I want to share the good news with all of you. In the month of March, '
            'for the first [time] in a long long time, the Youngstown Works *earned* *a* *profit* for the United States Steel Corporation.', head2='COMPLAINT ¶10h · ' + SIXTH),
 'e08': hot('7 APR 1978', 'Bill Kirwan, superintendent', 'We got the orders and the opportunity to make April even a better month. '
            '*Keep* *up* *the* *momentum—our* *future* *is* *what* *we* *make* *it.*', head2='COMPLAINT ¶10h · ' + SIXTH, items=[EX('C-2', x=1600, y=850, at=-.3)]),
 'e09': hot('21 DEC 1978', 'Bill Kirwan, superintendent', 'You will recall that early in 1978 we initiated significant changes in our operations in order to make Youngstown Works '
            'profitable … we have attained our 1978 goal which was *‘survival’* and now we embark on the 1979 goal which is *‘revival.’*', head2='COMPLAINT ¶10l · ' + SIXTH),
 'e10': doc('STATEMENT TO THE PRESS AND ON ABC TELEVISION', '*Simply* *stated,* *we* *have* *no* *plans* *for* *shutting* *down* *our* *Youngstown* *operation.* '
            'Only two things would result in a Youngstown shutdown: [massive expenditures to meet environmental requirements or an unproductive plant operation.]',
            head2='DAVID RODERICK, CHAIRMAN OF THE BOARD, U.S. STEEL · ON OR ABOUT 18 JUNE 1979', cite='COMPLAINT ¶10p · ' + SIXTH, items=[EX('C-3', x=1560, y=860, at=-.3)]),
 'e11': doc('COMPLAINT · THE INDIVIDUAL PLAINTIFFS', 'Frank Georges, R.D. 2, Hillsville Road, Lowellville, Ohio, another individual Plaintiff, bought a new home on '
            '*November* *27,* *1979,* and heard the news of Defendant’s shutdown announcement *on* *the* *car* *radio* as he drove home from the bank.', cite=SIXTH),
 'e12': dict(type='river', riverDur=.01, cam=[[0, 910, 590, 1.7, 0], [3, 960, 540, 1.0, 0]], towns=TOWNS_ALL, mills=[['ohio', 0, -.25], ['mcd', 0, -.3], ['brier', 0, 'off'], ['camp', 0, 'off']],
             closed={'camp': 'CLOSED · 1977', 'brier': 'CLOSED · 1979', 'ohio': 'CLOSING · 1980', 'mcd': 'CLOSING · 1980'}, items=[I('stamp', text='3,500', x=1560, y=880, s=70, at=-.6)]),
 'e13': typ(['Monday, 28 January 1980.'], s=96, redLine=0, sub='the Local 1330 union hall', clip='c_houses', dim=.82),
 'e14': cont(),
 'w05': dict(type='witness', clip='c_gate', imgTag='STEELWORKERS AT A YOUNGSTOWN MILL GATE · 1944 (STEEL TOWN) · NOT 1980'),
 'e15': typ(['KEEP OUR MILLS OPEN'], s=120, clip='c_gate', dim=.84, items=[I('stamp', text='28 JAN 1980', x=1560, y=200, s=60, at=.2)], tag='THE BANNER’S WORDS, AS RECORDED BY LYND (1982)'),
 'e16': typ(['Can a promise like that', 'hold up in court?'], s=96, step=.8, img='n_pour', era='b', dim=.82),
 # ── part 6 · the trial ──
 'f02': doc('UNITED STATES DISTRICT COURT · NORTHERN DISTRICT OF OHIO', 'LOCAL 1330, UNITED STEEL WORKERS OF AMERICA, et al., Plaintiffs, v. UNITED STATES STEEL CORPORATION, '
            'Defendant. Case No. C 79-2337 Y. *Filed* *December* *21,* *1979.*', head2='COMPLAINT', cite=NDO, stamp='21 DEC 1979', stampAt=-.5),
 'f03': typ(['Staughton Lynd', 'Judge Thomas D. Lambros'], s=90, step=1.3, sub='for the steelworkers  ·  for the court', img='centralsq_pc', era='c', dim=.86),
 'f04': dict(type='scale', title='THE PLAINTIFFS’ CASE', pans=[dict(side=-1, big='A PROMISE', small='CONTRACT · RELIANCE', w=1, at=-.45)]),
 'f05': cont(pans=[dict(side=-1, big='A TOWN’S RIGHT', small='COMMUNITY PROPERTY RIGHT', w=1, at=-.6)]),
 'f06': typ(['4 February 1980'], s=110, redLine=0, sub='U.S. Steel: the shutdown will come sooner'),
 'f07': hero('fed_bldg', FED, items=[I('stamp', text='28 FEB 1980', x=1560, y=200, s=60, at=.3)]),
 'f08': doc('PRETRIAL CONFERENCE · 28 FEBRUARY 1980', 'Everything that has happened in the Mahoning Valley has been happening for many years *because* *of* *steel.* '
            'Schools have been built, roads have been built. Expansion that has taken place is because of steel.', head2='JUDGE THOMAS D. LAMBROS, FROM THE BENCH',
            cite='TRANSCRIPT, ' + SIXTH, img='panorama1910', grade='b'),
 'f09': doc('PRETRIAL CONFERENCE · 28 FEBRUARY 1980', '… it seems to me that a *property* *right* *has* *arisen* *from* *this* *lengthy,* *long-established* *relationship* '
            'between United States Steel, the steel industry as an institution, the community in Youngstown, the people in Mahoning County and the Mahoning Valley …',
            head2='JUDGE THOMAS D. LAMBROS, FROM THE BENCH', cite='TRANSCRIPT, ' + SIXTH, until=-.85, img='panorama1910', grade='b'),
 'f10': hclip('c_furnace', ST44, items=[I('txt', text='INJUNCTION · THE MILLS STAY OPEN', x=240, y=860, s=40, f='Mono', w=600, at=.3),
             I('txt', text='THE TRIAL MOVES TO YOUNGSTOWN', x=240, y=910, s=40, f='Mono', w=600, at=-.45)]),
 'f11': typ(['17 March 1980'], s=120, redLine=0, sub='the trial opens · five days', clip='c_ohfloor', dim=.85),
 'f12': dict(type='scale', title='THE PLAINTIFFS REST', pans=[dict(side=-1, big='A PROMISE', small='CONTRACT · RELIANCE', w=1, at=0), dict(side=-1, big='A TOWN’S RIGHT', small='COMMUNITY PROPERTY RIGHT', w=1, at=0)]),
 # ── part 7 · the defence ──
 'g02': hero('palmer_slag1', PALMER, era='s', box=[460, 50, 1000, 870], cap='AN OPEN HEARTH IN YOUNGSTOWN · 1941', items=[EX('D-1', side='d', x=1420, y=820, at=-.5)]),
 'g03': hclip('c_tap', ST44, cap='OPEN-HEARTH FURNACE · YOUNGSTOWN, 1944', items=[EX('D-2', side='d', at=-.4)]),
 'g04': hero('palmer_scene', PALMER, era='s', box=[460, 50, 1000, 870], items=[I('stamp', text='$250 MILLION', x=1560, y=300, s=56, at=-.45),
             I('txt', text='KIRWAN’S OWN ESTIMATE, MAY 1979:', x=1150 + 310, y=420, s=22, f='Mono', w=600, al='center', at=-.4),
             I('txt', text='ELECTRIC FURNACES + CASTER AT McDONALD', x=1460, y=452, s=22, f='Mono', w=600, al='center', at=-.4)]),
 'g05': doc('TRIAL TESTIMONY · MARCH 1980', 'Q. And through the end of October, 1979, Youngstown the performance of that year was in the area of about the break even, was it not? '
            'A. … the actual number was about a *$300* *thousand* *loss,* as of the end of October, cumulative for the year.', head2='DAVID RODERICK, CHAIRMAN AND CEO, U.S. STEEL',
            cite=NDO, items=[EX('D-3', side='d', x=1640, y=880, at=-.3)]),
 'g06': dict(type='scale', title='YOUNGSTOWN WORKS · 1980 · THE COMPANY’S OWN PROJECTIONS', note='SOURCE · ' + NDO,
             pans=[dict(side=-1, big='+$32.4M', small='GROSS MARGIN · VARIABLE COSTS ONLY', w=1, at=-.55)]),
 'g07': cont(pans=[dict(side=1, big='−$9.4M', small='OVERALL · ALL COSTS COUNTED', w=1, at=-.7)]),
 'g08': cont(set={'level': .1}),
 'g09': hot('4 JAN 1978', 'Bill Kirwan, superintendent', 'With your help, this effort will continue and *if* *and* *when* *there* *will* *be* *a* *phase-out* *depends* *on* *the* *plant’s* '
            '*profitability,* but no time table has been set.', head2='COMPLAINT ¶10e · ' + SIXTH, items=[EX('D-4', side='d', x=1600, y=850, at=-.3)]),
 'g10': doc('THE COURT OF APPEALS, SUMMARISING U.S. STEEL’S ANSWER', '… claiming that the plants were unprofitable and could not be made otherwise due to obsolescence and change in '
            'technology, markets, and transportation. The company also asserts an *absolute* *right* *to* *make* *a* *business* *decision* to discharge its former employees and abandon Youngstown.',
            cite=SIXTH),
 'g11': doc('FINDINGS · 492 F. Supp. 1', 'David Roderick, United States Steel Board Chairman, has made it plain in testimony that he *will* *not* *sell* *the* *plants* *to* *any* *federally* '
            '*subsidized* *competitor.*', cite=NDO),
 'g12': dict(type='scale', title='WHO’S RIGHT?', level=.2, pans=[dict(side=-1, big='A PROMISE', small='CONTRACT · RELIANCE', w=1, at=0), dict(side=-1, big='A TOWN’S RIGHT', small='COMMUNITY PROPERTY RIGHT', w=1, at=0),
             dict(side=1, big='LOSSES', small='−$9.4M PROJECTED, 1980', w=.7, at=0), dict(side=1, big='OBSOLESCENCE', small='OPEN HEARTHS', w=.7, at=.15), dict(side=1, big='NO SUCH LAW', small='A RIGHT TO CLOSE', w=.6, at=.3)]),
 # ── part 8 · the verdict ──
 'h12': hero('fed_bldg', FED, items=[I('stamp', text='21 MAR 1980', x=1560, y=200, s=60, at=.3)]),
 'h13': doc('FINDINGS OF FACT · 492 F. Supp. 1', 'Although managerial employees of defendant on occasion throughout 1977, 1978, 1979 and 1980 urged plaintiff workers to increase their '
            'productivity …, the corporation *never* *promised* *to* *keep* *the* *mills* *operating* *so* *long* *as* *the* *workers* *made* *the* *mills* *profitable.*',
            head2='JUDGE THOMAS D. LAMBROS · MARCH 1980', cite=NDO),
 'h14': doc('OPINION · 492 F. Supp. 1', 'Unfortunately, the mechanism to reach this ideal settlement, to recognize this new property right, *is* *not* *now* *in* *existence* '
            '*in* *the* *code* *of* *laws* *of* *our* *nation.*', head2='JUDGE THOMAS D. LAMBROS · MARCH 1980', cite=NDO),
 'h15': doc('OPINION · 492 F. Supp. 1', 'However, this Court is *not* *a* *legislative* *body* and can not make laws where none exist … In these terms this Court can determine '
            '*no* *legal* *basis* *for* *the* *finding* *of* *a* *property* *right.*', head2='JUDGE THOMAS D. LAMBROS · MARCH 1980', cite=NDO),
 'h16': typ(['25 July 1980'], s=120, redLine=0, sub='U.S. Court of Appeals for the Sixth Circuit · Cincinnati'),
 'h17': doc('OPINION · 631 F.2d 1264 · SIXTH CIRCUIT · 25 JULY 1980', 'The former mill towns of New England, with their empty textile factory buildings, are *monuments* *to* *the* '
            '*migration* of textile manufacturers to the South, without hindrance from the Congress of the United States, from the legislatures of the states concerned, or, for that matter, from the courts of the land.',
            cite=SIXTH, until=-.97, img='n_bf2', grade='b'),
 'h18': doc('OPINION · 631 F.2d 1264 · SIXTH CIRCUIT · 25 JULY 1980', 'In the view of this court, formulation of public policy on the great issues involved in plant closings and removals is clearly the '
            '*responsibility* *of* *the* *legislatures* *of* *the* *states* *or* *of* *the* *Congress* *of* *the* *United* *States.*', cite=SIXTH, img='n_bf2', grade='b'),
 'h19': dict(type='dots', at=.0, falls=[-.12, -.3, -.45], total=-.62),
 'h20': hero('n_bf3', 'BLAST FURNACES, YOUNGSTOWN SHEET AND TUBE' + NARA, era='b', cap='SHEET & TUBE FURNACES IN 1918 · NOT JENNY', z=[1.2, 1.05],
             items=[I('stamp', text='29 JAN 1997', x=1560, y=200, s=60, at=-.5)]),
 'h21': typ(['Did it change anything?'], s=100, img='aerial2025b', dim=.8),
 # ── part 9 · the jury ──
 'j02': doc('OPINION · 492 F. Supp. 1', 'At this moment, *proposals* *for* *legislative* *redress* of economic relocation like the situation before us *are* *pending* *on* *Capitol* *Hill.*',
            head2='JUDGE THOMAS D. LAMBROS · MARCH 1980', cite=NDO),
 'j03': typ(['The WARN Act · 1988'], s=110, sub='60 days’ notice of most plant closings and mass layoffs', tag='WORKER ADJUSTMENT AND RETRAINING NOTIFICATION ACT · PUBLIC LAW 100-379'),
 'j04': typ(['60 days.', 'On Black Monday: none.'], s=110, step=1.0, redLine=0),
 'j05': hero('downtown_fed', 'DOWNTOWN YOUNGSTOWN · 2019 · PHOTO: DBLCUT3 (CC BY-SA 4.0)', items=[I('stamp', text='1992', x=1560, y=200, s=70, at=.2),
             I('txt', text='YOUNGSTOWN HISTORICAL CENTER OF INDUSTRY AND LABOR', x=240, y=880, s=30, f='Mono', w=600, at=.5)]),
 'j06': hero('downtown_north', 'DOWNTOWN YOUNGSTOWN · 2006 · PHOTO: DAYSLEEPER47 (CC BY 2.5)', items=[I('stamp', text='1995', x=1560, y=200, s=70, at=.2)]),
 'j07': hero('aerial2025', 'THE YOUNGSTOWN–WARREN AREA FROM THE AIR · 2025 · PHOTO: DESIGNISM (CC0)', items=[I('stamp', text='$650 MILLION', x=1500, y=220, s=60, at=.6),
             I('count', to=350, pre='≈ ', x=1500, y=880, s=90, at=-.75, dur=1.0, label='JOBS · 2012')]),
 'j08': dict(type='line', at=.1, draw=1.8, marks=[[1930, '1930'], [2020, '2020']], band=-.4),
 'j09': dict(type='scale', title='THE CASE', pans=[dict(side=1, big='LOSING MONEY', small='THE COMPANY SAID', w=1, at=-.3), dict(side=1, big='EVERY LEGAL RIGHT', small='TO CLOSE', w=1, at=-.65)]),
 'j10': cont(pans=[dict(side=-1, big='EIGHTY YEARS', small='OF A TOWN’S WORK', w=1, at=-.35), dict(side=-1, big='A BELIEF', small='THAT IT SHOULD COUNT', w=1, at=-.7)], set={'level': -.5}),
 'j11': cont(),
 'j12': typ(['Does a town have any right', 'to the mill it built its life around?'], s=74, step=1.2, clip='c_skyline', dim=.8),
 'j13': dict(type='jury', lines=['You’ve heard the case.', 'What’s your verdict?'], at=[.1, -.5], redLast=1),
 'j14': hero('skyline', 'YOUNGSTOWN FROM WEAN PARK · 2020 · PHOTO: DBLCUT3 (CC BY-SA 4.0)', box=[0, 140, 1920, 727], noflash=1),
}
WIT = {l['id']: l.get('witness') for l in L}

# ── timeline ──
scenes, subs, voice, t = [], [], [], 0.0
def add(sc, t0): sc = dict(sc); sc['t0'] = round(t0, 3); scenes.append(sc); return sc
def rel(v, vt, t0, d): return round(vt - t0 + (v if v >= 0 else -v * d), 3)
t = OPEN; after_card = False
prev_ch = None
for l in L:
    lid, ch = l['id'], l['chapter']; part = PART[ch]
    if lid in WIT and WIT[lid]:   # a witness card, held in silence
        w = WIT[lid]; sc = dict(type='witness', part=part, **{k: v for k, v in w.items() if k != 'hold'}); sc.update(S.get(lid, {}))
        add(sc, t); t += w['hold'] + .9; prev_ch = ch; continue
    d = DUR[lid]
    if ch != prev_ch and ch in CARD:   # the case caption card carries this part's first line
        ti, sub = CARD[ch]; t += PRECARD; add(dict(type='case', n=part, title=ti, sub=sub, part=part, line=lid), t)
        vt = t + 2.3; voice.append(dict(id=lid, t=round(vt, 3), d=d)); subs.append(dict(t0=round(vt, 3), t1=round(vt + d, 3), text=l['subs'][0]))
        t = vt + d + 1.2; prev_ch = ch; after_card = True; continue
    prev_ch = ch; vt = t
    sh = S.get(lid)
    if sh is None: raise SystemExit(f'no shot for {lid}')
    if sh.get('cont'):
        last = scenes[-1]
        for key in ('items', 'pans', 'mills', 'towns'):
            for it in sh.get(key, []):
                if isinstance(it, dict): it = dict(it); it['at'] = rel(it.get('at', .4), vt, last['t0'], d)
                else: it = list(it); it[1] = rel(it[1], vt, last['t0'], d)
                last.setdefault(key, []).append(it)
        for k, v in sh.get('set', {}).items(): last[k] = rel(v, vt, last['t0'], d)
    else:
        sc = copy.deepcopy(sh); sc['line'] = lid; sc['vd'] = d; sc['part'] = part
        if 'from_' in sc: sc['from'] = sc.pop('from_')
        if after_card: sc['xf'] = XF; after_card = False
        add(sc, max(0.0, vt - .25))
    voice.append(dict(id=lid, t=round(vt, 3), d=d))
    if any(l['subs']):
        tot = sum(len(s) for s in l['subs']); a = vt
        for s in l['subs']:
            b = a + d * len(s) / tot; subs.append(dict(t0=round(a, 3), t1=round(b, 3), text=s)); a = b
    t = vt + d + (QGAP if lid in QUIET else GAP)
    if lid == 'h08':   # the Mill Town title sequence after the cold open
        t = round(t * 30) / 30; add(dict(type='title', part=0), t); t += TITLE
scenes[0]['t0'] = 0.0   # the film opens on the first picture (fading up from black), no black lead-in
end = add(dict(type='end', part=9), t + .2); DURT = round(t + .2 + END, 3)
for a, b in zip(scenes, scenes[1:] + [None]): a['t1'] = b['t0'] if b else DURT
CREDITS = ['What Happened to Youngstown? The Day the Steel Mills Closed',
           'COURT RECORD · LOCAL 1330 v. U.S. STEEL · 492 F. SUPP. 1 (N.D. OHIO 1980) · 631 F.2d 1264 (6th CIR. 1980)',
           'SOURCE · STAUGHTON LYND, THE FIGHT AGAINST SHUTDOWNS: YOUNGSTOWN’S STEEL MILL CLOSINGS (1982)',
           'FILM · STEEL TOWN (1944), OFFICE OF WAR INFORMATION · NATIONAL ARCHIVES',
           'PICTURES · NATIONAL ARCHIVES · LIBRARY OF CONGRESS · USGS · DPLA POSTCARDS',
           'PHOTOGRAPHS · STU_SPIVACK · BFDHD · DBLCUT3 · DAYSLEEPER47 · DESIGNISM (CC BY / CC BY-SA / CC0)',
           'CENSUS FIGURES · U.S. CENSUS BUREAU · MAP · SCHEMATIC, MADE FOR THIS FILM',
           'MUSIC · ORIGINAL SCORE']
film = dict(dur=DURT, scenes=scenes, subs=subs, voice=voice, credits=CREDITS)
json.dump(film, open(os.path.join(D, 'film.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
cues = []
for s in scenes:
    for it in s.get('items', []):
        if it.get('k') in ('ex', 'stamp'):
            a = it.get('at', .4); cues.append(dict(k=it['k'], t=round(s['t0'] + (a if a >= 0 else -a * s.get('vd', s['t1'] - s['t0'])), 3)))
json.dump(dict(dur=DURT, voice=voice, cues=cues, scenes=[dict(type=s['type'], t0=s['t0'], t1=s['t1'], part=s.get('part'), line=s.get('line'), clip=s.get('clip') or s.get('clips')) for s in scenes]),
          open(os.path.join(D, 'audio/cues.json'), 'w'), indent=0)
print(f'{len(scenes)} scenes, {DURT:.1f} s = {DURT / 60:.2f} min')
print('0:00 The Charge'); [print(f"{int(s['t0'] // 60)}:{int(s['t0'] % 60):02d} " + (f"Part {s['n']}: {s['title']}" if s['type'] == 'case' else 'Mill Town title')) for s in scenes if s['type'] in ('case', 'title')]
