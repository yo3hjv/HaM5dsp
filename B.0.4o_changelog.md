================================================================================
vB.0.4o - Heartbeat LED Fix when Inactivity Timer is OFF (2026-06-06)
--------------------------------------------------------------------------------
- [BUGFIX][SCREENSAVER] Heartbeat LED: Corectarea funcției screensaveUpdate() în screensaver_manager.cpp prin permiterea executării logicii de clipire/puls a LED-ului în modul Energy Saver (Backlight OFF) chiar și atunci când temporizatorul automat de inactivitate este dezactivat (Timer = OFF / scr_saver_timer == 0), dar modul a fost pornit manual (de exemplu, prin comanda serială SSAV9).

================================================================================
vB.0.4n - Screensaver Wake via SSAO Fix (2026-06-06)
--------------------------------------------------------------------------------
- [BUGFIX][SCREENSAVER] SSAO Command: Corectarea comportamentului comenzii seriale SSAO (Screensaver OFF) prin înlocuirea modificării directe a variabilei g_scr_saver_active cu apelul funcției standard screensaveReset(). Aceasta asigură restabilirea luminozității backlight-ului (BL), oprirea corectă a LED-ului de heartbeat și redesenarea UI-ului, rezolvând blocarea ecranului stins după recepționarea comenzii.

================================================================================
vB.0.4m - Conditional Debug Logs Clean up (2026-06-06)
--------------------------------------------------------------------------------
- [SYSTEM][DEBUG] MP3 & SD Logs: Filtrarea ultimelor mesaje de debug persistente pe serială: scanarea directoarelor/pieselor SD (Found Tape:..., Total SD Tapes:...) în parseSDforMp3.cpp și pregătirea listei shuffle (SHUFFLE PREPARE:...) în mp3.cpp sunt acum controlate corect de macro-ul SYSTEM_DEBUG_LOGS_ENABLED din config.h (implicit 0/dezactivate).

================================================================================
vB.0.4l - LED Feedback, Level Capping & Screensaver Heartbeat relocation (2026-06-06)
--------------------------------------------------------------------------------
- [POWER][UI/UX] Power Diagnostics: Limitarea la maximum 99% a procentajului bateriei afișat în UI pe durata încărcării active (is_charging=true) pentru a preveni indicarea prematură sau derutantă de 100% în faza CV a încărcării.
- [PERIPHERALS] Module Audio M144: Adăugarea indicatorului LED de încărcare pe LED-ul 0 (Dreapta, lângă mufa USB-C), activabil opțional prin macro-ul CHARGE_LED_FEEDBACK_ENABLED din config.h. Acesta clipește roșu la încărcare activă, rămâne verde constant la încărcare completă (pe USB) și se stinge complet la deconectarea USB pentru a preveni consumul suplimentar de energie.
- [PERIPHERALS][SCREENSAVER] Relocarea heartbeat-ului pe LED-ul 2 (Stânga, cel îndepărtat) în modul Screensaver cu backlight oprit (anterior pe LED-ul 1), asigurând o separare totală a rolurilor LED-urilor (Stânga = Heartbeat, Mijloc = VAS, Dreapta = Încărcare).
- [POWER][BUGFIX] Screensaver Backlight: Corectarea funcției updatePowerRails() din pwr_mgmt.cpp prin condiționarea DCDC3 (alimentarea backlight-ului) de ambele stări: g_lcd_power_en și s_backlight_enabled. Acest lucru permite stingerea completă a iluminării ecranului în modul Energy Saver (ecran stins) când s_backlight_enabled = false, chiar dacă logica LCD-ului (LDO2) rămâne activă.

