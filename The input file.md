In the input file there are some keywords that the code use to recognize and read the input variables. The order of the keywords in the file is not important. Some of that Keywords has a default values.

#### Keywords without  default values
#### #Molecule_File

*\# Molecule_File*
*Character*

The name of the .xyz file is written on the next line following the keyword. For example:
*\# Molecule_File*
*carbon.xyz*

#### #Box_info

*\# Box_info
Real(1) Real(2) Real(3)*

Cell periodic constants in Angstrom (only orthogonal cells, presently). For Example:
*\# Box_info
60.0 60.0 60.0*

#### Keywords with default values
#### #Cube_Mesh_Size

*\# Cube_Mesh_Size*
*Real*
 
 Size of the cubic grid in Angstrom. For Example:
*\# Cube_Mesh_Size*
*1.0*

Default: 1.0 A

#### #Out_Mesh_Size

*\# Out_Mesh_Size*
*Real*

Step to output the volumes (usually = dMesh) in Angstrom. For Example:
*\# Out_Mesh_Size*
*1.0*

Default: 1.0 A

#### #Threshold_small

*\# Threshold_small*
*Real*

Value in Angstrom of the maximum wall distance to discard a cube of the grid. For example if for a void cube all the minimum wall distance for every direction are smaller than Real, this cube will be considered as "filled", so part of the material because there is not any probe that can fit in that space.
For Example:
*\# Threshold_small*
*7.0*

Default: 7.0 A

#### #Do_Accessible
*# Do_Accessible*
*Character*

Choose whether to exclude the volume not accessible by the probe from the distribution of V(MinD) or to consider all the porous volume.
The options are:
- "yes": use only the accessible volume
- "no": use the total porous volume

For Example:
*# Do_Accessible*
*yes*

Default: yes

#### #XYZ_out_file

*# XYZ_out_file*
*Character*

Choose whether to print the cavity's "porous.xyz" output file by assigning a different atom to each block so that using software like VMD you can get a representation of the cavity with different colors based on the block classification.

The options are:
- "no". In this way the file won't be printed.
- "basic". Each block will have a different color distinguishing: 
	- **Ar**: blocks filled with the material atoms
	- **Kr**: blocks that are filled because their maximun wall distance is lower than *Threshold_small*
	- **He**: Not accessible volume (if required)
	- **Ne**: the surface 
	- **Xe**: the bulk volume
- "classification". Each block will have a different color distinguishing: 
	- **Ar**: blocks filled with the material atoms or blocks that are filled because their maximun wall distance is lower than *Threshold_small*
	- **He**: Not accessible volume (if required)
	- **Ne**: the surface and bulk volume blocks with MinD < 7.0 A
	- **Kr**: the surface and bulk volume blocks with < 7.0 A MinD < 20.0 A
	- **Xe**: the surface and bulk volume blocks with < 20.0 A MinD < 35.0 A
	- **Rn**: the surface and bulk volume blocks with < 35.0 A MinD < 50.0 A
	- **Ca**: the surface and bulk volume blocks with MinD > 50.0 A
- "total". Each block will have a different color distinguishing: 
	- **Ar**: the material
	- **Ar**: block that are filled because their maximun wall distance is lower than *Threshold_small*
	- **Kr**: the not accessible volume (if required)
	- **Li**: the surface volume blocks with MinD < 7.0 A
	- **Na**: the surface volume blocks with < 7.0 A MinD < 20.0 A
	- **K**: the surface volume blocks with < 20.0 A MinD < 35.0 A
	- **Rb**: the surface volume blocks with < 35.0 A MinD < 50.0 A
	- **Cs**: the surface volume blocks with MinD > 50.0 A
	- **Be**: the bulk volume blocks with MinD < 7.0 A
	- **Mg**: the bulk volume blocks with < 7.0 A MinD < 20.0 A
	- **Ca**: the bulk volume blocks with < 20.0 A MinD < 35.0 A
	- **Sr**: the bulk volume blocks with < 35.0 A MinD < 50.0 A
	- **Ba**: the bulk volume blocks with MinD > 50.0 A

For Example:
*# XYZ_out_file*
*total*

Default: no

#### #Surface_computation

*# Surface_computation*
*Character*

Choose whether results from the surface computation are written to the "Texture.txt" output file.
The options are:
- "yes": write the results
- "no": don't write the results

For Example:
*# Surface_computation*
*yes*

Default: yes

#### #Probe_Rad
*# Probe_Rad*
*Real*

Value in Angstrom of the radius of the spherical probe used for the surface computation and to compute the accessible volume (if required).
For Example:
*# Probe_Rad*
*2.0*

Default: 2.0 A

#### #Angle_scan
*# Angle_scan*
*Real*

Number of directions used to scan the space starting from a block to compute the distance from the walls.
The options are:
- 120
- 180: Using this value gives a more precise description but increases the computation time.
We suggest using the value 120 as with 180 the calculation time increases a lot and the increase in detail in the results is not very large.
For Example:
*# Angle_scan*
*120*

Default: 120
