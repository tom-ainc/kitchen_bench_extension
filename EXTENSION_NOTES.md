# Kitchen bench extension: design notes

## Current design (model v107). Read this first; the history below is superseded wherever it disagrees.

**Unit:** semi-freestanding three-drawer base unit under the benchtop extension, 15 mm plywood throughout, hand routing only, drawers on Hafele Alto runner drawbars (steel sides not used).
- Overall floor to benchtop underside 874 (top surface 900: 26 mm timber top, with a 12 mm hem under the front edge only); plinth frame 125 (kickboard cover Kb 115, as the existing kickboard); carcass 805 wide x 522 deep x 749 high (775 clear between the sides, inside depth 507). The front of the unit is set 15 mm further back from the benchtop edge (front overhang 38) so the hem clears the fronts; the rear did not move. The carcass and plinth stop 40 mm short of the wall (skirting board); the benchtop keeps its 600 depth.
- Parts (sheet 1): C1, C2 sides 749 x 522; C3 bottom 775 x 507; C4 back 775 x 749 (full height, on the ends of the plinth side rails); C9 front top rail 775 x 60; plinth P1 front rail and P2 rear rail 767 x 125, P3 (free end) and P4 (joint end) side rails 461 x 125, Kb kickboard cover 852 x 115; drawer fronts 802 x 215 (D1, D2) and 802 x 313 (D3); sides 495 x 164 (x4) and 495 x 245 (x2); backs 713 x 159 (x2) and 713 x 240; bases 728.5 x 487.5 (x3).
- Drawers: box sides 16 from the walls, drawbar plate tops 534 / 331 / 50 above the top of C3, fronts 212.7 / 212.7 / 326.3 overlapping 10 mm (nose 2 mm clear of the front above), D1 mitre plane 15 mm (vertical) below a parallel 45 degree plane through the hem's back-bottom edge, bottom front level with the existing doors (120 above the floor) and hanging 5 below C3. Base slot (15.5 x 8) in the sides and the back; front plain; box built front-last.
- Fixing of the box to the drawbars: option 1 snap clip (main), option 2 screws from below (alternative); `DB_FIX` in the script.
- Pull: 45 degree mitre on the top edge of all three fronts (R3 nose), full-thickness 45 degree mitre (15 mm high on the face, back edge rounded R2 and face arris R3, `MIT_BOT_R_TIP` / `MIT_BOT_R_FACE`; about 15 mm vertical gap to the mitre of the front below, a fingertip tested with calipers) on the bottom edge of D1 and D2 (primary; `MIT_BOTTOM` = "mitre" | "cove"); other styles remain selectable in the script only, not documented in the drawings; `PULL` = "mitre" | "front_cove" | "groove" | "rebate".
- Joints modelled: 42 pocket joints (25 mm, 15 degrees) in the carcass and plinth (30 carcass and plinth-rail joints plus 12 plinth-to-carcass), 28 in the drawer boxes, 36 bracket screws, link-bolt slots in C2, kickboard screws, clip screws. Not modelled: Hafele runner fixing screws and front-bracket fixings (hole patterns not supplied).

