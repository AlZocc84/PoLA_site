Several output files are produced:
#### Texture.txt
In this file a summary of textural results is written.
In the first part is reported:
- Solid weight (g/mol) of the material
- Unit Cell volume (A^3): the volume of the unitary cell
- Apparent density (g/cm^3): the solid weight of the material divided by the volume of the unitary cell
- Skeletal volume (A^3): the volume occupied by the material
- Skeletal density (g/cm^3): the solid weight of the material divided by the skeletal volume

In the second part there is the porous volume analysis.
There is:
- The porous volume (Accessible volume if required) in A<sup>3</sup> and in cm<sup>3</sup>/g
- The porous accessible (or total) volume fraction: the porous volume divided by the volume of the cell
- V(MinD) in cm<sup>3</sup>/g for each range of MinD
- The total surface in m<sup>2</sup>/g (if required)
- The surface in m<sup>2</sup>/g for each range of MinD (if required)

#### VMinD.txt
This file has 3 columns:
- MinD in A 
- V(MinD) in A<sup>3</sup>
- V(MinD) in cm<sup>3</sup>/g

#### Cumulative_volume.txt
This file has 3 columns:
- MinD in A 
- The Cumulative V(MinD) in A<sup>3</sup>
- The Cumulative V(MinD) in cm<sup>3</sup>/g

#### Simplified_vol.txt
This file contains the values of V(MinD) "simplified", i.e. considering the value of V(MinD):
- total Volume
- V(MinD) with MinD < 7A
- V(MinD) with 7A < MinD < 20A
- V(MinD) with 20A < MinD < 35A
- V(MinD) with 35A < MinD < 50A
- V(MinD) with MinD > 35A
#### wrapped_coord.txt
Before all the computation the coordinate of the system are translated so that the atom with the lowest coordinates is centered in the cube (0,0,0), and if required the atom that are outside the cell are wrapped into the box cell.

#### porous.xyz
If required, each block is assigned a different element (i.e., a different color) to describe the cavity in this file, depending on the mode requested in the input.