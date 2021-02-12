import pygame as pg 
import random,sys,time

def EXIT(window,file, score):
    file.save_scores(score)
    E_font = pg.font.SysFont("comicsansms", 72)
    window.fill((0,0,0))#Tlo jest czarne
    window.blit(E_font.render("The End", True, (255,0,0)),(40,100))
    window.blit(E_font.render("Push ESC", True, (255,0,0)),(40,200))
    pg.display.flip()#Zamiana buforow
    flag =1

    while flag:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key ==pg.K_ESCAPE:
                flag=0
                print("klik")
    time.sleep(0.100)
    sys.exit(0)#Koniec aplikacji

class Scores:
    def __init__(self):
        try:
            self.file = open("top5.txt", "r")#Otwieram plik z danymi
            self.tmp = self.file.readlines()#Zapis pliku do tmp
            self.txt = [int(x) for x in (self.tmp)]#Konwersja lini pliku do tablicy int
        #Jezeli plik nie istnieje to stworz tablice z piecioma 0, do tablicy wynikow, w zapisie i tak zostanie
        #stwrzony nowy pusty plik(malo efektywne)
        except:
            #self.file = open("top5.txt", "w+")#Otwieram plik z danymi
            #[self.file.write("{}\n".format(x*0)) for x in range(5)]
            self.txt = [int(x*0) for x in range(5)]
    #Zapis punktow do pliku
    def save_scores(self,x):
        #Sprawdzenie czy punkty weza sa wieksze niz te w pliku
        tmp=0
        #Sprawdzanie czy ktorys ze elementow jest mniejszy od wyniku, jesl tak to zamien go z wynikiem weza
        for y in range(len(self.txt)):
            if self.txt[y] <x:
                tmp =self.txt[y]
                self.txt[y]=x
                x=tmp
        try:
            self.file = open("top5.txt", "w+")#Wymazanie zawartosci pliku
            #Zapis zawartosci tablicy do pliku z nowej lini kazda wartosc
            for val in self.txt:
                self.file.write(str("{}\n".format(val)))
            self.file.close()
        except:
            print("Zmiena prawa dotepu do pliku")
class Color():
    def __init__(self):
        self.white = ((255,255,255))
        self.blue = ((0,0,255))
        self.green = ((0,255,0))
        self.red = ((255,0,0))
        self.black = ((0,0,0))
        self.orange = ((255,100,10))
        self.yellow = ((255,255,0))
        self.blue_green = ((0,255,170))
        self.marroon = ((115,0,0))
        self.lime = ((180,255,100))
        self.pink = ((255,100,180))
        self.purple = ((240,0,255))
        self.gray = ((127,127,127))
        self.magenta = ((255,0,230))
        self.brown = ((100,40,0))
        self.forest_green = ((0,50,0))
        self.navy_blue = ((0,0,100))
        self.rust = ((210,150,75))
        self.dandilion_yellow = ((255,200,0))
        self.highlighter = ((255,255,100))
        self.sky_blue = ((0,255,255))
        self.light_gray = ((200,200,200))
        self.dark_gray = ((50,50,50))
        self.tan = ((230,220,170))
        self.coffee_brown =((200,190,140))
        self.moon_glow = ((235,245,255))
        self.color ={0:self.marroon,1:self.white,2:self.red,3:self.coffee_brown,4:self.red,5:self.rust,6:self.green,7:self.yellow,
        8:self.pink,9:self.orange,10:self.tan}
#Klasa przechowująca id eventow dla timerow
class Event():
    def __init__(self):
         self.event_id=0#Inicjalizacja ID

    def get_id(self):#Metoda zwraca ID powiekszone o jeden, uzytkownik dostaje unikalny numer, numeracja zaczyna sie 1
        self.event_id+=1
        return self.event_id
