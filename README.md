# normb
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

Package that runs a battery of univariate and mutivariate normality tests on a numeric pandas.DataFrame (df). The packages comes with a `DataFrameGenerator` that can produce dfs following a `uniform`, `normal` or `mixed` distribution. These dataframes or any other dfs can be run through the `NormalityBattery` class which runs the conventional univariate normality tests by [Kolmogorov A (1933)](https://ci.nii.ac.jp/naid/10010480527/), [Smirnov N (1948)](https://www.jstor.org/stable/2236278?seq=1#page_scan_tab_contents), [Shapiro and Wilk (1965)](https://www.jstor.org/stable/2333709?seq=1#page_scan_tab_contents), [Jarque and Bera (1980)](https://www.sciencedirect.com/science/article/pii/0165176580900245), [D’Agostino (1971)](https://www.jstor.org/stable/2334522) and [Pearson’s (1973)](https://www.jstor.org/stable/2335012?seq=1#page_scan_tab_contents). In addition, the `NormalityBattery` produces results of the multivariate normality tests by [Mardia, K.V. (1970)](https://www.jstor.org/stable/2334770?seq=1#page_scan_tab_contents), [Roystone (1983)](https://www.jstor.org/stable/2347291?seq=1#page_scan_tab_contents), [Henze and Zirkler (1990)](https://www.tandfonline.com/doi/abs/10.1080/03610929008830400) and [Doornik and Hansen (2008)](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0084.2008.00537.x). The results of all the tests are summarised in a report which can be accessed via the `normality_report` method in the `NormalityBattery` class. 