================================================================================
vB.0.4k - Smart Refresh, Circular Lists, Slider NR Lev & Screensaver Fix (2026-06-06)
--------------------------------------------------------------------------------
- [BUGFIX][UI/UX] Power Diagnostics: Implementarea tehnicii de Smart Refresh (flicker-free) prin eliminarea ștergerii cu fillRect și înlocuirea cu text cu fundal solid și padding cu spații (lățime fixă). De asemenea, s-a eliminat din listă indicatorul redundat de filtru ADC ("ADC Filter"), reducând elementele la 6.
- [UI/UX] MP3 List: Adăugarea navigării circulare (wrap-around) pe butoanele UP și DN pentru liste de casete (tapes) și melodii (tracks).
- [UI/UX] Slider Carousel: Adăugarea parametrului "NR Lev" (Noise Reduction Aggressiveness) în caruselul sliderelor, activ exclusiv în modul VOICE (tranziție: Vol -> Lcut -> Hcut -> NR Lev -> Vol). În modurile CW, acesta este omis automat.
- [BUGFIX][UI/UX] Screensaver: Rezolvarea suprapunerii ceasului/datei peste elementele din Main Viewport la utilizarea comenzii seriale SSAV9 sau SSAO. S-a realizat prin forțarea resetării variabilei tranzitorii s_wasActive la false atunci când screensaver-ul devine inactiv (în screensaveUpdate()) și unificarea activării în screensaveActivate().
- [SYSTEM] Centralizarea și opționalizarea mesajelor de debug pe serială prin optiunea de compilare SYSTEM_DEBUG_LOGS_ENABLED în config.h.

================================================================================
vB.0.4j - Corecții Alimentare Periferice 5V & ADC AXP192 (2026-06-06)
--------------------------------------------------------------------------------
- [POWER][BUGFIX] Corectarea bug-ului critic de mapare a biților din registrul 0x12 (Power Control) din pwr_mgmt.cpp: EXTEN a fost mutat de pe Bit 0 (care controla eronat DCDC1-ul de 3.3V al ESP32 și oprea alimentarea) pe Bit 6 (EXTEN hardware). DCDC1 este garantat permanent pornit (Bit 0 setat fix pe 1).
- [POWER] Aplicarea setării pentru alimentare periferice ("Perif. 5V: OUT/IN" redenumit din "VBUS Mode") se face exclusiv la boot/reboot (din pwr_init()), eliminând apelarea live la runtime și salvare în saveAndBack() pentru a evita drop-urile tranzitorii de tensiune (brownout) pe timpul funcționării active.
- [POWER] Adăugarea detecției duale a tensiunii pe USB-C lateral (VBUS - Bit 5 din AXP192 Reg 0x00) pe lângă alimentarea prin dock/bază (ACIN - Bit 7), asigurând reflectarea corectă a stării "usb_plugged" și actualizarea grafică în header când se folosește mufa de pe placă.
- [POWER] Configurare condiționată a registrului 0x30 la pornire (în pwr_apply_perif_5v()): în modul OUT se forțează calea VBUS-IPSOUT prin 0x80 (datorită blocării hardware a N_VBUSEN prin linia EXTEN), iar în modul IN se menține registrul la valoarea sa implicită (0x02), prevenind un conflict analogic ce ducea la crash.
- [POWER][BUGFIX] Corectarea citirii telemetriei de curent (încărcare reg 0x7A, descărcare reg 0x7C) prin reintroducerea citirii corecte pe 13 biți (readAxp13) cu rezoluție de 0.5mA, rezolvând eroarea de înjumătățire a valorilor care apărea la folosirea funcției de 12 biți.
- [UI/DEVSET] Redenumirea opțiunii din Setup -> Device în "Perif. 5V: OUT/IN" și adăugarea sufixului "*Reboot" (ex. "Perif. 5V: OUT *Reboot") pentru a indica vizual necesitatea repornirii pentru aplicarea setării hardware.