#Klasa przechowuje figury, oraz linie ktore ograniczaja obszar gry
class Figures():
    def __init__(self,event,size):
        self.scores=0#Zmienna przechowuje liczbe punktów
        self.figures = []#Lista przechowujaca wszystkie figury w grzse
        self.ID_down=event.get_id()#Przypisanie unikalnego numeru do eventu odpowidzalnego od opuszczania w dol figur
        self.ID_move = event.get_id()#Przypisanie unikalnego numeru do eventu odpowidzalnego od poruszania w boki spadajacej figury
        self.line_down =  pg.Rect(0,size[1],size[0],1)#Linia dolna ogranicza obszar gry od dolu
        self.line_left = pg.Rect(-1,0,1,size[1])#Linia lewa,ma grubosc 1 wysokosc size[1] oraz poloozenie x=-1 oraz y=0
        self.line_rigth = pg.Rect(size[0],0,1,size[1])#Linia prawa
        self.figur={0:Line,1:Squar,2:Lblock,3:Tblock,4:Zblock}#Slownik z nazwami klas, jest to potrzebne do generowania 
        self.next = random.randint(0,4)
        #figury w metodzie add
        self.offset=0#Offset potrzebny do przsuwania figury spadajacej ktora znajduje sie za prawa sciana line_rigth
    def add(self):#Dodawanie nowwej spadajacej figury
        self.figures.append(self.figur[self.next]())#Dodanie do listy nowej fiugury
        self.plot()#Metoda sprawdza czy jakis posiom zostal w pelnio zapelniony
        self.next = random.randint(0,4)#Losowanie wartosci od <0;4>, dla liczb sa przypisane Klasy

    def draw(self,window):#Metoda odpowiedzialna za rysowanie wszysatkich figur znajdujacych sie w liscie figures[]
        pg.draw.rect(window,(0,255,0),self.line_down)#Rysowanie dolnej lini
        pg.draw.rect(window,(0,255,0),self.line_left)#Lewa
        pg.draw.rect(window,(0,255,0),self.line_rigth)#Prawa
        for obj in self.figures:#Obj to osobna figura z listy
            obj.draw(window)#Wywolanie metody draw z obiektu obj
        # for obj in self.figures[:-1]:#Obj to osobna figura z listy oprocz ostatniej
        #     for block in obj.body:#Block to osobny protokat z figury
        #         if block.y <0:#Jesli Jakas figura jest wyzej niz okno to koniec gry, bo figury wystaja po okno
        #             return True
        # return False
    def break_top(self):
        for obj in self.figures[:-1]:#Obj to osobna figura z listy oprocz ostatniej
            for block in obj.body:#Block to osobny protokat z figury
                if block.y <0:#Jesli Jakas figura jest wyzej niz okno to koniec gry, bo figury wystaja po okno
                    return True
        return False
    def rote(self):#Metoda odpowiedzialna za obrocenie figury
        last_figure = self.figures[-1].copy()#Zapamietanie ostatniej figury
        self.figures[-1].rote(0)#Obrocenie spadajacej figru
        if self.colistion():#Jesli po obroceniu figura zderzyla sie z kims to cofniecie rotacji
            self.figures[-1].body = last_figure.copy()#Ostatni obiekt z powrotem ma wartosc przed zmiana
        self.offset=self.get_offset()#offset rowna sie wartosci z metody get_offseta
        for obj in self.figures[-1].body:#Obj kazdy blok z ostatniej spadajacej figury
            obj.x-=self.offset#Zmiana parametru x bloku
    def down(self):#Metoda odpowiedzialna za spadanie bloku
        last_cp = self.figures[-1].copy()#Skopiowanie ostatniej figury
        self.figures[-1].down()#Wywolanie metody down na ostatnim figurze
        if (self.line_down.collidelist(self.figures[-1].body) != -1):#Sprawdzanie czy dolna linia nie zderza sie z cialem ostatniej figury
            self.figures[-1].body=last_cp#Kopiowanie ciala ostanitje figury
            self.add()#Dodanie nowej figury
        elif self.colistion():#Wywolanie metody colistion
            self.figures[-1].body=last_cp
            self.add()#Dodanie nowej figury

    def get_offset(self):#Obliczenie offsetu
        max=0
        tmp=0
        for  obj in self.figures[-1].body:
            if obj.x >= self.line_rigth.x:
                tmp = obj.x-self.line_rigth.x+self.figures[-1].size#Obliczenie o ile elementy figury wystaja poza prawa krawedz okna
                if tmp>max:
                    max=tmp
                    print(max)
        return max#Zwrocenie max wartosci,o tyle zostanie przesunieta figura jesli wystaje po prawa krawedz okna
        
    def colistion(self):#Metoda sprawdza czy jakis blok nie wchodzi w inna figure,jesli tak to zwrot True,
        for obj in self.figures[:-1]:#Figur z tablicy od pierwszego do przed ostatniego
            for block in obj.body:
                if block.collidelist(self.figures[-1].body) != -1:#Jesli Blok z poprzedniej lini zawiera sie w ostatniej figurze to zwroc true
                    return True
        return False#Zwroc false jesli zaden blok nie zachodzi w inna figure
    def move(self,key):#Metoda odpowiedzialna za roszanie
        #self.figures[-1].move(key) 
        last_cp = self.figures[-1].copy()#Kopiowanie ostatniego elementu
        self.figures[-1].move(key)#Wywolanie metody move z obiektu figures[-1]
        if (self.line_down.collidelist(self.figures[-1].body) != -1):#Sprawdzenie czy ostatnia figura nie zachodzi na dolna linie
            self.figures[-1].body=last_cp
        elif (self.line_left.collidelist(self.figures[-1].body) != -1):#Sprawdzenie czy figura nie wystaje poza lewa krawedz
            self.figures[-1].body=last_cp
        elif (self.line_rigth.collidelist(self.figures[-1].body) != -1):#Sprawdzenie czy figura nie wystaje poza prawa krawedz
            self.figures[-1].body=last_cp
        elif self.colistion():#Sprawdzenie czy bloki nie zawieraja sie w innej figurze
            self.figures[-1].body=last_cp

    def plot(self):#Metoda odpowiedzialna za sprawdzanie czy jakis poziom nie zostal zapelniony
        x = self.figures[-1].size#x wartosc rozmiaru bloku
        list_line = []#Lista zawierajaca linie do przekreslenia
        score=0
        for i in range(20):#Sprawdzanie 2 wierzy
            rect = pg.Rect(0,i*x+20,400,1)#Tworzenie lini ktora pomaga przy sprawdzaniu czy poziom zapelniony
            list_line.append(rect)#Dodanie do listy odpowiedzialnej za przekreslanie
        cnt =0#Licznik zliczajacy ile blokow w figurze styka sie linia, jesli 10 to znaczy sie nalezy usunac bloki bo wierz zapelniony
        for rect in list_line:#kazdy obiekt w liscie list
            for obj in self.figures:#Kazda figura w liscie figures
                for block in obj.body:#Kazdy blok z obj
                    if rect.colliderect(block):#Sprawdzenie czy blok styka sie z linia
                        cnt+=1#Jesli sie styka do zwiekszenie licznika o jeden
            list_remove =[]#Inicjalizacja listy remove, przechowujaca elementy do usuniecia

            if cnt >=10:#Jesli licznik rowny lub wiekszy niz 10
                for obj in self.figures:
                    for block in obj.body:
                        if rect.colliderect(block):#Jesli blok styka sie linia dodanie go do listy remove
                            list_remove.append(block)
                    for d in list_remove:
                        if d in obj.body:
                            obj.body.remove(d)#Usuwanie obiektow zawierajacych sie liscie remove
            
            if cnt>=10:#Przesuniecie wszystkich blokow powyzej usuniecia w dol o rozmiar bloku
                for obj in self.figures:
                    for block in obj.body:
                        if block.y < rect.y:
                            block.move_ip(0,40)
                score+=1 
            cnt=0
        self.scores+= score**2