**Files** (project folder):
- `extension_unit.py`: the model script (copy of the golf project's `ext.py`). Parameters at the top: `PULL`, `DB_FIX`, `BASE_SLOT`, `REAR_SETBACK`, `AV_STEP` (picture view mode, 0 = normal).
- `bench_with_extension_pull_mitre.step` (primary), `_pull_front_cove.step`, `_pull_groove.step`, `_pull_rebate.step`: whole bench plus the new unit. Older exports are in `archive/`.
- `shop_drawings/extension_unit_shop_drawings.pdf`: 11 sheets, built by `shop_drawings/build_all.py`. Sheet 10 cutting diagrams (exact, 2 sheets); sheet 11 store cuts on 100 mm multiples (3 sheets, from `nest_round.py`).
- `assembly/extension_unit_assembly_guide.pdf` and `assembly/ASSEMBLY_GUIDE.md`: nine picture steps plus the written guide; built from `assembly/content.py`, `assembly/steps_content.py` by `assembly/build_guide.py`; pictures in `assembly/img/`.

**Open points:** Hafele load rating vs a loaded 15 mm ply bottom drawer unchecked; fronts are rigid on the boxes (no adjustment); runner setback (runner front 2 mm behind the front panel's back face) to be checked against the Hafele instructions; link-bolt length and the main run's rail position to be checked on site; plunger test pending; Alto drawbar section, clip and bracket outline taken from the supplied STEP files, fixed-runner block is a 14 x 45 envelope; the private build-pack artifact is a separate document (see the last section of this file).

## History (chronological; earlier sections describe superseded designs)

Files: `bench_with_extension.step` (whole bench + new unit, one assembly), `extension_unit.py` (golf script that builds it).
Drawer fronts face -X, over the KickboardExt position. All coordinates are bench.step's.

## Construction (16 mm ply carcass, no CNC)
- Carcass 773 mm clear width x 561 mm inside depth: 2 sides, bottom, full back. No stretchers: the benchtop is held by 9 steel angle brackets (25x25x2, 40 long; 3 per side, 3 on the back).
- Plinth: 115 mm high ply frame (front rail, two side rails, rear rail) that carries the unit. The kickboard is a separate 16 mm cover panel, set 60 mm behind the drawer fronts and held on by 4 screws from inside the plinth through the front rail. It carries no load and is removable. It replaces the KickboardExt placeholder and still ends against the main run's kickboard.
- Four drawers. Fronts 19 mm, 3 mm gaps: 163 / 163 / 210 / 210 mm (two sizes only) (3 mm between fronts, 5 mm under the benchtop; the bottom front hangs 20 mm below the carcass base, in front of the recessed kickboard). Same handle style as the main run.
- Drawer boxes 16 mm ply sides, front and back, 12 mm ply base: inside width 731 mm (= opening 773 - 42, Blum rule).
  - Base slot: 12.5 x 8 mm groove in sides (open at the rear) and front (stopped), hand router + fence.
  - Pocket holes (15 deg, 1" / 25 mm screws): sides into front (outer face of sides), back into sides (rear face of back). Keep screws out of the groove.
  - Box heights 130 / 130 / 165 / 165 mm (usable height inside about 105 / 105 / 140 / 140); the top pair and bottom pair are identical parts. The bottom pair is limited by the carcass base to 167 mm max (all inside Blum's opening - 20 mm limit).
- Semi-freestanding: unit stands on its own plinth. bracket screws up into the benchtop; 2 x M6 x 50 link bolts from the joint-end side to the main run's front framing rail. Remove those, cut the caulk line at the benchtop joint, lift out.

## Hardware (Blum TANDEM 563H5500B BLUMOTION, 550 mm, 30 kg) x4 pairs
Runners are modelled as simplified envelopes from Blum's published installation dimensions (opening - 42; side <=16 mm; 14 mm bottom clearance; runner holes 37 mm up; 3 mm setback), NOT Blum's own CAD. Locking devices (T51.1901.PS) and rear brackets (295.3750.01) are not modelled but are required: 8 locking devices + 8 rear brackets. Check against Blum's CAD/CAM download before ordering.

## Assumptions to confirm
- 5 mm overhang of the placeholder kickboard past the benchtop at the free end was not copied: the plinth is set 6 mm inside the carcass end.
- Placeholder benchtop is used as given (25 mm, 23 mm front overhang, 15 mm free-end overhang); joint to the main top is a butt joint.

## Corrections to the existing joinery (applied in this model; bench.step itself is unchanged)
- Existing doors and handles: fronts are 15 mm behind the benchtop edge (y 445.6), moved +13 mm.
- Main kickboard: front 38 mm behind the door fronts (y 483.6), moved +38 mm. The unit's kickboard panel is lengthened to meet it.
- Top framing rail: moved back 14 mm (front at y 464.6) so it sits behind the doors. Link bolts are therefore M6 x 65.

## Bay beside the extension: bin drawer + sliding door
The existing left door (and its handle) is removed. The 773 mm bay (x 1667.9-2440.9) is split, left to right:
- **Full-height pull-out bin drawer (315 mm front, x 1671.9-1986.9):** two fixed 16 mm ply side panels and a base (assumed: the reference model has no dividers or base here). One 315 x 730 x 19 front in the existing door plane. Tall ply box: sides/back 16 mm, 281 wide x 560 high x 550 long (inside 249 = opening - 42), tops at z -40 so they clear the sink bowl above (checked: no overlap with the sink); 12 mm base in grooves. Runners: Blum TANDEM 563H5500B envelope modelled, but a full-height loaded frame needs a heavier runner (70 kg class, confirm part number and tall-side limits with Blum); Blum TIP-ON push-to-open adapter (envelope only). Two short bins (237 x 255 x 360, ~21 L each) stand one behind the other on the base.
- **Internal wire basket above the bins:** 223 x 420 x 130, 5 mm bar (modelled as square section), on its own pair of 450 mm runners (13 x 40 envelopes) fixed to the tall drawer sides at z -205 to -165, for cleaning products and bin bags. It slides out independently once the drawer is open. Not modelled: runner part number, basket front lip/handle, load rating.
- **Sliding door (450 mm opening):** 16 mm ply, 470 x 697, x 1990.9-2460.9 closed, so it tucks 20 mm behind the extension and leaves no gap. It slides +X behind the extension (travel 452 mm) and parks with its leading edge flush with the extension's front plane (x 2442.9), fully hidden (door ends at x 2912.9, inside the extension's 3040.9 end). A push latch with a magnet in the track end holds it; pushing it in releases the latch, which pops the door about 20 mm back out so the edge can be gripped.
  - Hung from a low top track on the front of the main run's framing rail (track y 452.6-464.6, z 74-99) with two hangers; the track top is 2.5 mm below the link-bolt shafts and the door top is at z 72, so the bolts are cleared. The door top is 32 mm below the other doors; a 6 mm pelmet in the door plane (x 1990.9-2441, z 74-104.6) hides the track.
  - Routed stadium finger pull (30 x 70, 6 deep) near the leading edge.
  - Not modelled: track screws, hanger adjusters, the latch spring, and a floor guide (the door is held 15 mm behind the extension's side panel, which limits swing; a small bottom guide can be added in the bay).
- Not modelled: sink waste pipework (check it clears the bin drawer), TIP-ON mounting detail, panel fixing screws.
- Parameters: `DOOR_SLIDE` (0 closed, 452 parked, 432 popped out), `SD_W`, `RP1`, `BF_H`, `SHOW_DOOR`.

## Showing the bin drawer in use
Run extension_unit.py with `BIN_PULL` (mm the full-height drawer is pulled out, e.g. 500) and `BASKET_PULL` (extra mm the internal wire basket slides out, e.g. 350). Defaults are 0 (closed). The exported bench_with_extension.step is the closed state.

**Bin drawer update:** the wire basket is now fixed to the bay side panels on its own runners, above the bin drawer. The drawer sides and back are lowered (top at z -250) so the bins pull out underneath it and the basket stays put. `BIN_PULL` moves only the drawer and bins; `BASKET_PULL` slides only the basket.

**Full-height sliding door:** the sliding door is now the same height as the other doors (top at z 104.6). Its C-channel track hangs under the framing rail, and the door hangs from it by two plates in the 3 mm gap behind the door. The pelmet is gone. The two link bolts moved to x 2935 and 3015, beyond the door's parked position. `DOOR_SLIDE` is 0 closed and 452 parked.

**Stepped drawers:** `EXT_OPEN` (four fractions, top to bottom) opens the extension drawers, with `EXT_TRAVEL` (500 mm) as 100%. Default is all closed.

## Alternative drawers: Hafele Alto 732.25.602 (steel sides, no routing)
- This is now the main design: `DRAWER_SYS = "alto"` is the default in `extension_unit.py`, and `bench_with_extension.step` is the closed state (v50). The earlier plywood boxes on Blum TANDEM are `DRAWER_SYS = "timber"`, saved as `bench_with_extension_timber.step` (v47).
- No CAD file was available (Hafele's site blocked the download), so the sides and runners are envelope models built from the Hafele installation datasheet. Side wall thickness, lip and runner section are assumed.
- From the datasheet: base width = inside cabinet width - 75 + 0.5 (698.5), base length = runner - 5 (495), back width = ICW - 89 + 0.5 (684.5), 16 mm base and back, back height 70 (86 mm sides) or 148 (164 mm sides), minimum depth 510, front panel at least 105 (86) or 185 (164) high.
- Drawers 1 and 2 use 86 mm sides; drawers 3 and 4 use 164 mm sides (only the 86 mm set is confirmed at Bunnings). The bin drawer is unchanged.
- Clash check (v50, closed): no overlaps among the drawer parts, runners and carcass.
- Not modelled: front fixing brackets and the clips, rear hooks, screws, front drilling.

### Alto runner and side detail (updated)
- Runner: 29 wide x 39 high against the cabinet wall, bottom 11 below the base underside, 500 long. Footprint measured from the datasheet section drawing, so approximate (2 to 3 mm).
- Steel side wall: from the runner face to the base edge (37.5 from the wall, per the datasheet), full side height.
- Front bracket: 2 mm plate on the back of the front, 59 high, hole line 44.5 from the wall, plate edge 9 beyond it (datasheet labels).
- Still assumed: side wall thickness, the base lip, the runner section. A Hafele STEP file or dimensioned section would replace these.
- Clash check (closed): no overlaps among the drawer parts, runners, brackets and carcass.

### Alto sizes corrected (v55)
- All Alto steel sides are 86 mm. The Bunnings 204 x 500 set (I/N 0676280, $44.71) is the same 86 mm side with round gallery rails, overall 204. Drawers 1 and 2 use the 86 set; drawers 3 and 4 use the 204 set.
- The 204 set needs a front at least 225 mm tall (datasheet), so with `DRAWER_SYS = "alto"` the front heights are 133 / 133 / 240 / 240 (the timber version keeps 163 / 163 / 210 / 210).
- Back panel heights: 70 (86) and 188 (204), per the datasheet. The model backs are 2 mm lower.
- Gallery rails: two 10 mm round bars per side at 125 and 199 above the side bottom. The count and heights are assumed.
- Layout check: top drawer box clears the top stretcher by about 6 mm; each drawer clears the one below by about 20 mm. No overlaps in the closed state.

### All 15 mm ply (v58)
- `T = 15` and `FRONT_T = 15`: carcass, plinth, fronts, bay side panels, bin drawer, sliding door and the Alto bases and backs are all 15 mm (Bunnings STRUCTAply 15 mm, three sheets).
- The opening between the carcass sides is now 775 mm (outer faces fixed), so the Alto base is 700.5 x 495 and the backs 686.5 wide. The carcass back is 775 x 725 and the bottom 775 x 562.
- The sliding door is 15 mm. Hanger plates now start at the door back. The bin drawer front is 15 mm; its box is 4 mm further forward than before and the runners are set from the bay panel fronts.
- The bin drawer base is 15 mm in a 15.5 mm groove. The bay side panels keep their outer faces, so the inside gap is 293 mm.
- The bay base is existing joinery (not built, not in the cut list). It stays in the model as `bay_base`, group "Existing joinery (assumed)", for reference.
- Alto base and back: Hafele specifies 16 mm; 15 mm is a fit check to make on the first set. The minimum front thickness for the knock-in brackets is not known.
- Clash check (closed): no overlaps among the new parts. Cut list sizes come from the model's part sizes.

## Plywood boxes on the Alto drawbars (DRAWER_SYS = "drawbar")

The Alto steel sides are not used. The Hafele Alto runners are used on their own and the 15 mm ply boxes sit on the runner
drawbars (user-supplied STEP files: Left/Right Runner Drawbar, snap clip). Set `DB_FIX` in `extension_unit.py`:

- `DB_FIX = 1`: snap clip drops into the bracket pocket from above, its plate screwed up into the side's bottom edge
  (No.6 x 12, 3.5 mm pilot 11.4 deep); the 2.4 mm clip ears bite into the ply. The rear tab sits in a 10 x 4.6 mm notch
  in the inner bottom edge of the side.
- `DB_FIX = 2`: tab ground off flush, two 4.2 mm holes through the drawbar plate at the centre of the 8 mm underside
  opening (36.5 mm behind the bracket and 38 mm from the rear), two 12 mm screws per side up into the side.

Geometry from the user: drawbar outer face is 14 mm from the cabinet wall; the 8 mm opening faces away from the wall;
the clip drops in from above. Resulting layout:

- Box sides: 15 mm ply, outer faces 16 mm from the walls, sitting on the 15.2 mm flat of the drawbar. Outer width 743 mm.
- Box length 495 mm (drawbar 468 + bracket 26.5).
- The bracket hangs 31 mm below the drawbar plate, so every box bottom is >= 33 mm above its own front's bottom edge and
  >= 33 mm above the box below. Fronts are back to 163 / 163 / 210 / 210. Box heights 116 / 126 / 165 / 142
  (top to bottom); box bottoms at z -25.4 / -191.4 / -404.4 / -583.4.
- Fixed runner is an envelope (14 wide x 39 high against the wall); its height and position are assumed.

Files: `bench_with_extension_drawbar_clip.step` (DB_FIX 1), `bench_with_extension_drawbar_screws.step` (DB_FIX 2),
`drawbar_fix_detail.py` (single-side detail model), `extension_unit_alto_v58.py` (previous Alto-sides version).
Not yet updated: cut list, BOM and the build pack still describe the Alto-sides version.

### Update: three drawers (2 standard + 1 large) on the drawbars

Replaces the four-drawer layout above (box heights 116 / 126 / 165 / 142).

- Fronts 215 / 215 / 319 mm (3 mm gaps; bottom front hangs 20 mm below the carcass base).
- Box side heights 168 / 168 / 250 mm (top to bottom); box bottoms at z -77.4 / -295.4 / -583.4.
- Constraints used: box bottom >= 33 mm above its own front's bottom edge (bracket hangs 31 mm below the drawbar plate),
  >= 33 mm above the box below, box top <= its front's top - 1, top box clear of the front stretcher by 3 mm.
- Exports refreshed: `bench_with_extension_drawbar_clip.step` (DB_FIX 1) and `bench_with_extension_drawbar_screws.step` (DB_FIX 2),
  both clash-free in the closed state except the intended clip/bracket snap interference.

### Correction: the runner hangs below the drawbar (from the user's photographs)

The Alto runner is a telescoping steel stack, about 45 mm tall, that sits entirely below the drawbar plate; the fixing
plates are against the wall. The earlier model put a 14 x 39 block mostly above the plate. Now (`RUN_DROP = 45`, `RUN_CLR = 2`):

- Runner block: 14 wide (wall to drawbar outer face), z from plate - 45 to plate top.
- Each box leaves 47 mm between its top and the drawbar plate of the drawer above; the bottom plate is 47 above the carcass base.
- Box side heights 164 / 164 / 236 (top to bottom); drawbar plates 541 / 330 / 47 above the top of the carcass bottom.
- Sides 495 x 164 (x4) and 495 x 236 (x2); backs 713 x 135.75 (x2) and 713 x 207.75; bases unchanged.
- Extension unit still nests on two 15 mm sheets (92% and 75% full).
- Exports refreshed: `bench_with_extension_drawbar_clip.step` and `bench_with_extension_drawbar_screws.step`.

### Finger pull options (`PULL` in `extension_unit.py`; replaces the bar handles on the extension fronts)

A front-face cove has nothing to hook, so it only works with push-to-open. Three options are modelled (all with the snap-clip fixing, `DB_FIX = 1`):

- `PULL = "front_cove"`: 9.5 mm radius cove on the front-top corner, full width. 3 mm gaps, fronts 215 / 215 / 319. For use with a push-to-open plunger (room behind the box: 73 mm to the carcass back, 66 mm behind the runners). Export: `bench_with_extension_pull_front_cove.step`.
- `PULL = "back_cove"`: the same cove on the back-top corner, so fingers hook behind the lip. 20 mm air gap above every front (and under the benchtop), fronts 200 / 200 / 300. Box heights unchanged (164 / 164 / 236). Export: `bench_with_extension_pull_back_cove.step`.
- `PULL = "slot"`: finger-pull slot cutter, same gaps as `back_cove`. The profile is ASSUMED (20 mm tall x 9.5 mm deep rebate in the back face with a 9.5 mm inner corner radius): the cutter's listing could not be read. Export: `bench_with_extension_pull_slot.step`.

Cut list, BOM and pack still describe the earlier handle version; not yet updated for any option.

### Update: air gaps rejected; undercut finger groove as the fallback pull

The 20 mm air gaps (`back_cove`, `slot`) are no good, so the primary design is `front_cove` + a push-to-open plunger (to be tested on one assembled drawer). If the plunger fails, `PULL = "groove"`:

- A stopped undercut groove in the front face (dovetail bit): 300 mm long, centred; opening 15 mm tall starting 10 mm below the top edge; 8 mm deep; 14 degree undercut, so it is 19 mm tall at the bottom. Fingertips hook behind the face skin. Gaps stay 3 mm, fronts 215 / 215 / 319.
- Export: `bench_with_extension_pull_groove.step`.
- `back_cove` and `slot` stay in the script but are not recommended. The Rannb bit's silhouette (25.4 mm dia, 21 mm high, lobe + cove + shoulder) is in `SLOT_BIT`.

### Shop drawings

`shop_drawings/extension_unit_shop_drawings.pdf`: 10 sheets, A3 landscape, vector. Generated by `shop_drawings/build_all.py` (sheets in `sheets_a.py` to `sheets_d.py`, helpers in `sdlib.py`) from the dimensions in `extension_unit.py`.
Drawn state: `PULL = "front_cove"` (fallback groove on sheet 9), `DB_FIX = 1` (option 2 on sheets 6 and 8), three drawers, runner hanging 45 below the drawbar.
Known gaps: no top stretchers are modelled; bracket holes (Hafele pattern) are not dimensioned; the fixed runner is a 14 x 45 block and the bracket outline on sheet 8 is approximate; the plinth rear rail C6 is 3 mm proud of the side returns as modelled.

### Update: fallback groove is now full width

`PULL = "groove"` runs the whole 802 mm width of each front, open at both ends (`GRV_LEN = 810`): same undercut profile (15 mm opening starting 10 mm below the top edge, 8 mm deep, 14 degrees). One pass per front with a dovetail bit and a fence, no stops. The groove ends show at the end faces of the front. Export: `bench_with_extension_pull_groove.step` (replaced). Shop drawings sheets 1 and 9 updated.

### Update: base slot moved from the front panel to the back panel (`BASE_SLOT = "back"`)

The sides keep their through groove (15.5 x 8, lower edge 13 above the bottom edge). The back panel now carries the matching groove across its full width; the front is a plain panel (TASK.md originally asked for the front slot; changed at the user's request).

- Back panels: 713 x 159 (D1, D2) and 713 x 231 (D3), bottom edge 5 above the side bottoms so there is 7.75 mm of ply under the groove.
- Bases: 728.5 x 487.5. The front edge butts the front panel (flush with the side ends); the rear edge ends 0.5 short of the bottom of the back groove (7.5 into the back).
- Build order: sides and back first, slide the base in from the front, fit the front last (pocket screws through the sides into the front).
- Back pocket-hole heights above its bottom edge: D1, D2 at 40 and 70; D3 at 55, 123 and 181.
- Exports refreshed: `bench_with_extension_pull_front_cove.step` and `bench_with_extension_pull_groove.step`. The `back_cove` and `slot` exports and the two older `drawbar_clip` / `drawbar_screws` files predate this change and the rejected pull options.
- Shop drawings sheets 1, 2, 3, 7 and 10 updated. The build pack is still the older version.

### Update: fallback slot moved down

`GRV_TOP = 15`: the full-width undercut slot's opening (15 mm tall) now starts 15 mm below the top edge, so the visible slot is the same height as the lip above it. Ply above the slot at depth is 13 mm. Opening bottom is 30 mm below the top edge. `bench_with_extension_pull_groove.step` and shop drawing sheet 9 updated.

### Parked ideas (not modelled)

The user is leaning toward the snap clip (option 1), so these are on hold:
- Widen the boxes up to 20 mm (10 mm per side). The 11 mm wall-side gap above the drawbar is air; the fixing plate is 3 mm thick and rises about 18 mm above the drawbar top. 8 mm per side keeps 5 mm clear of the plate.
- Fix the drawbar into the base through a flat ply spacer strip (about 8 mm wide, thickness equal to the height of the groove's lower edge above the side bottom, glued under the base edge), or with a bottom rebate so the base sits on the drawbar.
- 9 mm bases: marginal for the large drawer (sag across 729 mm), and it does not reduce the number of 15 mm sheets unless the carcass back C4 and the bin drawer base also go to 9 mm.

### Update: fallback slot 25 / 25 with a 3 mm roundover

`GRV_TOP = 25`, `GRV_OPEN = 25`, `GRV_RAD = 3`: the slot opening is 25 mm tall starting 25 mm below the top edge (25 mm of material above), 8 mm deep, 14 degree undercut (29 mm tall at the back wall), full width. A 3 mm external radius rounds both edges of the opening. Ply above the slot at depth is 23 mm. Made in three operations with standard bits: (1) straight slot 25 x 8 along a fence, (2) 14 degree dovetail pass at 8 deep, (3) 3 mm roundover last (a dovetail wider than the slot would re-cut a roundover made earlier). The finished opening is the dovetail's diameter minus 4.0 mm at 8 deep, so a 29 mm bit gives 25 mm; a 1-1/4 in (31.75 mm) bit gives 27.8 mm.

## Fallback slot: 25 mm between the radii (v34)
With the 3 mm roundover each arc leaves the flat face 3.84 mm beyond its sharp corner, so the lower edge was raised: corner-to-corner opening 17.32 mm (GRV_OPEN), giving 25.0 mm between the outermost points of the two radii. Top edge (25 below the top), 8 deep and 14 deg unchanged; back wall 21.3 tall. Dovetail bit = opening + 4.0 (21.3 mm; a 7/8 in bit gives 18.2). Model valid, 84 parts.

## Rebate pull option (PULL = "rebate", v35)
Slot opened to the top edge: only the lower dovetail lip remains. Full width, 8 deep, 14 deg undercut on the lower wall, 3 mm roundover on the lower lip, 25 mm from the top edge to where the radius meets the face (corner 21.16 below the top; back wall 23.2 below the top). 7 mm back skin remains above the cut. Straight rebate pass, then dovetail pass, then roundover. Model valid, one solid per front. Export: bench_with_extension_pull_rebate.step. Shop drawing sheet 9 not yet updated for this option.

### Rebate narrowed to 15 mm (v36)
User asked for a narrower rebate and both pulls on sheet 9. REB_SPAN = 15: top edge to the radius tangent point 15 mm (corner 11.16 below the top, back wall 13.2 below). Same 8 deep, 14 deg undercut, 3 mm roundover. Valid, one solid per front; bench_with_extension_pull_rebate.step re-exported. Sheet 9 now shows the slot (B, C) and the rebate (B2).

## Assembly guide
`assembly/extension_unit_assembly_guide.pdf` (A4, 9 pages) and `assembly/ASSEMBLY_GUIDE.md`, generated from `assembly/content.py` by `assembly/build_guide.py`; pictures in `assembly/img/` (renders of the primary design: front cove, snap clip). Covers parts, routing, plinth, carcass, runner heights (drawbar plates 541 / 330 / 47 above the top of C3), drawer boxes, both fixing options, plunger test, the three pull options, kickboard, benchtop, link bolts, removal and open points. Not proven by a build. Open points include the runner setback (2 mm behind the front panel's back face, 4 mm forward of the carcass edge as modelled), unmodelled Hafele bracket holes and no top stretchers.
The guide treats fixing option 1 (snap clip) as the main path (user's choice); option 2 appears as a marked alternative.

### Assembly guide: pictorial steps
`assembly/steps_content.py` (9 steps) and `assembly/build_guide.py` now put an IKEA-style section first: one exploded 3D picture per step, then the written guide. Pictures come from `AV_STEP` (1 to 9) in `extension_unit.py`, a view mode that hides and explodes parts per step (0 = normal model). Render with views [1,1,-0.8] (front/free-end/above), [1,-1,-0.8] for the pull profiles, and `faint` for parts already built. The renderer ignores part colours, so contrast is solid versus see-through. Images are in `assembly/img/`.

### Cutting for a panel saw that only cuts on 100 mm multiples (sheet 11)
`shop_drawings/nest_round.py` builds `round_layout.json`; sheet 11 draws it. Every store cut is a rip or cross-cut on a multiple of 100 mm; each part is cut as a rough blank (size rounded up to 100, stacked parts share a blank) and trimmed at home (11 blanks, 10 of which hold more than one part, so 13 home separation cuts besides trimming). No all-round layout fitted on two sheets (a random strip search found none; rounded blank area alone is about 6.2 m2 against 5.76 m2 on two sheets), so it needs a third sheet, which is only 13% used (a 1900 x 200 strip) and has room for the bin drawer, bay and door parts. Sheet 10 (exact sizes, two sheets) is unchanged.

## Rear setback for the skirting board (REAR_SETBACK = 30, v50)
A skirting board projects 20 to 25 mm from the wall behind the unit. The carcass and plinth now stop 30 mm short of the wall (`REAR_SETBACK` in `extension_unit.py`; `X_BACK_C` = carcass rear). The front and the benchtop (600 deep) are unchanged, so the benchtop overhangs the back of the carcass by 30.
- C1, C2: 740 x 547 (was 577). C3: 775 x 532 (was 562). C7 side rails: 486 (was 516). C4, C5, C6, C8 and all drawer parts are unchanged. Inside depth 532.
- Free space behind the drawer boxes: 43 mm (was 73). A push-to-open plunger body should pass through a hole in C4 into the 30 mm gap behind the carcass (above the skirting).
- Link bolts moved to x 2935 and 2985 (holes at 471.1 and 521.1 from the front edge of C2; were 471.1 and 551.1, which would have been off the shorter side).
- Benchtop brackets are unchanged (the rear ones follow C4). Alto 500 mm runners still fit: the runner rear end is 36 mm in front of C4.
- Shop drawings (sheets 1 to 5, 9, 10, 11), the cutting layouts and the assembly guide are updated. Sheet 11's layout was re-run. The build pack is still the old version. Exports of the STEP files predate this change.

### Update: rear setback now 40 mm (REAR_SETBACK = 40, v51; replaces the 30 mm figures above)
User's choice. C1, C2: 740 x 537. C3: 775 x 522 (inside depth 522). C7 side rails: 476. 33 mm free behind the drawer boxes (runner rear ends 26 mm in front of C4), 40 mm gap behind C4 for a plunger body. Link bolts at x 2935 and 2975 (holes at 471.1 and 511.1 from the front edge of C2); the last side bracket moved to x 2970 (506 from the front). Shop drawings, cutting layouts (sheets 10 and 11) and the assembly guide are updated; the build pack and older STEP exports still show the old depth.

## Design review (v53)
Changes made:
- C4 back is full height, 775 x 740, standing on the plinth rear rail with C3 butting its front face (was 725 high, leaving a 15 mm slot underneath). The rear plinth rail C6 is now flush with the C7 rail ends.
- New front top rail C9, 775 x 60 x 15, between the sides at the top (the carcass had no top tie at the front).
- Link bolts: the two 6.5 mm holes in C2 sat 5.1 mm below the top edge, leaving about 1.9 mm of ply. They are now slots open to the top edge (6.5 wide, 8.4 deep), so the bolts are fitted before the benchtop goes on.
- Benchtop brackets moved to x 2560 / 2720 / 2880 (96, 256, 416 from the carcass front): the old rear one overlapped C4 (4.1 mm) and a link bolt, and the front one would have hit C9.
- Carcass and plinth joints are now glued pocket-screw butt joints (25 mm coarse screws, 30 in all) instead of No.8 screws into end grain; 12 No.8 x 40 hold the carcass down onto the plinth. Bracket screws specified (18 x No.8 x 12, 18 x No.8 x 16).
Checks: model valid, 85 parts; contacts check on the unit, benchtop and fixings finds no clash except the accepted snap clip / bracket interference and screws in their holes; every modelled part size agrees with the schedule on sheet 1.
Open (not changed): Alto 86 mm load rating vs a loaded 15 mm ply bottom drawer is unchecked; fronts are fixed rigidly to the boxes (no front adjustment); Hafele bracket holes not dimensioned; link bolt length and the main run's rail position to be checked on site; the assembly step pictures, build pack and STEP exports predate this review.

### Every joint modelled (v55)
`extension_unit.py` now models the carcass and plinth joints and the bracket fixings as well as the drawer joints:
- 30 pocket holes cut into the parts, each with its 25 mm screw (parts `carcass_pocket_screws` 22, `plinth_pocket_screws` 8): C3 4 per side at 96, 216, 336, 456 from the front edge (underside); C4 5 per side at 70, 210, 350, 490, 630 above its bottom (rear face); C9 2 per end at 15 and 45 (underside); C5 and C6 2 per end at 30 and 85 above the floor (inner faces).
- `carcass_hold_down_screws`: 8 No.8 x 40 down through C3 into C5 (4) and C6 (4).
- `bracket_screws`: 36 (2 per bracket leg: No.8 x 12 into the carcass, No.8 x 16 up into the benchtop).
- Already modelled: drawer pocket screws, base grooves, snap clip screws, clip pilots and rear-tab notches, kickboard screws, link bolts and their slots in C2.
- Not modelled: the Hafele runner fixing screws and holes (the hole pattern is not in the supplied files), the front fixing screws through the Hafele brackets, and the main run's rail that takes the link bolts.
Screws overlap the part they screw into (no pilot holes are cut in the receiving part): expected in contacts.

### Fix: pocket hole bore (v56)
`pocket_set` cut the 9.5 mm bore from 30 to 16 mm behind the end-grain exit point, but the board face is about 34.8 mm behind it (9 mm / sin 15 degrees), so each pocket was a closed void with only a sliver breaking out. The bore now runs from the screw shoulder out through the face (30 mm cylinder ending at the shoulder). It applies to every pocket joint (drawer boxes, carcass, plinth); all parts stay valid single solids.

### Fix 2: pocket bore now clears the face completely (v57)
The v56 bore (30 mm) reached past the face but its far end disc was still only 2.9 mm outside it, and at 15 degrees that disc needs about 4.6 mm clearance, so the pocket ended in a flat cut inside the board instead of opening out. The bore is now 50 mm long (far end 8 mm clear of the face) and the pocket opens as a full elliptical slot. Applies to all pocket joints. Parts still valid, single solids.

## Documentation refresh (model v57)
- Notes: current-design summary added at the top; exports of older designs moved to `archive/`.
- STEP exports regenerated from the current model: `bench_with_extension_pull_front_cove.step`, `_pull_groove.step`, `_pull_rebate.step`.
- Shop drawings: all 11 sheets rebuilt (cover notes, schedule with C4 full height and C9, plan with C9 and the link-bolt slots, notes on joints and the rear setback).
- Assembly guide: all pictures re-rendered from the current model (top rail, full-height back, brackets); text updated (nesting percentages, store-cut option, removal order, open points).
- Build pack (private artifact, https://claude.ai/artifact/Xyba81G5U1uNgDKA3Air8E, now version 17): BOM, cut list, routing, assembly steps, open items, timeline and the unit pictures updated to the current design (cove pulls and plunger instead of handles, back base slot, full-height back, C9, pocket-screw joints, slots for the link bolts, 40 mm rear setback). Bay, bin drawer, basket and door content is unchanged.
- The re-rendered pictures came out with a dark background (viewer in dark mode); their background was recoloured to light beige. Faint (see-through) parts keep a darker tint.


## Plinth rework and D3 height (model v73)
- Plinth parts renamed so they differ from the carcass parts: P1 front rail (was C5), P2 rear rail (C6), P3 free-end side rail and P4 joint-end side rail (C7), Kb kickboard cover (C8). Model part names: P1_front_rail, P2_rear_rail, P3_side_rail_free_end, P4_side_rail_joint_end, Kb_kickboard.
- Carcass fixed to the plinth by pocket screws from inside the plinth frame, up into the underside of C3 (4 from P1, 4 from P2) and the bottom edges of the sides (2 from each of P3, P4); the old 8 No.8 x 40 hold-down screws are gone. The carcass is assembled upside down and the frame screwed to it, then turned over. P2 moved forward to sit fully under C3 (its rear face level with C3's rear edge); P3 and P4 still run 8 mm on under C4, which stands on their ends. C4's footing is therefore only 8 mm of bearing: it is held by glue and the pocket screws into the sides and C3.
- D3 front now ends level with the existing doors (bottom 120 above the floor, 5 above the kickboard), so it is 294 high (was 319, tops unchanged). To keep it covering the carcass base the plinth frame is 125 high (was 115) so C3 sits 5 mm above the front's bottom edge; the kickboard cover stays 115 so the 5 mm gap under the doors matches the main run. Consequences: carcass sides 730 high (was 740), D3 box sides 226 and back 221 (was 236, 231), drawbar plate heights 531 / 320 / 47.
- Top rail C9: kept. It is cheap (one 775 x 60 offcut, 4 pocket screws), keeps the open front of the carcass square while it is carried and the runners parallel (they need to be level within 1 mm), and the benchtop brackets only help after the top is on. Structurally it is not essential once the benchtop is fixed.
- Pictures re-rendered in light mode (no recolour); assembly pictures have dashed lines showing where fasteners go (`av_assembly_lines` part, built in `AV_STEP` mode from the screw positions). Runner fixing screws are not shown because their hole pattern is not modelled.
- Shop drawings are now A4 landscape (297 x 210): same layout on the old A3 grid scaled by 0.707, all text is at least 5 pt (about 1.8 mm), long lines wrapped; print at 100%.
- Sheet 10 now carries a grouped cut list (25 pieces: qty, length, width, part and sheet) beside the cutting diagrams, for a store that will make all the cuts.

## Benchtop height, hem and front set-back (model v107)
- The existing benchtop top is 899-900 above the floor (bench.step's placeholder had 880 and 25 thick, so the reference benchtop in the model was moved up 20). The extension top is 26 mm timber, so its underside and the top of the carcass are at 874 (was 855), 19 mm taller. Carcass sides and back are 749 high.
- The 12 mm hem under the front edge of the top only is modelled on `ref_BenchtopExt` (placeholder replaced by the 26 mm top plus a front hem strip, 12 wide). To make room at the front the unit front is 15 mm further back: C1, C2 522 deep, C3 507, plinth side rails 461, drawer fronts 17 behind the benchtop edge, front overhang 38. The rear and the 40 mm skirting setback are unchanged, so the void behind the boxes is 18 mm (was 33).
- The extra 19 mm of height went to D3: front 313, box sides 245, back 240. D1 front is 205 (was 215): its top must stop 15 mm below the underside of the top, because the 12 mm front hem hangs below the underside and a front only 5 mm below it could not open past the hem. D2 stays 215. D3's bottom edge is still level with the existing doors. Drawbar plate heights above C3: 550 / 339 / 47.
- Brackets and C3 pockets moved 15 mm back with the front (still 96, 256, 416 and 96, 216, 336, 456 from the carcass front). The link-bolt slots in C2 are now 27.4 deep, which also lets the unit sit about 20 mm higher or lower on the bolts.
- Push-to-open: the rear plunger (through C4) still has 18 mm behind the box. Side-mounted ejectors in the front end grain of C1/C2 were suggested, but the runners fill the 16 mm gap beside each box, so nothing fits there; not drawn, untested.

## Mitre pull (PULL = "mitre", default) - final
- Top edge of D1, D2 and D3: 45 degree mitre cut through the full 15 mm front thickness, R3 roundover-bit nose: the arc is tangent to the front face 14.9 mm below the top edge (bit set 2 mm higher than the tangent position) and meets the mitre face at an edge, not blended, which is broken with an R1 fillet (hand sanded; `MIT_FIL` in the script, nose top then 12.16 below the top edge); nose top 12 mm below the top edge, sharp apex 9.7 mm down the face (`MIT_BIT_UP`, `MIT_L` in the script). D1 and D2 have a 45 degree mitre on the front-bottom edge, 15 mm high on the face (`MIT_BOT_D`), full thickness with no land (`MIT_BOT_LAND = 0`) and no sharp edge: R2 on the thin back edge, R3 on the arris (the runners self-close and could trap fingers). The R2 lifts the lowest point 2.83 mm, so the closed gap to the nose below is 5 mm. It opens a funnel above the nose of the front below for fingers (the old R10 cove stays selectable with `MIT_BOTTOM = "cove"`). One cutter profile per front, single solids.
- Each nose stays about 5 mm below the lowest point of the front above (the rounded thin edge of its bottom mitre; 2 mm before that edge was rounded), so no front can catch the one above when it opens; fronts overlap 10 mm vertically (GAP = -10).
- Fronts 212.7 / 212.7 / 326.3 mm (D1 and D2 identical, one cut list line; `MIT_FH12`; D3 takes the remaining height); D3 bottom level with the doors (5 mm below plinth top). D1's top edge is set so that its mitre plane is 15 mm (vertical) below a parallel 45 degree plane through the benchtop hem's back-bottom edge (`MIT_HEM_GAP`); this is the fingertip gap for D1.
- Box sides stop at the base of each mitre (24.7 mm below the front top): sides 153 / 153 / 231, backs 148 / 148 / 226, 5 mm clearance under the runners; plate tops above C3 534 / 331 / 50.
- Top strip (`TOP_STRIP`): a false front above D1, 802 x 32.3 x 15 ply in the plane of the fronts, plain top at the benchtop underside, bottom mitre identical to D1/D2 (its bottom edge is where a front above D1 would end, 10 mm overlap, so the gap above D1 repeats the other gaps and the open carcass top is closed in). It is glued to a 6 mm packer (775 x 15) that is glued to the front of the top rail C9; it carries no load. Parts `top_strip`, `top_strip_packer`.
- Catch step (`MIT_CATCH = 7.5`): the 45 degree wall of the top mitre runs only the front 7.5 mm; behind it a half-thickness rebate from the back leaves a vertical 7.5 mm catch wall for the fingertip (a 45 degree ramp alone needs friction >= 1 to pull), then a flat shelf at the old back level (24.7 below the top edge), so box heights are unchanged. Cut order: rebate (straight bit), 45 degree lip (chamfer cutter), R3 roundover, hand-sanded R1. Optional 14 degree dovetail pass into the wall.
- Design review (three read-only agents: DFM/A, ergonomics, function) actioned: fronts are cut and finished first and dry-fitted with screws only (glue after the open-and-close test); fronts fix through 6 mm oversize holes (about 1 mm play) on 2 mm spacers, no extra adjustment hardware (closest front-to-front approach is 5 mm after rounding, reveal 15 mm); top strip packer is 20 high and the optional screws are No.8 x 75 from the back edge of C9; benchtop brackets and link bolts are fitted before the drawer boxes; the drawer base gets a glue bead along its front edge; the store-cut layout (sheet 11) keeps the grain direction on every part (still 3 sheets). Base ply stays 15 mm (checked: a thinner base saves 0.7-1.4 kg per box and adds a ply line). Still open: Alto 30 kg rating against D3 (about 10 kg box + contents), plinth side-rail bearing (9 mm under the sides), kickboard fixing access, timber top movement, edge sealing of the ply plinth.
- Export: `bench_with_extension_pull_mitre.step`. Alternatives remain selectable: front_cove, groove, rebate.