================================================================================
vB.0.4i - AXP192 Power Refactoring & VU-Meter Propagation Fix (2026-06-05)
--------------------------------------------------------------------------------
- [POWER] Refactorizarea completă a managementului alimentării AXP192. Adăugarea unui nou element de setare "VBUS" în meniul DevSet Setup, cu stările `OFF`, `IN` (Input), `OUT` (Output), oferind configurare runtime flexibilă, memorare persistentă în NVS și limitarea curentului de încărcare a bateriei principale la `450mA` prin `BATT_CHARGE_CURRENT_LIMIT` în `config.h`.
- [BUGFIX][POWER] Detecția stării de încărcare (`is_charging`) se bazează acum pe bitul 2 din registrul `0x00` (sensul fizic al curentului prin baterie: `1` = încărcare, `0` = descărcare), prevenind blocarea pe starea de încărcare și rezolvând afișarea `+0.0mA` pe baterie. Curentul din header indică `i_acin` (din USB) când încarcă, respectiv `-i_discharge` cu minus și portocaliu fix (`0xFDA0`) când se descarcă.
- [BUGFIX][POWER] Curentul de încărcare a bateriei (`i_charge`) este citit corect pe 13 biți (`readAxp13(0x7A, 0x7B)`), eliminând zgomotul citirii anterioare pe 12 biți și eliminând logica redundantă de override software din `pwr_update()`.
- [UI/VU-METER] Inversarea ordinii de propagare a LED-urilor VU-metrului (SK6812),
  aprinzându-se acum de jos în sus pe ambele părți (Led5-Led1 pe stânga, Led10-Led6
  pe dreapta).
- [UI/VU-METER] Adăugarea unui prag de liniște (gate) de `3%` pentru stingerea completă
  a LED-urilor în absența semnalului. De asemenea, LED-urile sunt acum stinse complet
  când redarea MP3 este pusă pe pauză (`PAUSE`).

================================================================================
vB.0.4g - CWspdL/CWspdH Edit Fix & After_Boot Script (2026-06-05)
--------------------------------------------------------------------------------
- [BUGFIX][UI/UX] Repararea comportamentului butonului fizic BtnC în submeniul
  Setup -> CwSet pentru parametrii CWspdL (MENU_CW_MIN_WPM) și CWspdH
  (MENU_CW_MAX_WPM). Anterior, BtnC incrementa eronat valoarea în loc să o
  decrementeze și nu salva în NVS. S-a simplificat logica la o decrementare directă
  cu 1 la fiecare apăsare scurtă (limită minimă 5 pentru Min WPM, respectiv
  Min WPM + 1 pentru Max WPM), eliminând comportamentul complex de longPress în
  modul editare și integrând apelul corect de persistență `prefsSaveCwDec()`.
- [SYSTEM] Actualizarea versiunii oficiale de firmware la "B.0.4g" în M5DSP.ino.
- [SCRIPTS] Implementarea noului script interactiv After_Boot/after_boot.py
  (înlocuind vechiul preset_mem.py) scris complet în limba engleză. Acesta
  scanează dinamic porturile seriale disponibile, permite configurarea interactivă
  a cheii de licențiere (prin comanda AUTH::[key] cu validare regex) și oferă un
  meniu cu 5 opțiuni, inclusiv programarea combinată a licenței și preset-urilor
  consecutiv într-o singură conexiune.

================================================================================
vB.0.4f - ReviveScreen Touch Guard (2026-05-28)
--------------------------------------------------------------------------------
- [UI/UX] Implementarea protecției ReviveScreen Touch Guard la trezirea din
  Energy Saver. La finalizarea long-press-ului de trezire (ESAVER_WAKE_TOUCH_MS),
  degetul rămâne fizic pe ecran și poate declanșa comenzi accidentale pe UI-ul
  redesenat. Soluție în două straturi:
    * Strat 1 (Finger-Still Guard): Cât timp degetul care a efectuat long-press-ul
      este încă pe ecran (`points > 0`), orice procesare de touch/butoane este
      blocată complet prin `continue` în task-ul UI.
    * Strat 2 (Cooldown Timer): După ridicarea degetului, touch-ul rămâne blocat
      pentru un interval suplimentar `ESAVER_REVIVE_COOLDOWN_MS` (config.h,
      default 300 ms, range 20–1000 ms), prevenind interpretarea accidentală a
      gestului de ridicare rapidă.
  Implementare: variabile statice (`s_reviveGuardActive`, `s_reviveGuardStart`,
  `s_reviveFingerWasDown`) co-localizate în blocul ESaver din `taskUi()` în
  `M5DSP.ino`. Nu necesită modificări în `screensaver_manager`.
- [CONFIG] Adăugare constantă `ESAVER_REVIVE_COOLDOWN_MS` în `config.h` în
  grupul constantelor Energy Saver, cu documentare inline completă.
- [BUGS][SERIAL] Rezolvat inactivarea comenzilor la activarea EnergySaver/ScreenSaver