class Figure():
    def __init__(self,start = [0,0]):
        self.size = 40#Rozmiar bloku
        if start == [0,0]:
            self.start=[3*self.size,-self.size]#Miejsce startu figur
        else:
            self.start=start
        self.body = []#Puste cialo
        self.cnt_rote=0#Licznik przechowuje w jakiej pozycji znajduje sie figura
        self.color = Color().color[random.randint(0,10)]#Losowanie koloru figury
    def add(self,vec):#Dodawanie blokow
        self.body.append(pg.Rect(*vec,self.size,self.size))
    def draw(self,window):#Rysowanie blokow
        for obj in self.body:
            pg.draw.rect(window,self.color,obj)
    def down(self):#Opadanie w dol o rozmiar bloku
        for obj in self.body:
            obj.move_ip(0,self.size)
    def move(self,key):#Metoda odpowiezialna za porusznie figury
        if key[pg.K_a]:
            for obj in self.body:
                obj.move_ip(-self.size,0)
        elif key[pg.K_d]:
            for obj in self.body:
                obj.move_ip(self.size,0)
    
    def copy(self):
        tmp = []
        for x in self.body:
            tmp.append(x.copy())
        return tmp

class Line(Figure):#Figura linie
    def __init__(self,start=[0,0]):
        super().__init__(start)
        self.add((self.start[0],self.start[1]))
        self.add((self.start[0],self.start[1]+self.size))
        self.add((self.start[0],self.start[1]+2*self.size))
        self.add((self.start[0],self.start[1]+3*self.size))
    
    def rote(self,offset):#Metoda odpowiedzialna za rotacje
        if self.cnt_rote==0:
            for i in range(len(self.body)):
                self.body[i].move_ip(i*self.size-offset,-i*self.size)
        elif self.cnt_rote==1:
            for i in range(len(self.body)):
                self.body[i].move_ip(-i*self.size-offset,i*self.size)
        self.cnt_rote+=1
        if self.cnt_rote >=2:
            self.cnt_rote=0

