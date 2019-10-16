from stl_normalize import GcodeGenerater

gcode_gen = GcodeGenerater()
gcode_gen.unit_E = 1.0
gcode_gen.infile = './hexhab3x_3rd-1_R.stl'

gcode_gen.analyze()

print('layer count: ', len(gcode_gen.z_range))
print(gcode_gen.z_range)

print(len(gcode_gen.paths[44]))
print(gcode_gen.paths[44])
print(len(gcode_gen.paths[45]))
print(gcode_gen.paths[45])

for i in range(len(gcode_gen.z_range)):
    if len(gcode_gen.paths[i][1]) == 1:
        print(i)
