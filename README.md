# Build Log

## Shop Drawings

### Cut List

- While Bunnings offer panel saw cutting services, their website says they'll only make cuts to 100mm lengths.
- Nonetheless, it'd be great if they could cut all the parts for me at the store
  - It would save me a bunch of time
  - 2400x1200 sheets don't quite fit in my car, so I need _some_ cuts done anyway, in for a penny in for a pound?
- I had Claude generate two nestings for the same cutlist to take with me
  - Tightly nested, all the parts fit neatly into two sheets, saving about 80 dollary-doos (this only works if they're willing to make precision cuts though)
  - As many cuts as possible per their websites 100mm increment constraint to hopefully save me at least a little material handling effort

<img style="width: 700px" src="./media/0.1 Cutlist Tight.png"/>
<img style="width: 700px" src="./media/0.1 Cutlist Sparse.png"/>

## At Bunnings

- The 100mm constraint isn't legit,
- When I gave them the tight cutlist and asked cheekily if they wanted to cut 25 parts, the first guy looked at it and asked the second "hey do you want to cut all this?", who responded with a laugh (as in "haha \[_not really_\]), followed by saying they can only guarantee cuts are only accurate to ±5mm,
- since I'm looking for tolerances closer to ±0.5mm, clearly I was going to be doing all the precision cuts myself
- I gave them the 2nd sheet, which they went ahead and cut, with a couple of minor variations
  - Sheet A: exactly as Claude intended
  - Sheet B: `B3` `B2` and the offcut in the bottom right were merged into a single `B2/3` blank (since the extra shop cuts wouldn't help me in any meaningful way)
  - Sheet C: Apparently Bunnings won't rip @ 200mm for safety reasons, so I checked the part dimensions on that sheet, and told them to just cut the sheet into 4 equal-sized blanks

## Precision Cuts

- After getting home with the blanks, blindly trusting Claude's cut list, I went ahead and measured & cut all the parts

<img style="width: 700px" src="./media/1.0 cuts_done.jpg"/>

## Routing

Having the parts cut to size, the next step was to route grooves for the drawer bases to slot into, like so:

<img style="width: 700px" src="./media/drawer base grooves.png"/>

I put together a router jig on the welding table (the same welding table that in a previous life was the fixture plate for the CNC milling machine George, Max, and I built back in 2020)

<img style="width: 700px" src="./media/3.0 router_jig.jpg"/>

As part of this setup I resized an issue with the shop drawings

<img style="width: 700px" src="./media/slot datum.png"/>
> - The datum should've been the top edge of the panel, not the bottom (so any height variation in the panels will be visible only from underneath, i.e. not)

______________________________________________________________________

## **From here on, I don't really have much to say about this process, it all went together easily. What follows is therefore basically just series of pictures I took along the way.**

## Fit up

With the routing done, all that was left was to see if everything fit together and fits in the space.

#### Plinth

<img style="width: 700px" src="./media/4.1 plinth_assembled.jpg"/>

#### Carcass & Plinth

<img style="width: 700px; height: 800px; object-fit: cover" src="./media/5.2 carcass_assembled.jpg"/>

#### Drawer

<img style="width: 700px" src="./media/5.4 drawer test fit.jpg"/>

## Test fit in the space

#### Drawer

<img style="width: 700px; height: 600px; object-fit: cover;" src="./media/5.5 drawer test fit.jpg"/>

#### Carcass

<img style="width: 600px; height: 600px; object-fit: cover;" src="./media/5.3 carcass_test_fit.jpg"/>

### Oil & Assemble Drawers

#### Carcass & Drawer Parts

<img style="width: 700px" src="./media/6.1 carcass_and_drawers_oiled.jpg"/>
#### Benchtop
<img style="width: 700px" src="./media/6.2 benchtop_oiled.jpg"/>
#### Drawers
<img style="width: 700px" src="./media/7.0 drawers_assembled.jpg"/>

## Installation

#### Carcass & Benchtop

<img style="width: 700px" src="./media/8.0 carcass_with_benchtop_installed.jpg"/>

#### Testing the bottom drawer

<video style="width: 700px" src="./media/9.0 drawer_runner_check.mp4"/>

#### Drawers installed

<img style="width: 700px" src="./media/10.1 assembled_drawers_out.jpg"/>

#### Coffee up!

https://github.com/user-attachments/assets/8676af79-2570-4209-ad91-c1c517506db3

