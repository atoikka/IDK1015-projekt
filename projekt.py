from tkinter import *

text_debug = False
delimiter = ";"

testpunktid_x = []; testpunktid_y = [];
ui_elemendid = []

# tühjenda_väli
# Eemaldab kõik failispetsiifilised elemendid
def tühjenda_väli():
    global ui_elemendid
    for element in ui_elemendid:
        w.delete(element)

def joonista():
    # Kõik punktid, mis on failist laetud, kohaldatagu vahemikku 0-350
    # Selleks leida kõigepealt mõlema telje max-min väärtused
    max_x = max(testpunktid_x); min_x = min(testpunktid_x)
    print("X-telje väärtused: MIN " + str(min_x) + ", MAX " + str(max_x))
    max_y = max(testpunktid_y); min_y = min(testpunktid_y)
    print("Y-telje väärtused: MIN " + str(min_y) + ", MAX " + str(max_y))

    # Skaleerime oma väärtusi järgneva vastuse abil:
    # http://stackoverflow.com/questions/5294955/how-to-scale-down-a-range-of-numbers-with-a-known-min-and-max-value
    punktid_x = []; punktid_y = [];
    for i in range(0, punktide_arv):
        x = testpunktid_x[i]
        punktid_x.append((((350 - 0)*(x - min_x))/(max_x - min_x))+0);
        y = testpunktid_y[i]
        punktid_y.append((((350 - 0)*(y - min_y))/(max_y - min_y))+0);

    # Kirjutada min ja max väärtused joonisele
    w.create_line(teljestiku_begin_x-5, teljestiku_begin_y, teljestiku_begin_x+2, teljestiku_begin_y)
    ui_elemendid.append(w.create_text(teljestiku_begin_x-15, teljestiku_begin_y, text=str(max_y)));
    ui_elemendid.append(w.create_text(teljestiku_begin_x-15, teljestiku_begin_y+350-5, text=str(min_y)));

    ui_elemendid.append(w.create_text(teljestiku_begin_x+350, teljestiku_begin_y+350+10, text=str(max_x)));
    ui_elemendid.append(w.create_text(teljestiku_begin_x+5, teljestiku_begin_y+350+10, text=str(min_x)));

    # Joonistada väikesed ovaalid
    for i in range(0, len(punktid_x)):
        #print(" PUNKT " + str(punktid_x[i]) + ":" + str(punktid_y[i]) + " (enne: " + str(testpunktid_x[i]) + ":" + str(testpunktid_y[i]) + ")")
        x = teljestiku_begin_x + punktid_x[i]
        y = (teljestiku_begin_y + 350) - punktid_y[i]
        ui_elemendid.append(w.create_oval(x - 2, y - 2, x + 2, y + 2))
        if text_debug:
            string = str(testpunktid_x[i]) + ":" + str(testpunktid_y[i]);
            ui_elemendid.append(w.create_text(x + 2, y + 2, text=string))

# vali_fail
# Annab kasutajale dialoogi faili valimiseks ning valimisel laeb 
def vali_fail():
    error = False
    fail_nimi = filedialog.askopenfilename();
    
    # Tühjendada vana punktide list
    tühjenda_väli()
    global testpunktid_x, testpunktid_y, punktide_arv
    testpunktid_x = []; testpunktid_y = [];
    # Avada fail ning tuvastada delimiter
    try:
        fail = open(fail_nimi, 'r')
    except (IOError, OSError) as e:
        error = "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        error = sys.exc_info()[0]
    
    rida = fail.readline().strip()
    if rida.find(";") != -1:
        delimiter = ";"
    elif rida.find(",") != -1:
        delimiter = ","
    else:
        error = "Tundmatu eraldaja (toetatud on koma ja koolon)!"

    if error == False:
        print("Delimiter is " + delimiter)
        # Leida telgede nimetused
        telje_nim = rida.split(delimiter)
        print(str(telje_nim))
        # Lugeda koordinaadid järgnevatelt ridadelt
        for rida in fail:
            coords = rida.strip().split(delimiter)
            if len(coords) == 2:
                # Lubada eestipärased ujukomaarvude täiskoha eraldajad
                coords[0].replace(",", ".")
                coords[1].replace(",", ".")
                    
                print(rida.strip() + " => " + coords[0] + " & " + coords[1])
                testpunktid_x.append(float(coords[0]))
                testpunktid_y.append(float(coords[1]))
            else:
                error = "Koordinaatide lugemine ebaõnnestus (ebakorrektne formaat)!"
                break;

    if error == False:
        punktide_arv = len(testpunktid_x)
        joonista()
    else:
        ui_elemendid.append(w.create_text(60, 150, text="Ilmnes viga!\n" + error, fill="red", anchor=NW))

# Alustada UI loomist
master = Tk()

w = Canvas(master, width = 600, height = 400)
w.pack();

# Teljed (350 pikslit mõlemas suunas)
teljestiku_begin_x = 50
teljestiku_begin_y = 30
telgede_ristumine_x = teljestiku_begin_x
telgede_ristumine_y = teljestiku_begin_y+350

w.create_line(teljestiku_begin_x, teljestiku_begin_y, teljestiku_begin_x, 380) #, arrow=FIRST
w.create_line(teljestiku_begin_x, 380, 400, 380) #, arrow=LAST
# Nupp faili valimiseks
btn_vali_fail = Button(master, text="Vali fail", command=vali_fail)
btn_vali_fail.place(x=teljestiku_begin_x+350+20, y=teljestiku_begin_y);

# Laadida punktid failist
vali_fail()

# Program loop
mainloop()
