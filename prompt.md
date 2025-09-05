flask app to display an XY plot with two lines A and B.

- each line starts at the origin,
- each line ends at y = DISTANCE and x = 0
- DISTANCE should default to 1.0 but be user selectable with an input element with a spinner control to adjust up and down in tenths. the units are selectable with a drop down box and default to miles.
- the x,y data for each of the lines is calculated from their course angle with 0 being vertical in a positive y direction and 90 degrees being horizontal in a positive x direction.
- the angle for each track should default to AngleA = 40 and AngleB=50. Both need to be user selectable. the data points should include y = 0 and y = DISTANCE / 2 and y = DISTANCE.
- label each line with the length of the line.
- add another input box which will contain speed. starting defaults will be A = 4.0 and B = 5.0 these should be editable and adjustable with spinner controls. Add a drop down selection box to choose units, default to knots, nautical miles per hour.