class Squar(Figure):#Kwadrat
    def __init__(self,start=[0,0]):
        super().__init__(start)
        self.add((self.start[0],self.start[1]))
        self.add((self.start[0]+self.size,self.start[1]))
        self.add((self.start[0]+self.size,self.start[1]+self.size))
        self.add((self.start[0],self.start[1]+self.size))

    def rote(self,offset):
        pass

class Lblock(Figure):#eLka
    def __init__(self,start=[0,0]):
        super().__init__(start)
        for i in range(3):
            self.add((self.start[0],self.start[1]+i*self.size))
        self.add((self.start[0]+self.size,self.start[1]+self.size*2)) 
    def rote(self,offset):
        if self.cnt_rote ==0:
            self.body[0].move_ip(2*self.size,0)
            self.body[1].move_ip(1*self.size,-self.size)
            self.body[2].move_ip(0,-2*self.size)
            self.body[3].move_ip(-self.size,-self.size)
        elif self.cnt_rote==1:
            self.body[0].move_ip(-self.size,2*self.size)
            self.body[1].move_ip(0,self.size)
            self.body[2].move_ip(self.size,0)
            self.body[3].move_ip(0,-self.size)
        elif self.cnt_rote==2:
            self.body[0].move_ip(-self.size,-self.size)
            self.body[1].move_ip(0,0)
            self.body[2].move_ip(self.size,self.size)
            self.body[3].move_ip(2*self.size,0)
        elif self.cnt_rote ==3:
            self.body[0].move_ip(0,-self.size)
            self.body[1].move_ip(-self.size,0)
            self.body[2].move_ip(-2*self.size,self.size)
            self.body[3].move_ip(-self.size,2*self.size)
        self.cnt_rote+=1
        if self.cnt_rote>4:
            self.cnt_rote=0

class Tblock(Figure):#Figura T
    def __init__(self,start=[0,0]):
        super().__init__(start)
        for i in range(3):
            self.add((self.start[0]+i*self.size,self.start[1]))
        self.add((self.start[0]+self.size,self.start[1]+self.size)) 
    def rote(self,offset):
        if self.cnt_rote ==0:
            self.body[0].move_ip(self.size,0)
            self.body[1].move_ip(0,self.size)
            self.body[2].move_ip(-self.size,2*self.size)
            self.body[3].move_ip(-self.size,0)
        elif self.cnt_rote ==1:
            self.body[0].move_ip(self.size,self.size)
            self.body[1].move_ip(0,0)
            self.body[2].move_ip(-self.size,-self.size)
            self.body[3].move_ip(self.size,-self.size)
        elif self.cnt_rote ==2:
            self.body[0].move_ip(-self.size,self.size)
            self.body[1].move_ip(0,0)
            self.body[2].move_ip(self.size,-self.size)
            self.body[3].move_ip(self.size,self.size)
        elif self.cnt_rote ==3:
            self.body[0].move_ip(-self.size,-2*self.size)
            self.body[1].move_ip(0,-self.size)
            self.body[2].move_ip(self.size,0)
            self.body[3].move_ip(-self.size,0)

        self.cnt_rote+=1
        if self.cnt_rote>4:
            self.cnt_rote=0

