#  __Komponen Yang Diperlukan__ #
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_restful import Resource, Api
from gevent.pywsgi import WSGIServer

#  __Import MyLib__ #
from Lib import Database

app = Flask(__name__)
db = Database()
app.secret_key = "rahasia"
api = Api(app)
app.debug=True

def startServer():
    # app.run(host="127.0.0.1", port="3001", debug=True)
	print("Starting Server...")
	print("url pattern: /smkindonesia")
	http = WSGIServer(('0.0.0.0', 3001), app.wsgi_app)
	http.serve_forever()

@app.route('/', methods=["GET"])
def index():
	return redirect("/smkindonesia/")

@app.route('/smkindonesia/', methods=["GET"])
def index2():
	return render_template("login.html")

@app.route('/smkindonesia/<string:path>', methods=["GET"])
def arah(path):
	Rtr = "Upsss... Mau Kemana BoyyyPERTAMA..."
	try:
		lvl = session["level"]
		if lvl == "1":
			if path == "admin":
				Rtr = render_template("admin.html")
		if lvl == "2":
			if path == "guru":
				Rtr = render_template("guru.html")
		if lvl == "3":
			if path == "siswa":
				Rtr = render_template("siswa.html")
	except KeyError as ke:
		print("BELUM LOGIN Boyy!")
		print(session)
		return redirect("/smkindonesia")
	except Exception as ex:
		import traceback
		tb = traceback.format_exc()
		print(tb)
		print("<--- Something Error --->")
		print(ex)
		return redirect("/smkindonesia")

	if path == "logout":
		session.clear()
		Rtr = redirect("/")
	return Rtr

@app.route('/smkindonesia/<string:path>/<string:where>', methods=["GET"])
def arahKe(path, where):
	Rtr = "Upsss... Mau Kemana BoyyyKEDUA..."
	try:
		lvl = session["level"]

		""" ROUTING ADMIN """
		if lvl == "1":
			if path == "admin":
				if where == "guru":
					Rtr = render_template("A_guru.html")
				if where == "siswa":
					Rtr = render_template("A_siswa.html")
				if where == "mapel":
					Rtr = render_template("A_mapel.html")
				if where == "prodi":
					Rtr = render_template("A_prodi.html")
				if where == "kelas":
					Rtr = render_template("A_kelas.html")
				if where == "mapelGuru":
					Rtr = render_template("A_mapelGuru.html")
				if where == "kelasSiswa":
					Rtr = render_template("A_kelasSiswa.html")
				if where == "jadwal":
					Rtr = render_template("A_jadwal.html")
		
		""" ROUTING GURU """
		if lvl == "2":
			if path == "guru":
				sql = "SELECT * FROM guru NATURAL JOIN mapel_guru NATURAL JOIN jadwal NATURAL JOIN mapel NATURAL JOIN kelas NATURAL JOIN prodi WHERE kode_guru=%s"
				df_guru = db.getData(sql, [str(session["kode"])], True)
				nmguru = df_guru["nama"].iloc[0]
				kls = df_guru["kelas"].iloc[0]
				kdprd = df_guru["kode_prodi"].iloc[0]
				ket = df_guru["ket"].iloc[0]
				nmprodi = df_guru["nama_prodi"].iloc[0]
				dtGuru = {
					"nama": nmguru,
					"kdkls": f"{kls} {kdprd} {ket}",
					"kdprd": f"{kls} {nmprodi} {ket}"
				}
				if where == "nilai":
					sql = "SELECT * FROM mapel_guru NATURAL JOIN mapel WHERE kode_guru=%s"
					df_prodi = db.getData(sql, [str(session["kode"])], df=True)
					Rtr = render_template("G_nilai.html", dataProdi=df_prodi, dataGuru=dtGuru)
				if where == "jadwal":
					sql = "SELECT * FROM jadwal NATURAL JOIN mapel_guru NATURAL JOIN guru NATURAL JOIN kelas NATURAL JOIN mapel WHERE kode_guru=%s"
					df_jadwal = db.getData(sql, [str(session["kode"])], df=True)
					Rtr = render_template(
						"G_jadwal.html", dataJadwal=df_jadwal, dataGuru=dtGuru)
		
		""" ROUTING SISWA """
		if lvl == "3":
			if path == "siswa":
				sql = "SELECT * FROM siswa  NATURAL JOIN userprofile  NATURAL JOIN kelas_siswa  NATURAL JOIN kelas  NATURAL JOIN prodi  WHERE nis=%s"
				df_siswa = db.getData(sql, stmt=[str(session["nis"])], df=True)
				nmsiswa = df_siswa["nama"].iloc[0]
				nis = df_siswa["nis"].iloc[0]
				kls = df_siswa["kelas"].iloc[0]
				kdprd = df_siswa["kode_prodi"].iloc[0]
				ket = df_siswa["ket"].iloc[0]
				nmprodi = df_siswa["nama_prodi"].iloc[0]
				dtsiswa = {
					"nama": nmsiswa,
					"nis": nis,
					"kelas": kls,
					"kdkls": f"{kls} {kdprd} {ket}",
					"kdprd": f"{kls} {nmprodi} {ket}"
				}
				if where == "jadwal":
					sql = "SELECT * FROM kelas_siswa NATURAL JOIN jadwal NATURAL JOIN mapel_guru NATURAL JOIN guru NATURAL JOIN kelas NATURAL JOIN mapel WHERE nis=%s"
					df_jadwal = db.getData(sql, [str(session["nis"])], df=True)
					Rtr = render_template(
						"S_jadwal.html", dataJadwal=df_jadwal, dataSiswa=dtsiswa)
				if where == "nilai":
					sql = "SELECT * FROM kelas_siswa NATURAL JOIN nilai NATURAL JOIN mapel_guru NATURAL JOIN guru NATURAL JOIN kelas NATURAL JOIN mapel WHERE nis=%s"
					df_nilai = db.getData(sql, [str(session["nis"])], df=True)
					Rtr = render_template("S_nilai.html", dataNilai=df_nilai, dataSiswa=dtsiswa)
				if where == "kelas":
					sql = "SELECT kode_kelas FROM kelas_siswa WHERE nis=%s"
					df_kdkls = db.getData(sql, [str(session["nis"])], df=True)
					if len(df_kdkls.index) == 0:
						return render_template("S_kelas.html", dataKelas="kosong", sts="kosong")
					sql = "SELECT * FROM kelas_siswa NATURAL JOIN siswa NATURAL JOIN kelas NATURAL JOIN prodi WHERE kode_kelas=%s"
					df_kelas = db.getData(sql, [str(df_kdkls["kode_kelas"].iloc[0])], df=True)
					Rtr = render_template("S_kelas.html", dataKelas=df_kelas,
										sts="ada", dataSiswa=dtsiswa)
	except KeyError as ke:
		print("BELUM LOGIN Boyy!")
		return redirect("/smkindonesia")
	except Exception as ex:
		import traceback
		tb = traceback.format_exc()
		print(tb)
		print("<--- Something Error --->")
		print(ex)
		return redirect("/smkindonesia")

	return Rtr

