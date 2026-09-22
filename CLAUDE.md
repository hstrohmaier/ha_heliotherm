# ha_heliotherm

Home Assistant Custom Component für Heliotherm-Wärmepumpen (und kompatible Brötje-NEO-Wärmepumpen mit NEO-RKM) über Modbus TCP, angesprochen via Heliotherm RCG-Interface.

## Architektur

Alle Modbus-Register werden einmalig in `ENTITIES_DICT` in `const.py` deklariert. Die Funktion `const.init(detected_version)` klassifiziert jeden Eintrag anhand von Registertyp und Datenform in typisierte Dicts — `SENSOR_TYPES`, `SELECT_TYPES`, `BINARY_TYPES`, `NUMBER_TYPES`, `CLIMATE_TYPES` usw. Jede Plattform-Datei (`sensor.py`, `select.py`, ...) ruft `setup_platform_from_types()` aus `entity_common.py` auf, das für jeden Eintrag im jeweiligen Dict die passende `HubBackedEntity`-Subklasse instanziiert.

## Entität hinzufügen/ändern

1. Eintrag in `ENTITIES_DICT` in `const.py` anlegen/ändern.
2. Registerfelder: `RT` (Registertyp), `REG` (0-basierte Adresse), `NAME`, `DT` (Datentyp), optional `UNIT`, `FAKTOR`, `MIN`, `MAX`, `VALUES` (für Selects/Enums), `PF` (Plattform-Override), `HA` (zugeordnetes Hand-Aktiv-Register, siehe eigener Abschnitt unten).
3. Übersetzungen in `translations/en.json` und `translations/de.json` unter dem passenden Plattform-Key ergänzen.
4. Kein Plattform-Code nötig, außer eine neue Plattform kommt hinzu.

**Registertypen:**
- `C_REG_TYPE_INPUT_REGISTERS` → read-only Sensor
- `C_REG_TYPE_HOLDING_REGISTERS` → read-write (Number/Select/Climate)
- `C_REG_TYPE_DISCRETE_INPUTS` → read-only Binary Sensor
- `C_REG_TYPE_COILS` → read-write Switch

**Plattform-Override:** `"PF": Platform.NUMBER` (o.ä.) erzwingt eine Klassifizierung unabhängig vom Registertyp.

## Firmware-abhängige Registerdefinitionen

Beim Setup wird die RCG-Firmwareversion über `webmi_version.detect_firmware_version()` per WebMI-HTTP-Handshake (RSA-verschlüsselte Session, siehe `webmi_version.py`) ermittelt und an `const.init(version)` übergeben. Ist die Erkennung nicht möglich, fällt der Code auf die zuletzt in den Config-Entry-Options gespeicherte Firmwareversion (`CONF_FIRMWARE`) zurück. `const.init()` wendet darauf basierend Versions-Patches auf `ENTITIES_DICT` an (Registereinträge werden ab bestimmten Mindestversionen hinzugefügt/entfernt) — siehe die Patch-Logik rund um `Version(min_version)` in `const.py`.

## Hand-Aktiv-Register (Handwert/Hand-Aktiv-Paare)

Ein Teil der schreibbaren RCG-Parameter (u. a. Rücklaufsolltemperatur, MKR1-/MKR2-Solltemperatur, Aussentemperatur-, Puffertemperatur-, Brauchwassertemperatur- und Raumfühler-1-Handwert, 2. Stufe, EVU-Sperre, TF22, Zirkulationspumpe WW) ist in der Firmware als Registerpaar modelliert:

- ein **Wertregister** ("Handwert", z. B. `C_RUECKLAUFSOLLTEMPERATUR`, REG 102) — der gewünschte Sollwert,
- unmittelbar danach ein **Hand-Aktiv-Flag-Register** (z. B. `C_RUECKLAUFSOLLTEMPERATUR_HAND_AKTIV`, REG 103) — schaltet um, ob die Steuerung diesen manuell vorgegebenen Wert tatsächlich verwendet (1 = "Hand"/manuell) oder ihren eigenen berechneten Wert (0 = "Automatik").

