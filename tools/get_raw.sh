#!/bin/sh
# Archive material for "What Happened to Youngstown?" — public domain, CC0, CC BY and CC BY-SA (licences logged in SOURCES.jsonl).
cd "$(dirname "$0")/.." || exit 1
PY=${PY:-python -I}
F="$PY tools/footage.py fetch"
big() {   # name, commons file title, credit, licence, width
  ls raw/$1.* >/dev/null 2>&1 && return 0
  enc=$($PY -c "import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1].replace(' ','_')))" "$2")
  $F "https://commons.wikimedia.org/wiki/Special:FilePath/$enc?width=${5:-2600}" --name "$1" \
    --page "https://commons.wikimedia.org/wiki/File:$enc" --license "$4" --credit "$3"; sleep 2
}
url() {   # name, url, page, credit, licence
  ls raw/$1.* >/dev/null 2>&1 && return 0
  $F "$2" --name "$1" --page "$3" --license "$5" --credit "$4"; sleep 1
}
PD="Public domain"
big campbell_night "Y-68 - General View of Youngstown Sheet and Tube Company, Night View, Campbell Works.jpg" "Postcard Y-68: Campbell Works at night" "$PD" 2600
big bf1918 "Blast Furnace and Power Plant, 1918 National Archives (40089361451).jpg" "Sheet & Tube blast furnace and power plant, 1918 (National Archives)" "$PD" 2600
big larry1918 "Larry Car Used in Transferring Ore, Coke and Limestone from Bins to Skip Hoists at Blast Furnace, 1918 National Archives (25217070357).jpg" "Larry car at a Sheet & Tube blast furnace, 1918 (National Archives)" "$PD" 2600
big molds1918 "Stripping Molds from Steel Ingots 1918 National Archives (25217069197).jpg" "Stripping molds from steel ingots, Sheet & Tube, 1918 (National Archives)" "$PD" 2600
big oreyard1930 "Ore yard - Youngstown Sheet and Tube 1930.jpg" "Ore yard, Youngstown Sheet and Tube, c. 1930" "$PD" 1455
big viaduct_pc "Sheet&tube.jpg" "Postcard: viaduct at Youngstown Sheet and Tube Co." "$PD" 700
big ohioworks1905 "Ohio Steel Works and furnaces, view of west side, 1905 LCCN2007662629.tif" "Ohio Steel Works and furnaces, west side, 1905 (Library of Congress)" "$PD" 3996
big ohioworks_pc "Carnegie Steel Works (Ohio Works), Youngstown, Ohio - DPLA - c73c879cb821eb87e0e40c01867b035f (page 1).jpg" "Postcard: Carnegie Steel Works (Ohio Works), Youngstown (DPLA)" "$PD" 2600
big carnegie_pc "Carnegie Steel Co., Youngstown, Ohio - DPLA - 5a21756f1859e6e759114cea69d1335d (page 1).jpg" "Postcard: Carnegie Steel Co., Youngstown (DPLA)" "$PD" 2600
big panorama1910 "Panoramic view of Youngstown, O LCCN2007662628.tif" "Panoramic view of Youngstown, c. 1910 (Library of Congress)" "$PD" 5034
big birdseye1882 "Panoramic view of the city of Youngstown, county seat of Mahoning Co., Ohio 1882. LOC 73694520.jpg" "Panoramic view of Youngstown, 1882 (Library of Congress)" "$PD" 4000
big usgs1970 "Youngstown, Ohio USGS 1970-03-31 1-49.jpg" "Youngstown from the air, 31 March 1970 (USGS)" "$PD" 4000
big flag1918 "Flags - Flag Raisings - Flag raising at Central Square, Youngstown, Ohio showing crowd of 30,000 - NARA - 31480488.jpg" "Flag raising at Central Square, crowd of 30,000, 1918 (National Archives)" "$PD" 2600
big centralsq_pc "Central Square, Youngstown, Ohio - DPLA - ff2703712732acc15fa58d5adbdda577 (page 1).jpg" "Postcard: Central Square, Youngstown (DPLA)" "$PD" 2600
big palmer_slag1 "Slag run-off from open hearth furnace, Republic Steel Corp.1a35053v.jpg" "Alfred T. Palmer, open hearth, Republic Steel, Youngstown, 1941 (Library of Congress)" "$PD" 2600
big palmer_slag2 "Slag run-off from one of the open hearth furnaces of a steel mills, Republic Steel Corp1a35054v.jpg" "Alfred T. Palmer, open hearth, Republic Steel, Youngstown, 1941 (Library of Congress)" "$PD" 2600
big palmer_scene "A scene in a steel mill, Republic Steel, Youngstown, Ohio.jpg" "Alfred T. Palmer, Republic Steel mill, Youngstown, 1941 (Library of Congress)" "$PD" 2600
big n_pour "Industries of War - Machinery - Miscellaneous - Manufacturing Steel Products at the Youngtown Sheet and Tube Co., Youngtown, Ohio. Pouring molten iron from blast furnaces into mixer - NARA - 45486065.jpg" "Pouring molten iron into the mixer, Sheet & Tube, 1918 (National Archives)" "$PD" 4000
big n_ladle "Industries of War - Machinery - Miscellaneous - Manufacturing steel products at the Youngtown Sheet and Tube Co., Youngtown, Ohio. Pouring molten iron from the mixer into ladle - NARA - 45486083.jpg" "Pouring molten iron into a ladle, Sheet & Tube, 1918 (National Archives)" "$PD" 4000
big n_charge "Industries of War - Metals - Steel - Youngstown Sheet and Tube Company - Manufacture of steel products at the Youngstown Sheet and Tube Company, Youngstown, Ohio. Charging molten Iron into open-hearth furnace - NARA - 45487946.jpg" "Charging molten iron into an open-hearth furnace, Sheet & Tube, 1918 (National Archives)" "$PD" 4000
big n_crowd "Industries of War - Metals - Steel - Youngstown Sheet and Tube Company - Steel Manufacture at Youngstown Sheet and Tube Company, Youngstown, Ohio - NARA - 45487874.jpg" "Steelworkers at Youngstown Sheet and Tube, 1918 (National Archives)" "$PD" 4000
big n_bf1 "Industries of War - Metals - Steel - Youngstown Sheet and Tube Company - Steel Manufacture at Youngstown Sheet and Tube Company, Youngstown, Ohio - NARA - 45487918.jpg" "Steel manufacture at Youngstown Sheet and Tube, 1918 (National Archives)" "$PD" 4000
big n_bf2 "Industries of War - Metals - Steel - Youngstown Sheet and Tube Company - Steel Manufacture at Youngstown Sheet and Tube Company, Youngstown, Ohio - NARA - 45487960.jpg" "Steel manufacture at Youngstown Sheet and Tube, 1918 (National Archives)" "$PD" 4000
big n_bf3 "Industries of War - Metals - Steel - Youngstown Sheet and Tube Company - Steel Manufacture at Youngstown Sheet and Tube Company, Youngstown, Ohio - NARA - 45487972.jpg" "Blast furnaces, Youngstown Sheet and Tube, 1918 (National Archives)" "$PD" 4000
big n_bf4 "Industries of War - Metals - Steel - Youngstown Sheet and Tube Company - Steel Manufacture at Youngstown Sheet and Tube Company, Youngstown, Ohio - NARA - 45487974.jpg" "Steel manufacture at Youngstown Sheet and Tube, 1918 (National Archives)" "$PD" 4000
big n_pipe "Industries of War - Piping - Manufacturing steel pipe for the government at the Youngstown Sheet and Tube Company plant, Youngstown, Ohio. Method of welding steel pipe - butt-weld process - NARA - 45488931.jpg" "Butt-welding steel pipe, Sheet & Tube, 1918 (National Archives)" "$PD" 4000
big yst_sign "Youngstown Sheet&Tube Abandoned.jpg" "Photo: stu_spivack, 2006 (CC BY-SA 2.0)" "CC BY-SA 2.0" 2560
big aerial2025 "Youngstown-Warren aerial 20250323 (1).jpg" "Photo: Designism, 2025 (CC0)" "CC0" 3600
big aerial2025b "Youngstown-Warren aerial 20250323 (3).jpg" "Photo: Designism, 2025 (CC0)" "CC0" 3600
big downtown_aerial "Downtown Youngstown, Ohio aerial 20250323 (1).jpg" "Photo: Designism, 2025 (CC0)" "CC0" 3600
big struthers "Struthers aerial.jpg" "Photo: Ohio Development Services Agency, 2014 (CC BY 2.0)" "CC BY 2.0" 3600
big fed_bldg "Federal Bldg.JPG" "Photo: BFDhD, 2009 (CC BY-SA 3.0)" "CC BY-SA 3.0" 3600
big downtown_fed "Downtown Youngstown W. Federal.jpg" "Photo: Dblcut3, 2019 (CC BY-SA 4.0)" "CC BY-SA 4.0" 3600
big skyline "Youngstown skyline Wean Park.jpg" "Photo: Dblcut3, 2020 (CC BY-SA 4.0)" "CC BY-SA 4.0" 1936
big downtown_north "DowntownYoungstownLookingNorth.jpg" "Photo: Daysleeper47, 2006 (CC BY 2.5)" "CC BY 2.5" 2576
url film_steeltown "https://archive.org/download/306-163/306-163.mp4" "https://archive.org/details/306-163" "Steel Town, Office of War Information, 1944 (National Archives)" "Public domain (U.S. National Archives, 306-163)"