@app.route('/smkindonesia/<string:path>/<string:where>/<string:which>', methods=["GET","POST"])
def prosesSesuatu(path, where, which):
	Rtr = "Upsss... Mau Kemana BoyyyKETIGA..."

	if request.method == "GET":
		if path == "guru":
			if where == "nilai":
				if which == "ambilData":
					kode = request.args["kode"].split("-")
					sql = "SELECT * FROM nilai NATURAL JOIN mapel_guru NATURAL JOIN siswa NATURAL JOIN kelas_siswa NATURAL JOIN kelas NATURAL JOIN prodi WHERE kode_kelas=%s AND id_mg=%s AND kode_guru=%s"
					isi = [str(kode[0]), str(kode[1]), str(session["kode"])]
					dtJSN = db.getData(sql, isi)
					return dtJSN
				if which == "getDataEditNilai":
					kode = request.args["kode"]
					sql = "SELECT * FROM nilai NATURAL JOIN mapel_guru NATURAL JOIN siswa NATURAL JOIN kelas_siswa NATURAL JOIN kelas NATURAL JOIN prodi WHERE id_nilai=%s"
					isi = [str(kode)]
					dtJSN = db.getData(sql, isi)
					return dtJSN
				if which == "ambilDataKelas":
					kode = request.args["kode"]
					sql = "SELECT * FROM jadwal NATURAL JOIN kelas WHERE id_mg=%s"
					isi = [str(kode)]
					dtJSN = db.getData(sql, isi)
					return dtJSN
				if which == "ambilDataSiswa":
					kode = request.args["kode"]
					sql = "SELECT * FROM kelas_siswa NATURAL JOIN siswa WHERE kode_kelas=%s"
					isi = [str(kode)]
					dtJSN = db.getData(sql, isi)
					return dtJSN
		if path == "admin":
			# __GURU (ADMIN)__ #
			if where == "guru":
				if which == "ambilData":
					try:
						Rtr = db.getData("SELECT * FROM guru NATURAL JOIN userprofile")
					except Exception as e:
						print(e)
				if which == "ambilDataEdit":
					kode = request.args["kode"]
					sql = "SELECT * FROM guru NATURAL JOIN userprofile WHERE kode_guru=%s"
					isi = [str(kode)]
					try:
						Rtr = db.getData(sql, isi)
					except Exception as e:
						print(e)
			# __SISWA (ADMIN)__ #
			if where == "siswa":
				if which == "ambilData":
					try:
						sql = "SELECT * FROM siswa NATURAL JOIN userprofile"
						Rtr = db.getData(sql)
					except Exception as e:
						print(e)
				if which == "ambilDataEdit":
					nis = request.args["nis"]
					sql = "SELECT * FROM siswa NATURAL JOIN userprofile WHERE nis=%s"
					isi = [str(nis)]
					try:
						Rtr = db.getData(sql, isi)
					except Exception as e:
						print(e)
			# __MAPEL (ADMIN)__ #
			if where == "mapel":
				if which == "ambilData":
					try:
						Rtr = db.getData("SELECT * FROM mapel")
					except Exception as e:
						print(e)
				if which == "ambilDataEdit":
					kode = request.args["kode"]
					sql = "SELECT * FROM mapel WHERE kode_mapel=%s"
					isi = [str(kode)]
					try:
						Rtr = db.getData(sql, isi)
					except Exception as e:
						print(e)
			# __PRODI (ADMIN)__ #
			if where == "prodi":
				if which == "ambilData":
					try:
						Rtr = db.getData("SELECT * FROM prodi")
					except Exception as e:
						print(e)
				if which == "ambilDataEdit":
					kode = request.args["kode"]
					sql = "SELECT * FROM prodi WHERE kode_prodi=%s"
					isi = [str(kode)]
					try:
						Rtr = db.getData(sql, isi)
					except Exception as e:
						print(e)
			# __KELAS (ADMIN)__ #
			if where == "kelas":
				if which == "ambilData":
					try:
						Rtr = db.getData("SELECT a.kode_kelas,a.kode_prodi,a.kelas,a.ket,b.nama_prodi FROM `kelas` a INNER JOIN prodi b ON a.kode_prodi=b.kode_prodi")
					except Exception as e:
						print(e)
				if which == "ambilDataEdit":
					kode = request.args["kode"]
					sql = "SELECT a.kode_kelas,a.kode_prodi,a.kelas,a.ket,b.nama_prodi FROM `kelas` a INNER JOIN prodi b ON a.kode_prodi=b.kode_prodi WHERE a.kode_kelas=%s"
					isi = [str(kode)]
					try:
						Rtr = db.getData(sql, isi)
					except Exception as e:
						print(e)
			# __MAPELGURU (ADMIN)__ #
			if where == "mapelGuru":
				if which == "ambilData":
					try:
						Rtr = db.getData("SELECT * FROM mapel_guru NATURAL JOIN mapel NATURAL JOIN guru")
					except Exception as e:
						print(e)
				if which == "ambilDataEdit":
					kode = request.args["kode"]
					sql = "SELECT * FROM mapel_guru NATURAL JOIN mapel NATURAL JOIN guru WHERE id_mg=%s"
					isi = [str(kode)]
					try:
						Rtr = db.getData(sql, isi)
					except Exception as e:
						print(e)
			# __KELASSISWA (ADMIN)__ #
			if where == "kelasSiswa":
				if which == "ambilData":
					kode = request.args["kode"]
					sql = "SELECT * FROM kelas_siswa NATURAL JOIN siswa WHERE kode_kelas=%s"
					isi = [str(kode)]
					try:
						Rtr = db.getData(sql, isi)
					except Exception as e:
						print(e)
				if which == "ambilDataSiswa":
					try:
						Rtr = db.getData("SELECT * FROM siswa WHERE nis NOT IN (SELECT nis FROM kelas_siswa)")
					except Exception as e:
						print(e)
			# __JADWAL (ADMIN)__ #
			if where == "jadwal":
				if which == "ambilData":
					try:
						sql = "SELECT * FROM jadwal NATURAL JOIN mapel_guru NATURAL JOIN guru NATURAL JOIN mapel NATURAL JOIN kelas NATURAL JOIN prodi WHERE kode_kelas=%s"
						isi = [str(request.args["kode"])]
						Rtr = db.getData(sql,isi)
					except Exception as e:
						print(e)
				if which == "ambilDataMG":
					try:
						Rtr = db.getData("SELECT * FROM mapel_guru NATURAL JOIN guru NATURAL JOIN mapel")
					except Exception as e:
						print(e)
				
	if request.method == "POST":
		if path == "guru":
			if where == "nilai":
				if which == "prosesTambahNilai":
					dt = request.form
					mapel = dt["mapel"]
					nis = dt["nis"]
					uh = dt["uh"]
					uts = dt["uts"]
					uas = dt["uas"]
					na = dt["na"]
					sql = "INSERT INTO nilai(id_mg, nis, uh, uts, uas, na) VALUES(%s,%s,%s,%s,%s,%s)"
					isi = (str(mapel),str(nis),str(uh),str(uts),str(uas),str(na))
					db.execSql(sql, isi)
					return "Berhasil"
				if which == "prosesEditNilai":
					dt = request.form
					kode = dt["kode"]
					nis = dt["nis"]
					uh = dt["uh"]
					uts = dt["uts"]
					uas = dt["uas"]
					na = dt["na"]
					sql = "UPDATE nilai SET nis=%s, uh=%s, uts=%s, uas=%s, na=%s WHERE id_nilai=%s"
					isi = (str(nis), str(uh), str(uts), str(uas), str(na), str(kode))
					db.execSql(sql, isi)
					return "Berhasil"
				if which == "prosesDeleteNilai":
					kode = request.form["kode"]
					sql = "DELETE FROM nilai WHERE id_nilai=%s"
					isi = (str(kode))
					db.execSql(sql, isi)
		if path == "admin":
			# __GURU (ADMIN)__ #
			if where == "guru":
				if which == "prosesCekUseridGanda":
					dt = request.form
					username = dt["username"]
					sql = "SELECT userid FROM userprofile WHERE userid=%s"
					isi = [username]
					try:
						df_usr = db.getData(sql, isi, df=True)
						print(df_usr, len(df_usr.index))
						Rtr = "ada" if not len(df_usr.index) == 0 else "kosong"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesTambah":
					dt = request.form
					username = dt["username"]
					password = dt["password"]
					nama = dt["nama"]
					alamat = dt["alamat"]
					sql = "INSERT INTO guru(nama,alamat) VALUES(%s,%s)"
					isi = (str(nama), str(alamat))
					try:
						db.execSql(sql, isi)
						sql = "SELECT kode_guru FROM guru ORDER BY kode_guru DESC LIMIT 1"
						df_guru = db.getData(sql, df=True)
						sql = "INSERT INTO userprofile(userid, password, level, kode_guru) VALUES(%s,%s,%s,%s)"
						isi = (str(username),str(password),str(2),str(df_guru["kode_guru"].iloc[0]))
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesEdit":
					dt = request.form
					kode = dt["kode"]
					username = dt["username"]
					password = dt["password"]
					nama = dt["nama"]
					alamat = dt["alamat"]
					sql = "UPDATE guru SET nama=%s, alamat=%s WHERE kode_guru=%s"
					isi = (str(nama),str(alamat),str(kode))
					try:
						db.execSql(sql, isi)
						sql = "UPDATE userprofile SET userid=%s, password=%s WHERE kode_guru=%s"
						isi = (str(username),str(password),str(kode))
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesDelete":
					dt = request.form
					kode = dt["kode"]
					sql = "DELETE FROM guru WHERE kode_guru=%s"
					try:
						db.execSql(sql, str(kode))
						sql = "DELETE FROM userprofile WHERE kode_guru=%s"
						db.execSql(sql, str(kode))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
			# __SISWA (ADMIN)__ #
			if where == "siswa":
				if which == "prosesCekNisGanda":
					dt = request.form
					nis = dt["nis"]
					sql = "SELECT * FROM siswa WHERE nis=%s"
					isi = [str(nis)]
					try:
						data = db.getData(sql, isi, True)
						Rtr = "ada" if not len(data.index) == 0 else "kosong"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesTambah":
					dt = request.form
					username = dt["username"]
					password = dt["password"]
					nis = dt["nis"]
					nama = dt["nama"]
					jk = dt["jk"]
					alamat = dt["alamat"]
					sql = "INSERT INTO siswa(nis,nama,jk,alamat) VALUES(%s,%s,%s,%s)"
					isi = (str(nis), str(nama), str(jk), str(alamat))
					try:
						db.execSql(sql, isi)
						sql = "INSERT INTO userprofile(userid, password, level, nis) VALUES(%s, %s, %s, %s)"
						isi = (str(username),str(password),str(3),str(nis))
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesEdit":
					dt = request.form
					kode = dt["kode"]
					username = dt["username"]
					password = dt["password"]
					nis = dt["nis"]
					nama = dt["nama"]
					jk = dt["jk"]
					alamat = dt["alamat"]
					sql = "UPDATE siswa SET  nis=%s, nama=%s, jk=%s, alamat=%s WHERE nis=%s"
					isi = (str(nis),str(nama),str(jk),str(alamat),str(kode))
					print(sql, isi)
					try:
						db.execSql(sql, isi)
						sql = "UPDATE userprofile SET userid=%s, password=%s, nis=%s WHERE nis=%s"
						isi = (str(username), str(password), str(nis), str(kode))
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesDelete":
					dt = request.form
					nis = dt["nis"]
					sql = "DELETE FROM siswa WHERE nis=%s"
					try:
						db.execSql(sql, str(nis))
						sql = "DELETE FROM userprofile WHERE nis=%s"
						db.execSql(sql, (str(nis)))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
			# __MAPEL (ADMIN)__ #
			if where == "mapel":
				if which == "prosesCekKodeGanda":
					dt = request.form
					kode = dt["kode"]
					sql = "SELECT * FROM mapel WHERE kode_mapel=%s"
					isi = [str(kode)]
					try:
						data = db.getData(sql, isi, True)
						Rtr = "ada" if not len(data.index) == 0 else "kosong"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesTambah":
					dt = request.form
					kode = dt["kode"]
					nama = dt["nama"]
					sql = "INSERT INTO mapel(kode_mapel,nama_mapel) VALUES(%s,%s)"
					isi = (str(kode), str(nama))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesEdit":
					dt = request.form
					kodeAsli = dt["kodeAsli"]
					kode = dt["kode"]
					nama = dt["nama"]
					sql = "UPDATE mapel SET  kode_mapel=%s, nama_mapel=%s WHERE kode_mapel=%s"
					isi = (str(kode),str(nama),str(kodeAsli))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesDelete":
					dt = request.form
					kode = dt["kode"]
					sql = "DELETE FROM mapel WHERE kode_mapel=%s"
					try:
						db.execSql(sql, str(kode))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
			# __PRODI (ADMIN)__ #
			if where == "prodi":
				if which == "prosesCekKodeGanda":
					dt = request.form
					kode = dt["kode"]
					sql = "SELECT * FROM prodi WHERE kode_prodi=%s"
					isi = [str(kode)]
					try:
						data = db.getData(sql, isi, True)
						Rtr = "ada" if not len(data.index) == 0 else "kosong"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesTambah":
					dt = request.form
					kode = dt["kode"]
					nama = dt["nama"]
					sql = "INSERT INTO prodi(kode_prodi,nama_prodi) VALUES(%s,%s)"
					isi = (str(kode), str(nama))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesEdit":
					dt = request.form
					kodeAsli = dt["kodeAsli"]
					kode = dt["kode"]
					nama = dt["nama"]
					sql = "UPDATE prodi SET  kode_prodi=%s, nama_prodi=%s WHERE kode_prodi=%s"
					isi = (str(kode),str(nama),str(kodeAsli))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesDelete":
					dt = request.form
					kode = dt["kode"]
					sql = "DELETE FROM prodi WHERE kode_prodi=%s"
					try:
						db.execSql(sql, str(kode))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
			# __KELAS (ADMIN)__ #
			if where == "kelas":
				if which == "prosesCekKodeGanda":
					dt = request.form["kode"].split(",")
					#print(dt)
					kode = dt[0]
					kelas = dt[1]
					ket = dt[2]
					sql = "SELECT * FROM kelas WHERE kode_prodi=%s AND kelas=%s AND ket=%s"
					isi = [str(kode),str(kelas),str(ket)]
					try:
						data = db.getData(sql, isi, True)
						Rtr = "ada" if not len(data.index) == 0 else "kosong"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesTambah":
					dt = request.form
					kode = dt["kode"]
					kelas = dt["kelas"]
					ket = dt["ket"]
					sql = "INSERT INTO kelas(kode_prodi,kelas,ket) VALUES(%s,%s,%s)"
					isi = (str(kode), str(kelas), str(ket))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesEdit":
					dt = request.form
					kodeAsli = dt["kodeAsli"]
					kode = dt["kode"]
					kelas = dt["kelas"]
					ket = dt["ket"]
					sql = "UPDATE kelas SET  kode_prodi=%s, kelas=%s,ket=%s WHERE kode_kelas=%s"
					isi = (str(kode),str(kelas),str(ket),str(kodeAsli))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesDelete":
					dt = request.form
					kode = dt["kode"]
					sql = "DELETE FROM kelas WHERE kode_kelas=%s"
					try:
						db.execSql(sql, str(kode))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
			# __MAPELGURU (ADMIN)__ #
			if where == "mapelGuru":
				if which == "prosesCekKodeGanda":
					dt = request.form["kode"].split(",")
					print(dt)
					kodeM = dt[0]
					kodeG = dt[1]
					sql = "SELECT * FROM mapel_guru WHERE kode_mapel=%s AND kode_guru=%s"
					isi = [str(kodeM),str(kodeG)]
					try:
						data = db.getData(sql, isi, True)
						Rtr = "ada" if not len(data.index) == 0 else "kosong"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesTambah":
					dt = request.form
					kodeM = dt["kodeM"]
					kodeG = dt["kodeG"]
					sql = "INSERT INTO mapel_guru(kode_mapel, kode_guru) VALUES(%s,%s)"
					isi = (str(kodeM),str(kodeG))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesEdit":
					dt = request.form
					kodeAsli = dt["kodeAsli"]
					kodeM = dt["kodeM"]
					kodeG = dt["kodeG"]
					sql = "UPDATE mapel_guru SET  kode_mapel=%s, kode_guru=%s WHERE id_mg=%s"
					isi = (str(kodeM),str(kodeG),str(kodeAsli))
					try:
						db.execSql(sql, isi)
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "prosesDelete":
					dt = request.form
					kode = dt["kode"]
					sql = "DELETE FROM mapel_guru WHERE id_mg=%s"
					try:
						db.execSql(sql, str(kode))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
			# __MAPELGURU (ADMIN)__ #
			if where == "kelasSiswa":
				if which == "pindahSiswa":
					dt = request.form
					nis = dt["nis"]
					kelas = dt["kelas"]
					sql = "INSERT INTO kelas_siswa(nis, kode_kelas) VALUES(%s, %s)"
					try:
						db.execSql(sql, (str(nis), str(kelas)))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "pindahKelasSiswa":
					dt = request.form
					kode = dt["kode"]
					sql = "DELETE FROM kelas_siswa WHERE id_ks=%s"
					try:
						db.execSql(sql, str(kode))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
			# __JADWAL (ADMIN)__ #
			if where == "jadwal":
				if which == "pindahMapelGuru":
					dt = request.form
					kdmg = dt["kdmg"]
					kelas = dt["kelas"]
					sql = "INSERT INTO jadwal(id_mg, kode_kelas) VALUES(%s, %s)"
					try:
						db.execSql(sql, (str(kdmg), str(kelas)))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
				if which == "pindahJadwal":
					dt = request.form
					kode = dt["kode"]
					sql = "DELETE FROM jadwal WHERE id_jdwl=%s"
					try:
						db.execSql(sql, str(kode))
						Rtr = "Berhasil"
					except Exception as e:
						print(e)
						Rtr = "Upsss"
	return Rtr


