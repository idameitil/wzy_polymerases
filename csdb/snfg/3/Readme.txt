Low-resolution SFNG image files <CSDB_record_ID>.gif for selected CSDB records.

Values for CSDB_record_ID and CSDB_linear are found in the TSV 'CSDB_slice_for_Ida.txt'.

A subset of CSDB_record_IDs provided manually by Ida M were used, as well as records selected by
matching Taxonomy.

In most cases, an image was successfully generated using the CSDB_linear string provided, using
a 'wget' call to csdb.glycoscience.ru server. However, manual inspection of the gif files revealed
some failed, with the commonality that all contained text in square brackets describing subpopulations
of sugars. In these cases a sugar structure image could be obtained by removing the comment.
Therefore some of the images do not contain these elements.

For an additional subset of failed cases, an image could not be retrieved. These are 'registered'
in this directory as a zero-length file.

# Example where removing the 'subpopulations comment' enabled rendering.

For CSDB record_id 11556, compare the following:

(1) This link directly produced within CSDB, in this case failing to parse the sugar structure,
thus failing to provide an image.

http://csdb.glycoscience.ru/database/core/show_snfg.php?to_draw=-6%29aDGalp%281-4%29bDGlcpA%281-6%29bDGalp%281-4%29%5B%3C%3C30%25Ac%281-3%29%7C20%25Ac%281-2%29%3E%3E%5DbDGalp%281-4%29%5BAc%281-2%29%5DbDGlcpN%281-&scale=3

(2) Modified link with 'percentage of each subpopulation' element removed:

http://csdb.glycoscience.ru/database/core/show_snfg.php?to_draw=-6%29aDGalp%281-4%29bDGlcpA%281-6%29bDGalp%281-4%29bDGalp%281-4%29%5BAc%281-2%29%5DbDGlcpN%281-&scale=3


Jan 6, 2022, G.P.Gippert