Nur das Wertregister zu schreiben hat für sich genommen keine Wirkung: Die Wärmepumpe bleibt im Automatik-Modus, solange das zugehörige Hand-Aktiv-Flag nicht ebenfalls auf 1 gesetzt ist.

In `const.py` wird diese Kopplung über das Feld `"HA": <entity_key des Hand-Aktiv-Registers>` am Wertregister-Eintrag in `ENTITIES_DICT` hergestellt (Kommentar `# HA: Zugeordnete Hand-Aktiv-Entität`); `get_entity_ha()` liest das aus.

**Automatisches Setzen beim Schreiben:** `MyModbusHub.write_entity_value()` in `__init__.py` schreibt nach dem eigentlichen Wert automatisch `1` in das zugeordnete Hand-Aktiv-Register (Schritt 3, "Hand-Aktiv setzen"), sofern die Entität ein `HA`-Feld besitzt. Aus HA-Sicht genügt es also, den Number-/Climate-Wert zu setzen — die Aktivierung des Handmodus passiert transparent im Hintergrund.

**Sichtbar, aber als Konfigurations-Entität:** Die Hand-Aktiv-Companion-Schalter werden in `const.init()` immer angelegt, aber mit `entity_category=EntityCategory.CONFIG` versehen (siehe `MyBinaryEntityDescription`-Zweig in `const.py`). Home Assistant zeigt Entitäten dieser Kategorie nicht in der Haupt-Card, sondern in einem eigenen "Konfiguration"-Abschnitt auf der Geräteseite. Dadurch lässt sich der Handmodus für **jedes** Register wieder auf "Automatik" (0) zurückschalten, ohne die normale Entitätsliste mit technischen Hilfsschaltern zu überfluten. Das war ursprünglich als bekanntes Problem (mbuchber/ha_heliotherm#68) nur für `C_RUECKLAUFSOLLTEMPERATUR_HAND_AKTIV` per fest codierter Ausnahme (`exposed_companion_entities`-Whitelist) gelöst; diese Whitelist wurde entfernt und durch die generische `entity_category`-Lösung für alle elf Handwert/Hand-Aktiv-Paare ersetzt.

**Für neue Entitäten:** Beschreibt die RCG-Dokumentation ein neues Register ebenfalls als Handwert/Hand-Aktiv-Paar, muss das Wertregister das `"HA"`-Feld auf den entity_key des Hand-Aktiv-Registers setzen — die `entity_category=CONFIG`-Zuordnung für den Hand-Aktiv-Schalter passiert dann automatisch, weil `const.init()` jeden per `HA` referenzierten entity_key in `ha_entities` sammelt und daran erkennt.

## Hub (`MyModbusHub` in `__init__.py`)

- Pollt alle Register alle N Sekunden (Default 15) über `async_refresh_modbus_data()`. Der komplette Zyklus Connect → Lesen → Close läuft über `_do_read_cycle()` in einem Executor-Thread **unter einem einzigen `self._lock`**.
- Schreiben über `hub.write_entity_value(entity_key, value)` — kodiert den Wert und löst danach automatisch einen Refresh aus. `_write_modbus_registers()` hält `self._lock` ebenfalls über den kompletten Connect → Schreiben → Close-Zyklus.
- **Wichtig:** Der Lock muss immer den gesamten Connect-Betrieb-Close-Zyklus umschließen, nie nur einzelne Read-/Write-Aufrufe. Andernfalls können gleichzeitige Lese- und Schreibzugriffe denselben TCP-Socket parallel benutzen und zu `EBADF`/"bad file descriptor"-Fehlern führen. 
- Modbus-Antworten beim Schreiben (`write_coil`/`write_register`) werden über `response.isError()` geprüft und im Fehlerfall geloggt (siehe Known Issues zur Race Condition, die trotzdem bestehen bleibt).
- Entity-Callbacks werden über `hub.async_add_my_modbus_sensor(callback)` registriert.

## Entity-Update-Flow

`HubBackedEntity._on_hub_update()` (in `entity_common.py`) wird bei jedem Poll aufgerufen. Für Entitäten mit einem einzelnen Register ruft es `_apply_hub_payload(hub.data[description.key])` auf. `_on_hub_update` wird direkt überschrieben (z. B. bei der Climate-Entität), wenn mehrere Register aggregiert werden müssen.

## Schwesterprojekt: ha_comfoconnectpro

Dieses Repository wurde ursprünglich als Kopie von [`ha_comfoconnectpro`](https://github.com/hstrohmaier/ha_comfoconnectpro) (Zehnder ComfoConnect PRO, ebenfalls Modbus TCP über pymodbus) erstellt. Beide Projekte teilen sich weitgehend dieselbe Struktur von `__init__.py`, `entity_common.py` und `const.py`. **Fehlerbehebungen an der Modbus-I/O-Schicht sind in beiden Projekten praktisch immer relevant.** Bei Problemen mit der Modbus-Kommunikation hier lohnt sich ein Blick in die Commit-Historie von `ha_comfoconnectpro` (insbesondere zu Locking, `device_id=` vs. `slave=`-Parametern und Lese-/Schreib-Serialisierung), ob dort bereits ein Fix existiert, der hier noch nicht übernommen wurde — und umgekehrt.

Bereits aus `ha_comfoconnectpro` übernommene Fixes (Stand: Portierung auf Basis von dessen Releases 1.0.8 → 1.1.0 sowie den nachfolgenden Modbus-Locking-Fixes bis 1.1.8):
- `config_flow.host_valid()`: IPv6-Adressen wurden durch den Bug `.version == (4 or 6)` (wertet zu `== 4` aus) fälschlich abgelehnt; korrigiert zu `.version in (4, 6)`.
- `const.py`: Wildcard-Import `from homeassistant.components.sensor import *` durch explizite Imports ersetzt.
- `read_entity_value()`: fehlendes `f`-Prefix im Fehlertext (Variablen wurden als literale `{...}` statt interpoliert ausgegeben).
- `read_modbus_registers()`: doppelte Validierungsblöcke zu `_validate_modbus_response()` zusammengeführt.
- `_write_modbus_registers()`: Antwort von `write_coil`/`write_register` wird jetzt per `isError()` geprüft und geloggt, statt sie stillschweigend zu verwerfen.
- `async_refresh_modbus_data()`/`read_modbus_registers()`: kompletter Connect→Lesen→Close-Zyklus läuft jetzt unter einem einzigen Lock im Executor-Thread (siehe Hub-Abschnitt oben).

## Bekannte, ungelöste Probleme (auch in ha_comfoconnectpro offen)

- **Switch-/Coil-Zustand springt 1–3 Sekunden nach dem Schreiben zurück** ([ha_comfoconnectpro#23](https://github.com/hstrohmaier/ha_comfoconnectpro/issues/23)): `write_entity_value()` löst direkt nach dem Schreiben einen `async_refresh_modbus_data()`-Zyklus aus. Hat die Wärmepumpe/das Gerät den Schreibzugriff zu diesem Zeitpunkt noch nicht verarbeitet, liefert der sofortige Re-Read den alten Wert zurück und die Entität springt kurzzeitig auf den ursprünglichen Zustand zurück. Vermutete Ursache laut Issue: derselbe Race-Condition-Musterfehler wie in home-assistant/core#53826 / #53948 (State-Verifikation liest einen veralteten Wert direkt nach dem Schreiben). **Noch nicht behoben** — weder hier noch in `ha_comfoconnectpro`. Ein Fix müsste vermutlich entweder eine kurze Verzögerung/einen Retry vor dem Post-Write-Refresh einbauen oder sich auf den optimistisch gesetzten Entitätszustand verlassen, statt sofort neu zu lesen.

## Linting

```
ruff check .
ruff format .
```

## CI

GitHub Actions führen bei jedem Push `hassfest` (HA-Manifest-Validierung) und `hacs`-Validierung aus, siehe `.github/workflows/`. Keine Unit-Tests vorhanden.
