% =================================================================
% FILE: prolog_kb.pl
% Knowledge Base Logika Orde Pertama (FOL) 
% TEMA: OPTIMASI ITINERARY KULINER VIRAL DI KOTA BANDUNG
% =================================================================

% --- DAFTAR PREDIKAT UTAMA (Untuk Referensi) ---
% lokasi_populer/1, mengunjungi/2, antrean_panjang/1, fisik_lelah/1, 
% pengalaman_buruk/1, jarak/3, memiliki_fasilitas/2, butuh_optimasi/1, 
% lokasi_sulit/1, status_parkir/2, kondisi_lalin/2.

% -----------------------------------------------------------------
% 1. DEFINISI FACTS (Minimal 15 Facts / Proposisi Dasar)
% -----------------------------------------------------------------

% Fakta Spesifik untuk Uji Rantai (Minimal 2 Facts)
lokasi_populer(area_dago).                  % 1
mengunjungi(wisatawan_A, area_dago).        % 2

% Fakta Konstanta (Minimal 3 Konstanta)
wisatawan(wisatawan_A).                     % 3
wisatawan(wisatawan_B).                     % 4
area(area_dago).                            % 5
area(area_cihampelas).                      % 6
area(area_braga).                           % 7

% Fakta Status & Kondisi (Aritas > 1)
% Status Lalu Lintas
kondisi_lalin(area_dago, padat).            % 8
kondisi_lalin(area_braga, lancar).          % 9

% Status Parkir
memiliki_fasilitas(area_dago, parkir_motor). % 10
status_parkir(area_dago, sulit).            % 11 
status_parkir(area_cihampelas, mudah).      % 12

% Data Jarak (Untuk Rule baru, minimal 3 Facts)
% Format: jarak(Lokasi1, Lokasi2, Jarak_KM)
jarak(area_dago, area_braga, 5).            % 13
jarak(area_cihampelas, area_dago, 7).       % 14
jarak(area_braga, area_cihampelas, 10).     % 15 
jarak(area_cihampelas, area_braga, 10).     % 16 <-- Tambahan untuk memenuhi minimal 15

% Fakta Tambahan (Opsional: untuk menguji kondisi False)
mengunjungi(wisatawan_B, area_braga).       % 17
lokasi_populer(area_braga).                 % 18

% -----------------------------------------------------------------
% 2. DEFINISI RULES (Minimal 8 Rules / Implikasi FOL)
% -----------------------------------------------------------------

% --- A. RANTAI INFERENSI 3 LANGKAH (P -> Q -> R -> S) ---

% Rule 1: Jika lokasi populer, maka antrean panjang (P1 -> P2)
antrean_panjang(Area) :- 
    lokasi_populer(Area).                   % 1

% Rule 2: Jika antrean panjang DAN wisatawan mengunjungi, maka fisik lelah (P2 ^ V -> P3)
fisik_lelah(Wisatawan) :- 
    antrean_panjang(Area), 
    mengunjungi(Wisatawan, Area).           % 2

% Rule 3: Jika fisik lelah, maka pengalaman buruk (P3 -> P4)
pengalaman_buruk(Wisatawan) :- 
    fisik_lelah(Wisatawan).                 % 3

% --- B. RULES TAMBAHAN (Minimal 5 Rules Baru) ---

% Rule 4: Lokasi dianggap 'sulit' jika lalin padat DAN parkir sulit (Konjungsi)
lokasi_sulit(Area) :-
    kondisi_lalin(Area, padat),
    status_parkir(Area, sulit).             % 4

% Rule 5: Sebuah area 'terisolasi' jika jarak ke area lain JAUH (e.g. > 7 km) (Implikasi + Perbandingan)
terisolasi(Area) :-
    area(Area),
    jarak(Area, _, Jarak),
    Jarak > 7.                              % 5

% Rule 6: Wisatawan 'repot' jika mengunjungi lokasi populer yang tidak punya parkir motor (Konjungsi Negasi)
wisatawan_repot(Wisatawan) :-
    mengunjungi(Wisatawan, Area),
    lokasi_populer(Area),
    \+ memiliki_fasilitas(Area, parkir_mobil). % 6 

% Rule 7: Wisatawan 'puas' jika tidak mendapat pengalaman buruk (Negasi)
wisatawan_puas(Wisatawan) :-
    wisatawan(Wisatawan),
    \+ pengalaman_buruk(Wisatawan).          % 7

% Rule 8: Rute 'buruk' jika salah satu area di dalamnya sulit DAN terisolasi (Konjungsi Kompleks)
rute_buruk(Rute) :-
    rute_mengandung(Rute, Area), % Contoh predikat relasi baru (perlu fakta rute_mengandung)
    lokasi_sulit(Area),
    terisolasi(Area).                       % 8

% Rule Tambahan (Opsional, untuk melengkapi Rule 8)
rute_mengandung(rute_utara, area_dago).
rute_mengandung(rute_utara, area_cihampelas).