class Zblock(Figure):#Figura Z
    def __init__(self,start=[0,0]):
        super().__init__(start)
        self.add((self.start[0],self.start[1])) 
        self.add((self.start[0]+self.size,self.start[1])) 
        self.add((self.start[0]+self.size,self.start[1]+self.size)) 
        self.add((self.start[0]+2*self.size,self.start[1]+self.size)) 
    def rote(self,offset):
        if self.cnt_rote ==0:
            self.body[0].move_ip(self.size,0)
            self.body[1].move_ip(0,self.size)
            self.body[2].move_ip(-self.size,0)
            self.body[3].move_ip(-2*self.size,self.size)
        elif self.cnt_rote ==1:
            self.body[0].move_ip(-self.size,0)
            self.body[1].move_ip(0,-self.size)
            self.body[2].move_ip(+self.size,0)
            self.body[3].move_ip(2*self.size,-self.size)
        self.cnt_rote+=1
        if self.cnt_rote>1 :
            self.cnt_rote=0

class Grid():#Klasa odpowidzialna za rysowanie siatek w oknie
    def __init__(self,size):
        self.size = size
    
    def draw(self,window):
        x = self.size[0]/10
        y = self.size[1]/20
        #Rysowanie pionowe
        for i in range(10):
            rect = pg.Rect(x*i,0,1,self.size[1])
            pg.draw.rect(window,(0,0,255),rect)
        for i in range(20):
            rect = pg.Rect(0,x*i,self.size[0],1)
            pg.draw.rect(window,(0,0,255),rect)

class Menu():
    def __init__(self,size,lista):
        self.size = size
        self.time=0
        self.clock = pg.time.Clock()
        self.top5=lista
        self.last_figur=0

    def draw(self,window,score,figur):
        self.clock.tick()
        self.time+=self.clock.get_rawtime()
        #self.time=round(self.time/10,4)
        #self.second= time.localtime().tm_sec
        E_font = pg.font.SysFont("comicsansms", 26)
        window.blit(E_font.render("Scores {}".format(score), True, Color().red),(self.size[0]+20,40))
        window.blit(E_font.render("{}".format("Time "), True, Color().green),(self.size[0]+20,100))
        window.blit(E_font.render("{}".format(time.ctime(time.time()))[10:20], True, Color().green),(self.size[0]+10,140))
        window.blit(E_font.render("{}".format("Time of game"), True, Color().green),(self.size[0]+20,180))
        window.blit(E_font.render("{}".format(round(self.time/1000,1)), True, Color().green),(self.size[0]+20,220))
        window.blit(E_font.render("{}".format("TOP5"), True, Color().white),(self.size[0]+20,260))
        for ind in range(len(self.top5)):
            window.blit(E_font.render("{}. {}".format(ind+1, self.top5[ind]), True, Color().white),(self.size[0]+20,300+40*ind))
        if self.last_figur != figur:
            self.tmp =figur([self.size[0]+60,600])
            #self.tmp.body.clear()
            #self.tmp.add((self.size[0]+20,500))
            self.tmp.color=Color().white
            print("test")
        window.blit(E_font.render("{}".format("Next figure"), True, Color().white),(self.size[0]+20,520))
        self.tmp.draw(window)
        self.last_figur = figur
class Game():
    def __init__(self):
        scr = Scores()
        event = Event()
        pg.font.init()
        pg.display.init()
        pg.mixer.init()
        window = pg.display.set_mode((600,800))
        size = (400,800)
        x = Figures(event,size)
        grid = Grid(size)
        menu = Menu(size,scr.txt)
        x.add()
        pg.time.set_timer(x.ID_down,150) 
        pg.time.set_timer(x.ID_move,5)
        pg.mixer.music.load('theme.mp3')
        flag_music=1
        #pg.mixer.music.play(-1)
        #line.body[3].rect.move_ip(0,10)
        while True:
            window.fill((0,0,0))
            x.draw(window)
            grid.draw(window)
            menu.draw(window,x.scores,x.figur[x.next])
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    EXIT(window,scr,x.scores)
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    EXIT(window,scr,x.scores)
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:  
                    x.rote()
                if event.type == x.ID_down:
                    x.down()
                if event.type == x.ID_down:
                    key = pg.key.get_pressed()
                    x.move(key)
                    if x.break_top():
                        EXIT(window,scr,x.scores)
                if event.type == pg.KEYDOWN and event.key == pg.K_m:
                    flag_music^=1
                    if flag_music:
                        pg.mixer.music.stop()
                    else:
                        print(flag_music)
                        pg.mixer.music.play(-1)

Game()