@app.route('/smkindonesia/<string:path>', methods=["POST"])
def prosesLogin(path):
	Rtr = "Upsss... Mau Kemana BoyyyKEEMPAT..."
	if path == "login":
		usr = request.form["username"]
		pwd = request.form["password"]
		sql = "SELECT * FROM userprofile WHERE userid=%s AND password=%s"
		param = [str(usr),str(pwd)]
		try:
			df_usr = db.getData(sql, param, True)
			if len(df_usr.index) == 1:
				lvl = df_usr["level"].iloc[0]
				if lvl == 1:
					session["level"] = "1"
					session["userid"] = usr
					Rtr = redirect("admin")
				elif lvl == 2:
					session["level"] = "2"
					session["userid"] = usr
					session["kode"] = str(df_usr["kode_guru"].iloc[0])
					Rtr = redirect("guru")
				elif lvl == 3:
					session["level"] = "3"
					session["userid"] = usr
					session["nis"] = str(df_usr["nis"].iloc[0])
					Rtr = redirect("siswa")
				else:
					session.clear()
					Rtr = redirect("/")
					flash(usr)
			else:
				session.clear()
				Rtr = redirect("/")
				flash(usr)
		except Exception as e:
			print(e)
	return Rtr


#===>  SERVER START <===#
if __name__=='__main__':
	startServer()
