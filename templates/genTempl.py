import os

f = open("A_siswa.html", "r")
a = f.read()
f.close()

namaNya = []
# namaNya = ["mapel","prodi","kelas","mapelGuru","kelasSiswa","jadwal"]
for x in namaNya:
	with open("A_"+x+".html", "w") as f:
		f.write(a)
		f.close()
	print(x)
# print()