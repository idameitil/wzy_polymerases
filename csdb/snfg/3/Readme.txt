Low-resolution SFNG images for selected CSDB entrys by record_id.gif.

For some record_ids, the visualization failed, apparently due to the presence of
percentage values (for subpopulations) within the encoded csdb_linear sugar string.
These were identified manually and removed from the sugar string before retrieving
the images.

For example, for CSDB record_id 11556, compare the following:

(1) This link directly produced within CSDB, in this case failing to parse the sugar structure,
thus failing to provide an image.

http://csdb.glycoscience.ru/database/core/show_snfg.php?to_draw=-6%29aDGalp%281-4%29bDGlcpA%281-6%29bDGalp%281-4%29%5B%3C%3C30%25Ac%281-3%29%7C20%25Ac%281-2%29%3E%3E%5DbDGalp%281-4%29%5BAc%281-2%29%5DbDGlcpN%281-&scale=3

(2) Modified link with 'percentage of each subpopulation' element removed:

http://csdb.glycoscience.ru/database/core/show_snfg.php?to_draw=-6%29aDGalp%281-4%29bDGlcpA%281-6%29bDGalp%281-4%29bDGalp%281-4%29%5BAc%281-2%29%5DbDGlcpN%281-&scale=3


Jan 6, 2022, G.P.Gippert
