dataset	CSBrain	CBraMod	REVE	Ours (WM)	最好
PhysioNet-MI	.5990 / .5957	.6199 / .6244	.6573 / .6560	.6330 / .6321	REVE
FineMI	.1858 / .1962	.1972 / .1955	.2347 / .2146	.2000 / .1955	REVE
Kaya5F	.3803 / .3844	.3904 / .3903	.4174 / .3920	.3889 / .3777	REVE
Weibo2014 *	.1676 / .1704	.1845 / .1794	.2038 / .2188	.1861 / .1852	REVE*
Forenzo2024	.3074 / .2938	.3064 / .2948	.3171 / .2926	.3191 / .3137	ours
Jeong2020	.1601 / .1506	.1532 / .1516	.1522 / .1526	.1544 / .1564	平手
Forenzo2024Reg	.2133	.1977	.1422	.2207	ours




split / arm	l1 ↓	cos ↑	act_gap ↑
within / ours	0.5009	0.8773	+0.0079
within / lawm	0.6519	0.8463	+0.0021
within / random-init	0.7334	0.8334	+0.0000
subject / ours	0.4933	0.8850	+0.0057
subject / lawm	0.5543	0.8737	+0.0029
subject / random-init	0.7224	0.8407	+0.0000
