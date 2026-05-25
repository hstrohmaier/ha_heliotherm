"""Constants for the integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any, Callable, Awaitable
from copy import deepcopy
from packaging.version import Version, InvalidVersion

import sys

from homeassistant.components.climate import (
    ClimateEntityDescription,
    ClimateEntityFeature,
)
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.sensor import *
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberDeviceClass,
)
from homeassistant.const import (
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfEnergy,
    UnitOfPower,
    CONF_NAME,
    Platform,
)

from pymodbus.client import ModbusTcpClient

import logging

thismodule = sys.modules[__name__]
_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.info(f"{thismodule} loaded")




DOMAIN = "ha_heliotherm"
DEFAULT_NAME = "Heliotherm Heatpump"
DEFAULT_SCAN_INTERVAL = 15
DEFAULT_PORT = 502
DEFAULT_HOSTID = 1
DEFAULT_FIRMWARE = "1.2.0.5"
CONF_HOSTID = "hostid"
CONF_FIRMWARE = "firmware"
CONF_HUB = "haheliotherm_hub"
ATTR_MANUFACTURER = "Heliotherm"

# --- Konstanten ---

# Datentyp für coils oder discrete_inputs
C_DT_BITS = ModbusTcpClient.DATATYPE.BITS  # "bit"     # 1 Bit

# Datentypen für input_registers or holding_registers
C_DT_INT16 = ModbusTcpClient.DATATYPE.INT16  # "INT16"     # 1 Register
C_DT_UINT16 = ModbusTcpClient.DATATYPE.UINT16  # "UINT16"   # 1 Register
C_DT_INT32 = ModbusTcpClient.DATATYPE.INT32  # "INT32"   # 2 Register
C_DT_UINT32 = ModbusTcpClient.DATATYPE.UINT32  # "UINT32"   # 2 Register

C_MIN_INPUT_REGISTER = sys.maxsize
C_MAX_INPUT_REGISTER = -1
C_MIN_HOLDING_REGISTER = sys.maxsize
C_MAX_HOLDING_REGISTER = -1
C_MIN_COILS = sys.maxsize
C_MAX_COILS = -1
C_MIN_DISCRETE_INPUTS = sys.maxsize
C_MAX_DISCRETE_INPUTS = -1

# Konstanten zur Definition der Registerart
C_REG_TYPE_UNKNOWN = 0
C_REG_TYPE_COILS = 1
C_REG_TYPE_DISCRETE_INPUTS = 2
C_REG_TYPE_HOLDING_REGISTERS = 3
C_REG_TYPE_INPUT_REGISTERS = 4

# ------------------------------------------------------------
# 2) Entity-Konstanten (C_<NAME> = "<entity_key>")
#    >> Diese Konstanten dienen als Keys im ENTITIES_DICT.
# ------------------------------------------------------------
C_TEMP_AUSSEN = "temp_aussen"
C_TEMP_BRAUCHWASSER = "temp_brauchwasser"
C_TEMP_VORLAUF = "temp_vorlauf"
C_TEMP_RUECKLAUF = "temp_ruecklauf"
C_TEMP_PUFFERSPEICHER = "temp_pufferspeicher"
C_TEMP_EQ_EINTRITT = "temp_eq_eintritt"
C_TEMP_EQ_AUSTRITT = "temp_eq_austritt"
C_TEMP_SAUGGAS = "temp_sauggas"
C_TEMP_VERDAMPFUNG = "temp_verdampfung"
C_TEMP_KONDENSATION = "temp_kondensation"
C_TEMP_HEISSGAS = "temp_heissgas"
C_NIEDERDRUCK = "niederdruck"
C_HOCHDRUCK = "hochdruck"
C_HEIZKREISPUMPE = "heizkreispumpe"
C_PUFFERLADEPUMPE = "pufferladepumpe"
C_VERDICHTER = "verdichter"
C_STOERUNG = "stoerung"
C_VIERWEGENVENTIL_ABTAUBETRIEB = "vierwegenventil_abtaubetrieb"
C_WMZ_DURCHFLUSS = "wmz_durchfluss"
C_N_SOLL_VERDICHTER = "n_soll_verdichter"
C_COP = "cop"
C_TEMP_FRISCHWASSER = "temp_frischwasser"
C_EVU_SPERRE_AKTIV = "evu_sperre_aktiv"
C_TEMP_AUSSEN_VERZOEGERT = "temp_aussen_verzoegert"
C_HKR_SOLLTEMP = "hkr_solltemp"
C_MKR1_SOLLTEMP = "mkr1_solltemp"
C_MKR2_SOLLTEMP = "mkr2_solltemp"
C_EQ_VENTILATOR_PUMPE = "eq_ventilator_pumpe"
C_WW_VORRANG_WW = "ww_vorrang_ww"
C_KUEHLEN_UMV_PASSIV = "kuehlen_umv_passiv"
C_EXPANSIONSVENTIL = "expansionsventil"
C_VERDICHTERANFORDERUNG = "verdichteranforderung"

C_BETRIEBSSTUNDEN_IM_WW_BETRIEB = "betriebsstunden_im_ww_betrieb"
C_BETRIEBSSTUNDEN_IM_HZG_BETRIEB = "betriebsstunden_im_hzg_betrieb"
C_MKR1_VORLAUFTEMPERATUR = "mkr1_vorlauftemperatur"
C_MKR1_RUECKLAUFTEMPERATUR = "mkr1_ruecklauftemperatur"
C_MKR2_VORLAUFTEMPERATUR = "mkr2_vorlauftemperatur"
C_MKR2_RUECKLAUFTEMPERATUR = "mkr2_ruecklauftemperatur"
C_RAUMFUEHLER_1 = "raumfuehler_1"
C_SOLAR_KT1 = "solar_kt1"
C_FLOW_PRI = "flow_pri"
C_EQ_VENTILATOR_PUMPE_PROZENT = "eq_ventilator_pumpe_prozent"

C_WMZ_HEIZUNG = "wmz_heizung"
C_STROMZAEHLER_HEIZUNG = "stromzaehler_heizung"
C_WMZ_BRAUCHWASSER = "wmz_brauchwasser"
C_STROMZAEHLER_BRAUCHWASSER = "stromzaehler_brauchwasser"
C_STROMZAEHLER_GESAMT = "stromzaehler_gesamt"
C_STROMZAEHLER_LEISTUNG = "stromzaehler_leistung"
C_WMZ_GESAMT = "wmz_gesamt"
C_WMZ_LEISTUNG = "wmz_leistung"

C_BETRIEBSART = "select_betriebsart"
C_RAUMSOLLTEMPERATUR = "climate_raumsolltemperatur"
C_RUECKLAUFSOLLTEMPERATUR = "climate_ruecklaufsolltemperatur"
C_RUECKLAUFSOLLTEMPERATUR_HAND_AKTIV = "switch_ruecklaufsolltemperatur_hand_aktiv"
C_MIN_RUECKLAUFTEMPERATUR_KUEHLEN = "climate_min_ruecklauftemperatur_kuehlen"
C_WW_NORMALTEMPERATUR = "climate_ww_normaltemperatur"
C_WW_MINIMALTEMPERATUR = "climate_ww_minimaltemperatur"
C_MKR1_BETRIEBSART = "select_mkr1_betriebsart"
C_MKR1_RAUMSOLLTEMPERATUR = "climate_mkr1_raumsolltemperatur"
C_MKR1_SOLLTEMPERATUR = "climate_mkr1_solltemperatur"
C_MKR1_SOLLTEMPERATUR_HAND_AKTIV = "switch_mkr1_solltemperatur_hand_aktiv"
C_MKR1_MIN_RUECKLAUFTEMPERATUR_KUEHLEN = "climate_mkr1_min_ruecklauftemperatur_kuehlen"
C_MKR2_BETRIEBSART = "select_mkr2_betriebsart"
C_MKR2_RAUMSOLLTEMPERATUR = "climate_mkr2_raumsolltemperatur"
C_MKR2_SOLLTEMPERATUR = "climate_mkr2_solltemperatur"
C_MKR2_SOLLTEMPERATUR_HAND_AKTIV = "switch_mkr2_solltemperatur_hand_aktiv"
C_MKR2_MIN_RUECKLAUFTEMPERATUR_KUEHLEN = "climate_mkr2_min_ruecklauftemperatur_kuehlen"
C_PV_ANFORDERUNG = "switch_pv_anforderung"
C_PV_HEIZEN_OFFSET = "climate_pv_heizen_offset"
C_PV_KUEHLEN_OFFSET = "climate_pv_kuehlen_offset"
C_PV_HEIZEN_OFFSET_MKR1 = "climate_pv_heizen_offset_mkr1"
C_PV_KUEHLEN_OFFSET_MKR1 = "climate_pv_kuehlen_offset_mkr1"
C_PV_HEIZEN_OFFSET_MKR2 = "climate_pv_heizen_offset_mkr2"
C_PV_KUEHLEN_OFFSET_MKR2 = "climate_pv_kuehlen_offset_mkr2"
C_WW_NORMAL_MAX = "climate_ww_normal_max"
C_VORGABE_LEISTUNGSAUFNAHME = "input_vorgabe_leistungsaufnahme"
C_VORGABE_VERDICHTERDREHZAHL = "input_vorgabe_verdichterdrehzahl"
C_EXT_ANFORDERUNG = "switch_ext_anforderung"
C_ENTSTOEREN = "switch_entstoeren"
C_AUSSENTEMPERATUR_HANDWERT = "climate_aussentemperatur_handwert"
C_AUSSENTEMPERATUR_HAND_AKTIV = "switch_aussentemperatur_hand_aktiv"
C_PUFFERTEMPERATUR_HANDWERT = "climate_puffertemperatur_handwert"
C_PUFFERTEMPERATUR_HAND_AKTIV = "switch_puffertemperatur_hand_aktiv"
C_BRAUCHWASSERTEMPERATUR_HANDWERT = "climate_brauchwassertemperatur_handwert"
C_BRAUCHWASSERTEMPERATUR_HAND_AKTIV = "switch_brauchwassertemperatur_hand_aktiv"
C_HKR_HEIZGRENZE = "climate_hkr_heizgrenze"
C_HKR_RUECKLAUFSOLL_BEI_HEIZGRENZE = "climate_hkr_ruecklaufsoll_bei_heizgrenze"
C_HKR_RUECKLAUFSOLL_BEI_0_C = "climate_hkr_ruecklaufsoll_bei_0_c"
C_HKR_RUECKLAUFSOLL_BEI_15_C = "climate_hkr_ruecklaufsoll_bei_15_c"
C_MKR1_HEIZGRENZE = "climate_mkr1_heizgrenze"
C_MKR1_RUECKLAUFSOLL_BEI_HEIZGRENZE = "climate_mkr1_ruecklaufsoll_bei_heizgrenze"
C_MKR1_RUECKLAUFSOLL_BEI_0_C = "climate_mkr1_ruecklaufsoll_bei_0_c"
C_MKR1_RUECKLAUFSOLL_BEI_15_C = "climate_mkr1_ruecklaufsoll_bei_15_c"
C_MKR2_HEIZGRENZE = "climate_mkr2_heizgrenze"
C_MKR2_RUECKLAUFSOLL_BEI_HEIZGRENZE = "climate_mkr2_ruecklaufsoll_bei_heizgrenze"
C_MKR2_RUECKLAUFSOLL_BEI_0_C = "climate_mkr2_ruecklaufsoll_bei_0_c"
C_MKR2_RUECKLAUFSOLL_BEI_15_C = "climate_mkr2_ruecklaufsoll_bei_15_c"
C_2_STUFE_HANDWERT = "switch_2_stufe_handwert"
C_2_STUFE_HAND_AKTIV = "switch_2_stufe_hand_aktiv"
C_EVU_SPERRE_HANDWERT = "switch_evu_sperre_handwert"
C_EVU_SPERRE_HAND_AKTIV = "switch_evu_sperre_hand_aktiv"
C_TF22_HANDWERT = "input_tf22_handwert"
C_TF22_HAND_AKTIV = "switch_tf22_hand_aktiv"

## BEGIN Neu ab Firmware 2.2.0.1
C_FWS_ZIELTEMPERATUR = "climate_fws_zieltemperatur"
C_RAUMFUEHLER_1_HANDWERT = "climate_raumfuehler_1_handwert"
C_RAUMFUEHLER_1_HAND_AKTIV = "switch_raumfuehler_1_hand_aktiv"
C_ZIRKULATIONSPUMPE_WW_HANDWERT = "switch_zirkulationspumpe_ww_handwert"
C_ZIRKULATIONSPUMPE_WW_HAND_AKTIV = "switch_zirkulationspumpe_ww_hand_aktiv"
## END Neu ab Firmware 2.2.0.1


# --------------------------------------------------------------------------------------------
# 2) ENTITIES_DICT DICT, neue Register müssen nur hier zugefügt werden.
#    Sofern zusätzliche Register keine neue Logik erfordern, ist der restliche Code schon darauf vorbereitet
# --------------------------------------------------------------------------------------------
#    ENTITIES_DICT: Dict[str, Dict[str, Any]]
#    *Key = passende C_<...>-Konstante = HASS sensor_id
#    *NAME: Angezeigter Name
#    *REG: Modbus-Register (Zero-Based)
#    *RT: Register Typ (derzeit 1..4): Holding-Register, Coils (read-write) oder Input-Register, Discrete-Inputs (read-only)
#    *DT: Datentyp (derzeit nur BITS, INT16, UINT16), Hinweis: BITS für Coils und Discrete-Inputs (Angabe optional). Schalter immer mit 0 oder 1
#    RW: Read/Write für Coils und Holding-Register unterbinden mit "RW":0
#    FAKTOR: Multiplikator für Anzeige im HA (derzeit: 1, 0.1)
#    UNIT: Einheit der Entität (°C, W, kW, Wh, kWh, bar, ppm, m³/h...)
#    STEP: Steuert die Darstellung in der Anzeige im HA, Schrittweite der Einstellung (z.B. 5.0, 1.0, 0.5, 0.1)
#    MIN: Erlaubter Mindestwert der Entität
#    MAX: Erlaubter Höchstwert der Entität
#    VALUES: Gültige Auswahlwerte; dict[id,AngezeigterName] mit optionalem Bestandteil: "default":<defaultwert>
#    INC: 1, wenn Entität stetig steigende Werte liefert.
#    SWITCH: Werte für "aus" und optional für "ein". Wenn "ein" nicht angegeben ist, sind alle anderen ganzahligen Werte "ein" gültig
#    WEB_ID: Zugeordnete Web-Regler ID, wird in HASS nicht genutzt
#    HA: Zugeordnete Hand-Aktiv-Entität
#    PF: Anzeige-Variante in HA übersteuern. "PF":Platform.NUMBER v=> Temperaturwert wird nicht als CLIMATE, sondern als NUMBER behandelt.
#
#    *: Obligatorischer Wert
# --------------------------------------------------------------------------------------------

# Modbus-Register gemäß 20230705_Fachmannebene_RCGX_1.0.5.4_DE_mail.pdf vom 24.04.2023
# Änderungen nur über ENTITY_PATCHES!!
# --- ENTITIES_DICT --- wird über init() gesetzt.
ENTITIES_DICT: Dict[str, Dict[str, Any]] = {}

# BASE_ENTITIES_DICT entspricht RCG 2.1.0.5
BASE_ENTITIES_DICT: Dict[str, Dict[str, Any]] = {
    # INPUT_REGISTERS
    # --- 0-9 werden aktuell nicht genutzt ---
    C_TEMP_AUSSEN: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Aussen","REG":10,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 0"},
    C_TEMP_BRAUCHWASSER: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Brauchwasser","REG":11,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 2"},
    C_TEMP_VORLAUF: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Vorlauf","REG":12,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 3"},
    C_TEMP_RUECKLAUF: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Rücklauf","REG":13,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 4"},
    C_TEMP_PUFFERSPEICHER: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Pufferspeicher","REG":14,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 5"},
    C_TEMP_EQ_EINTRITT: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. EQ Eintritt","REG":15,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 6"},
    C_TEMP_EQ_AUSTRITT: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. EQ Austritt","REG":16,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 7"},
    C_TEMP_SAUGGAS: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Sauggas","REG":17,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 9"},
    C_TEMP_VERDAMPFUNG: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Verdampfung","REG":18,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 12"},
    C_TEMP_KONDENSATION: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Kondensation","REG":19,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 13"},
    C_TEMP_HEISSGAS: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Heißgas","REG":20,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 15"},
    C_NIEDERDRUCK: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Niederdruck","REG":21,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"bar","WEB_ID":"MP 20"},
    C_HOCHDRUCK: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Hochdruck","REG":22,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"bar","WEB_ID":"MP 21"},
    C_HEIZKREISPUMPE: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Heizkreispumpe","REG":23,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 22"},
    C_PUFFERLADEPUMPE: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Pufferladepumpe","REG":24,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 23"},
    C_VERDICHTER: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Verdichter","REG":25,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 30"},
    C_STOERUNG: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Störung","REG":26,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 31"},
    C_VIERWEGENVENTIL_ABTAUBETRIEB: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Vierwegenventil Abtaubetrieb","REG":27,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 32"},
    C_WMZ_DURCHFLUSS: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"WMZ Durchfluss","REG":28,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"l/min","WEB_ID":"MP 85"},
    C_N_SOLL_VERDICHTER: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"n-Soll Verdichter","REG":29,"DT":C_DT_INT16,"FAKTOR":1,"UNIT":"‰","WEB_ID":"MP 90"},
    # COP is dimensionless, but HA renders a proper history graph only if the entity
    # carries measurement metadata. Mirroring the original integration, we keep an
    # explicit empty unit here so _unit_mapping() yields state_class=measurement.
    C_COP: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"COP","REG":30,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"","WEB_ID":"MP 92"},
    C_TEMP_FRISCHWASSER: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Frischwasser","REG":31,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 11"},
    C_EVU_SPERRE_AKTIV: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"EVU Sperre aktiv","REG":32,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 37"},
    C_TEMP_AUSSEN_VERZOEGERT: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Temp. Aussen verzögert","REG":33,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 1"},
    C_HKR_SOLLTEMP: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"HKR Solltemp.","REG":34,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 57"},
    C_MKR1_SOLLTEMP: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"MKR1 Solltemp.","REG":35,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 66"},
    C_MKR2_SOLLTEMP: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"MKR2 Solltemp.","REG":36,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 72"},
    C_EQ_VENTILATOR_PUMPE: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"EQ Ventilator/Pumpe","REG":37,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 24"},
    C_WW_VORRANG_WW: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"WW Vorrang WW","REG":38,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 25"},
    C_KUEHLEN_UMV_PASSIV: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Kühlen UMV passiv","REG":39,"DT":C_DT_INT16,"SWITCH":{"off":0},"WEB_ID":"MP 27"},
    C_EXPANSIONSVENTIL: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Expansionsventil","REG":40,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"‰","WEB_ID":"MP 51"},
    C_VERDICHTERANFORDERUNG: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Verdichteranforderung","REG":41,"DT":C_DT_INT16,"VALUES":{0: "keine_anforderung",10: "kuehlen",20: "heizen",30: "warmwasser"},"WEB_ID":"MP 56"},
    C_BETRIEBSSTUNDEN_IM_WW_BETRIEB: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Betriebsstunden im WW-Betrieb","REG":42,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"h","WEB_ID":"SP 171"},
    C_BETRIEBSSTUNDEN_IM_HZG_BETRIEB: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Betriebsstunden im HZG-Betrieb","REG":44,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"h","WEB_ID":"SP 172"},
    C_MKR1_VORLAUFTEMPERATUR: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"MKR1 Vorlauftemperatur","REG":46,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 63"},
    C_MKR1_RUECKLAUFTEMPERATUR: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"MKR1 Rücklauftemperatur","REG":47,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 64"},
    C_MKR2_VORLAUFTEMPERATUR: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"MKR2 Vorlauftemperatur","REG":48,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 69"},
    C_MKR2_RUECKLAUFTEMPERATUR: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"MKR2 Rücklauftemperatur","REG":49,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 70"},
    C_RAUMFUEHLER_1: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Raumfühler 1","REG":50,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 16"},
    C_SOLAR_KT1: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Solar KT1","REG":51,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","WEB_ID":"MP 43"},
    C_FLOW_PRI: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Primary flow","REG":52,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"l/min","WEB_ID":"MP 104"},
    C_EQ_VENTILATOR_PUMPE_PROZENT: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"EQ Ventilator/Pumpe [%]","REG":53,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"%","WEB_ID":"MP 48"},
    # --- 54-59 werden aktuell nicht genutzt ---
    C_WMZ_HEIZUNG: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"WMZ Heizung","REG":60,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"kW/h","WEB_ID":"MP 52"},
    C_STROMZAEHLER_HEIZUNG: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Stromzähler Heizung","REG":62,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"kW/h","WEB_ID":"MP 53"},
    C_WMZ_BRAUCHWASSER: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"WMZ Brauchwasser","REG":64,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"kW/h","WEB_ID":"MP 54"},
    C_STROMZAEHLER_BRAUCHWASSER: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Stromzähler Brauchwasser","REG":66,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"kW/h","WEB_ID":"MP 55"},
    C_STROMZAEHLER_GESAMT: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Stromzähler Gesamt","REG":68,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"kW/h","WEB_ID":"MP 75"},
    C_STROMZAEHLER_LEISTUNG: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"Stromzähler Leistung","REG":70,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"W","WEB_ID":"MP 83"},
    C_WMZ_GESAMT: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"WMZ Gesamt","REG":72,"DT":C_DT_UINT32,"FAKTOR":1,"UNIT":"kW/h","WEB_ID":"MP 84"},
    C_WMZ_LEISTUNG: {"RT": C_REG_TYPE_INPUT_REGISTERS,"NAME":"WMZ Leistung","REG":74,"DT":C_DT_UINT32,"FAKTOR":0.1,"UNIT":"kW","WEB_ID":"MP 89"},
    # --- 76-99 werden aktuell nicht genutzt ---
    # HOLDING_REGISTERS
    C_BETRIEBSART: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Betriebsart","REG":100,"DT":C_DT_UINT16,"VALUES":{0: "aus",1: "automatik",2: "kuehlen",3: "sommer",4: "dauerbetrieb",5: "absenkbetrieb",6: "urlaub",7: "party","default":1},"WEB_ID":"SP 13"},
    C_RAUMSOLLTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Raumsolltemperatur","REG":101,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.5,"MIN":10.0,"MAX":25.0,"WEB_ID":"SP 69","PF":Platform.NUMBER},
    C_RUECKLAUFSOLLTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Rücklaufsolltemperatur","REG":102,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.5,"MIN":5.0,"MAX":65.0,"HA":C_RUECKLAUFSOLLTEMPERATUR_HAND_AKTIV,"WEB_ID":"MP 57","PF":Platform.NUMBER},
    C_RUECKLAUFSOLLTEMPERATUR_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Rücklaufsolltemperatur Hand-Aktiv","REG":103,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 57"},
    C_MIN_RUECKLAUFTEMPERATUR_KUEHLEN: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"min Rücklauftemperatur Kühlen","REG":104,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":1.0,"MIN":15.0,"MAX":25.0,"WEB_ID":"SP 175","PF":Platform.NUMBER},
    # Achtung: Abweichend zur Originalimplementierung: Dies ist 105/106 *KEIN* Regler mit ClimateEntityFeature.TARGET_TEMPERATURE_RANGE, sondern 106 ist die Frostschutzgrenze und 105 der Zielwert für die WW-Bereitung!!
    # Die Normaltemperatur ist nur eine Vorgabe, die Regelelektronik kann das Wasser höher erwärmen, wenn die Zykluszeit sonst zu kurz wäre.
    C_WW_NORMALTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"WW Normaltemperatur","REG":105,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":1.0,"MIN":5.0,"MAX":65.0,"WEB_ID":"SP 83","PF":Platform.NUMBER},
    C_WW_MINIMALTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"WW Minimaltemperatur","REG":106,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":1.0,"MIN":5.0,"MAX":65.0,"WEB_ID":"SP 85","PF":Platform.NUMBER},
    C_MKR1_BETRIEBSART: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Betriebsart","REG":107,"DT":C_DT_UINT16,"VALUES":{0: "aus",1: "automatik",2: "kuehlen",3: "sommer",4: "dauerbetrieb",5: "absenkbetrieb",6: "urlaub",7: "party","default":1},"WEB_ID":"SP 221"},
    C_MKR1_RAUMSOLLTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Raumsolltemperatur","REG":108,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.5,"MIN":10.0,"MAX":25.0,"WEB_ID":"SP 200","PF":Platform.NUMBER},
    C_MKR1_SOLLTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Solltemperatur","REG":109,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.5,"MIN":5.0,"MAX":65.0,"HA":C_MKR1_SOLLTEMPERATUR_HAND_AKTIV,"WEB_ID":"MP 66","PF":Platform.NUMBER},
    C_MKR1_SOLLTEMPERATUR_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Solltemperatur Hand-Aktiv","REG":110,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 66"},
    C_MKR1_MIN_RUECKLAUFTEMPERATUR_KUEHLEN: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 min Rücklauftemperatur Kühlen","REG":111,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":1.0,"MIN":15.0,"MAX":25.0,"WEB_ID":"SP 348","PF":Platform.NUMBER},
    C_MKR2_BETRIEBSART: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Betriebsart","REG":112,"DT":C_DT_UINT16,"VALUES":{0: "aus",1: "automatik",2: "kuehlen",3: "sommer",4: "dauerbetrieb",5: "absenkbetrieb",6: "urlaub",7: "party","default":1},"WEB_ID":"SP 244","PF":Platform.NUMBER},
    C_MKR2_RAUMSOLLTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Raumsolltemperatur","REG":113,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.5,"MIN":10.0,"MAX":25.0,"WEB_ID":"SP 223","PF":Platform.NUMBER},
    C_MKR2_SOLLTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Solltemperatur","REG":114,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.5,"MIN":5.0,"MAX":65.0,"HA":C_MKR2_SOLLTEMPERATUR_HAND_AKTIV,"WEB_ID":"MP 72","PF":Platform.NUMBER},
    C_MKR2_SOLLTEMPERATUR_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Solltemperatur Hand-Aktiv","REG":115,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 72"},
    C_MKR2_MIN_RUECKLAUFTEMPERATUR_KUEHLEN: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 min Rücklauftemperatur Kühlen","REG":116,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":1.0,"MIN":15.0,"MAX":25.0,"WEB_ID":"SP 352","PF":Platform.NUMBER},
    C_PV_ANFORDERUNG: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"PV Anforderung","REG":117,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"SP 436"},
    C_PV_HEIZEN_OFFSET: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"PV Heizen Offset","REG":118,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"K","STEP":0.1,"MIN":0.0,"MAX":10.0,"WEB_ID":"SP 437","PF":Platform.NUMBER},
    C_PV_KUEHLEN_OFFSET: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"PV Kuehlen Offset","REG":119,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"K","STEP":0.1,"MIN":0.0,"MAX":10.0,"WEB_ID":"SP 438","PF":Platform.NUMBER},
    C_PV_HEIZEN_OFFSET_MKR1: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"PV Heizen Offset MKR1","REG":120,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"K","STEP":0.1,"MIN":0.0,"MAX":10.0,"WEB_ID":"SP 453","PF":Platform.NUMBER},
    C_PV_KUEHLEN_OFFSET_MKR1: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"PV Kühlen Offset MKR1","REG":121,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"K","STEP":0.1,"MIN":0.0,"MAX":10.0,"WEB_ID":"SP 454","PF":Platform.NUMBER},
    C_PV_HEIZEN_OFFSET_MKR2: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"PV Heizen Offset MKR2","REG":122,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"K","STEP":0.1,"MIN":0.0,"MAX":10.0,"WEB_ID":"SP 455","PF":Platform.NUMBER},
    C_PV_KUEHLEN_OFFSET_MKR2: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"PV Kühlen Offset MKR2","REG":123,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"K","STEP":0.1,"MIN":0.0,"MAX":10.0,"WEB_ID":"SP 456","PF":Platform.NUMBER},
    C_WW_NORMAL_MAX: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"WW Normal Max","REG":124,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":1.0,"MIN":5.0,"MAX":65.0,"WEB_ID":"SP 347","PF":Platform.NUMBER},
    C_VORGABE_LEISTUNGSAUFNAHME: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Vorgabe Leistungsaufnahme","REG":125,"DT":C_DT_UINT16,"FAKTOR":1,"UNIT":"W","STEP":1,"MIN":0,"MAX":7000,"PF":Platform.NUMBER},   #MAX-Wert hängt von der LEistung der WP ab -> konfigurierbar machen?
    C_VORGABE_VERDICHTERDREHZAHL: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Vorgabe Verdichterdrehzahl","REG":126,"RW":0,"DT":C_DT_INT16,"FAKTOR":1,"UNIT":"‰","STEP":1,"MIN":0,"MAX":1000,"PF":Platform.NUMBER},  #!! DARF NICHT BESCHRIEBEN WERDEN
    C_EXT_ANFORDERUNG: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Ext. Anforderung","REG":127,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 27"},
    C_ENTSTOEREN: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Entstören","REG":128,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"SP 14"},
    C_AUSSENTEMPERATUR_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Aussentemperatur Handwert","REG":129,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.1,"MIN":-49.9,"MAX":60.0,"HA":C_AUSSENTEMPERATUR_HAND_AKTIV,"WEB_ID":"MP 0","PF":Platform.NUMBER},
    C_AUSSENTEMPERATUR_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Aussentemperatur Hand-Aktiv","REG":130,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 0"},
    C_PUFFERTEMPERATUR_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Puffertemperatur Handwert","REG":131,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.1,"MIN":5.0,"MAX":60.0,"HA":C_PUFFERTEMPERATUR_HAND_AKTIV,"WEB_ID":"MP 5","PF":Platform.NUMBER},
    C_PUFFERTEMPERATUR_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Puffertemperatur Hand-Aktiv","REG":132,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 5"},
    C_BRAUCHWASSERTEMPERATUR_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Brauchwassertemperatur Handwert","REG":133,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.1,"MIN":5.0,"MAX":60.0,"HA":C_BRAUCHWASSERTEMPERATUR_HAND_AKTIV,"WEB_ID":"MP 2","PF":Platform.NUMBER},
    C_BRAUCHWASSERTEMPERATUR_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Brauchwassertemperatur Hand-Aktiv","REG":134,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 2"},
    C_HKR_HEIZGRENZE: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"HKR Heizgrenze","REG":135,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","Step": 1.0, "MIN":5.0,"MAX":30.0,"WEB_ID":"SP 76","PF":Platform.NUMBER},
    C_HKR_RUECKLAUFSOLL_BEI_HEIZGRENZE: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"HKR Rücklaufsoll bei Heizgrenze","REG":136,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 80","PF":Platform.NUMBER},
    C_HKR_RUECKLAUFSOLL_BEI_0_C: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"HKR Rücklaufsoll bei 0°C","REG":137,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 81","PF":Platform.NUMBER},
    C_HKR_RUECKLAUFSOLL_BEI_15_C: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"HKR Rücklaufsoll bei -15°C","REG":138,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 82","PF":Platform.NUMBER},
    C_MKR1_HEIZGRENZE: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Heizgrenze","REG":139,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","Step": 1, "MIN":5.0,"MAX":30.0,"WEB_ID":"SP 205","PF":Platform.NUMBER},
    C_MKR1_RUECKLAUFSOLL_BEI_HEIZGRENZE: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Rücklaufsoll bei Heizgrenze","REG":140,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 209","PF":Platform.NUMBER},
    C_MKR1_RUECKLAUFSOLL_BEI_0_C: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Rücklaufsoll bei 0°C","REG":141,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 210","PF":Platform.NUMBER},
    C_MKR1_RUECKLAUFSOLL_BEI_15_C: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR1 Rücklaufsoll bei -15°C","REG":142,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 211","PF":Platform.NUMBER},
    C_MKR2_HEIZGRENZE: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Heizgrenze","REG":143,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","Step": 1, "MIN":5.0,"MAX":30.0,"WEB_ID":"SP 228","PF":Platform.NUMBER},
    C_MKR2_RUECKLAUFSOLL_BEI_HEIZGRENZE: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Rücklaufsoll bei Heizgrenze","REG":144,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 232","PF":Platform.NUMBER},
    C_MKR2_RUECKLAUFSOLL_BEI_0_C: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Rücklaufsoll bei 0°C","REG":145,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 233","PF":Platform.NUMBER},
    C_MKR2_RUECKLAUFSOLL_BEI_15_C: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"MKR2 Rücklaufsoll bei -15°C","REG":146,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","MIN":15.0,"MAX":35.0,"WEB_ID":"SP 234","PF":Platform.NUMBER},
    C_2_STUFE_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"2. Stufe Handwert","REG":147,"DT":C_DT_INT16,"SWITCH":{"off":0,"on":1},"HA":C_2_STUFE_HAND_AKTIV,"WEB_ID":"MP 49"},
    C_2_STUFE_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"2. Stufe Hand-Aktiv","REG":148,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 49"},
    C_EVU_SPERRE_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"EVU Sperre Handwert","REG":149,"DT":C_DT_INT16,"SWITCH":{"off":0,"on":1},"HA":C_EVU_SPERRE_HAND_AKTIV,"WEB_ID":"MP 37"},
    C_EVU_SPERRE_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"EVU Sperre Hand-Aktiv","REG":150,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 37"},
    # Raumbediengerät TF22
    C_TF22_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"TF22 Handwert","REG":151,"DT":C_DT_INT16,"FAKTOR":1,"STEP":1.0,"MIN":-80.0,"MAX":80.0,"WEB_ID":"MP 10","HA":C_TF22_HAND_AKTIV,"PF":Platform.NUMBER},
    C_TF22_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"TF22 Hand-Aktiv","REG":152,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 10"},
}

ENTITY_PATCHES = [
    {
        "min_version": "2.2.0.1",
        "remove": [
            C_MKR1_RUECKLAUFTEMPERATUR,
            C_MKR2_RUECKLAUFTEMPERATUR,
            C_WMZ_BRAUCHWASSER,
            C_STROMZAEHLER_BRAUCHWASSER,
        ],
        "update": {
            C_WMZ_DURCHFLUSS: {"FAKTOR": 0.1/60,},
            C_N_SOLL_VERDICHTER: {"FAKTOR": 0.1, "UNIT": "%",},
            C_EXPANSIONSVENTIL: {"UNIT": "%",},
            C_TF22_HANDWERT: {"FAKTOR": 0.1, "UNIT": "°C",},
        },
        "add": {
            C_FWS_ZIELTEMPERATUR: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"FWS Zieltemperatur","REG":153,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":1.0,"MIN":5.0,"MAX":65.0,"WEB_ID":"SP 87","PF":Platform.NUMBER},
            C_RAUMFUEHLER_1_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Raumfühler 1 Handwert","REG":154,"DT":C_DT_INT16,"FAKTOR":0.1,"UNIT":"°C","STEP":0.1,"MIN":-49.9,"MAX":60.0,"HA":C_RAUMFUEHLER_1_HAND_AKTIV,"WEB_ID":"MP 16","PF":Platform.NUMBER},
            C_RAUMFUEHLER_1_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Raumfühler 1 Hand-Aktiv","REG":155,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 16"},
            C_ZIRKULATIONSPUMPE_WW_HANDWERT: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Zirkulationspumpe WW Handwert","REG":156,"DT":C_DT_INT16,"SWITCH":{"off":0,"on":1},"HA":C_ZIRKULATIONSPUMPE_WW_HAND_AKTIV,"WEB_ID":"MP 29"},
            C_ZIRKULATIONSPUMPE_WW_HAND_AKTIV: {"RT": C_REG_TYPE_HOLDING_REGISTERS,"NAME":"Zirkulationspumpe WW Hand-Aktiv","REG":157,"DT":C_DT_UINT16,"SWITCH":{"off":0,"on":1},"WEB_ID":"MP 29"},
        },
    },
]

# ------------------------------------------------------------
# Klassendefinitionen für die unterschiedlichen Entitätstypen
# ------------------------------------------------------------


@dataclass
class MyBinarySensorEntityDescription(BinarySensorEntityDescription):
    """A class that describes Modbus binarysensor entities."""


@dataclass
class MySensorEntityDescription(SensorEntityDescription):
    """A class that describes Modbus sensor entities."""


@dataclass
class MyBinaryEntityDescription(BinarySensorEntityDescription):
    """A class that describes Modbus binary entities."""

    # Hinweis: Falls echte Schalter-Entities verwendet werden, ggf. SwitchEntityDescription verwenden.


@dataclass
class MySelectEntityDescription(SelectEntityDescription):
    """A class that describes Modbus select entities."""

    default_select_option: str | None = None
    setter_function: Callable[[Any, str], Awaitable[None]] | None = None


@dataclass
class MyClimateEntityDescription(ClimateEntityDescription):
    """A class that describes Modbus climate sensor entities."""

    min_value: float = None
    max_value: float = None
    step: float = None
    hvac_modes: list[str] = None
    temperature_unit: str = "°C"
    supported_features: ClimateEntityFeature = ClimateEntityFeature.TARGET_TEMPERATURE


@dataclass
class MyNumberEntityDescription(NumberEntityDescription):
    """A class that describes Modbus number entities."""

    mode: str = "slider"
    initial: float = None
    editable: bool = True


BINARYSENSOR_TYPES: dict[str, MyBinarySensorEntityDescription] = {}
SENSOR_TYPES: dict[str, MySensorEntityDescription] = {}
SELECT_TYPES: dict[str, MySelectEntityDescription] = {}
CLIMATE_TYPES: dict[str, MyClimateEntityDescription] = {}
NUMBER_TYPES: dict[str, MyNumberEntityDescription] = {}
BINARY_TYPES: dict[str, MyBinaryEntityDescription] = {}


# --------------------------------------------------------------------
# Hilfsfunktionen zur Klassifizierung der Eintitäten aus ENTITIES_DICT
# --------------------------------------------------------------------

TEMP_UNITS = {"°C", "K"}


def is_entity_readonly(props: Dict[str, Any]) -> bool:
    """Input-Register oder Discrete-Inputs oder Read-Only: RW=0)"""
    reg_type = get_entity_type(props)
    return reg_type in [C_REG_TYPE_INPUT_REGISTERS, C_REG_TYPE_DISCRETE_INPUTS] or (props.get("RW") == 0)


def is_entity_readwrite(props: Dict[str, Any]) -> bool:
    """Beschreibbar, Read-Only: Beschreibbar (WR=None)"""
    reg_type = get_entity_type(props)
    return reg_type in [C_REG_TYPE_HOLDING_REGISTERS, C_REG_TYPE_COILS]


def is_entity_switch(props: Dict[str, Any]) -> bool:
    reg_type = get_entity_type(props)
    return (reg_type in [C_REG_TYPE_DISCRETE_INPUTS, C_REG_TYPE_COILS]) or (
        get_entity_switch(props) is not None
    )


def is_entity_select(props: Dict[str, Any]) -> bool:
    return props.get("VALUES") not in (None, {})


def is_entity_climate(props: Dict[str, Any]) -> bool:
    return get_entity_unit(props) in TEMP_UNITS and get_entity_platform(props) in {
        None,
        Platform.CLIMATE,
    }


def is_entity_number(props: Dict[str, Any]) -> bool:
    return get_entity_platform(props) == Platform.NUMBER or not (
        is_entity_switch(props) or is_entity_select(props) or is_entity_climate(props)
    )


# -------------------------------------------------
# Hilfsfunktionen zum Lesen der Daten einer Entität
# -------------------------------------------------


def get_entity_type(props: Dict[str, Any]) -> int | None:
    return props.get("RT")


def get_entity_name(props: Dict[str, Any], default: str = None) -> str | None:
    return props.get("NAME", default)


def get_entity_unit(props: Dict[str, Any], default: str = None) -> str | None:
    return props.get("UNIT", default)


def get_entity_platform(props: Dict[str, Any], default: str = None) -> str | None:
    return props.get("PF", default)


def get_entity_min(props: Dict[str, Any]) -> float | None:
    return props.get("MIN", 0)


def get_entity_max(props: Dict[str, Any]) -> float | None:
    return props.get("MAX", 50.0)


def get_entity_step(props: Dict[str, Any]) -> float | None:
    return props.get("STEP", 0.1)


def get_entity_hvac_modes(
    props: Dict[str, Any], default: str = None
) -> list[str] | None:
    return props.get("HVAC_MODES") or default


def get_entity_switch(props: Dict[str, Any]) -> dict[str, int] | None:
    return props.get("SWITCH")


def get_entity_select(props: Dict[str, Any]) -> dict[Any, Any] | None:
    return props.get("VALUES")


def get_entity_select_values_and_default(
    props: dict[str, Any],
) -> tuple[list[str], str] | None:
    values = get_entity_select(props)
    default_index = values.get("default")
    select_map = {k: v for k, v in values.items() if k != "default"}
    return list(select_map.values()), select_map.get(default_index)


def get_entity_reg(
    props: Dict[str, Any],
) -> tuple[int | None, ModbusTcpClient.DATATYPE | None]:
    reg_type = get_entity_type(props)
    if reg_type in [C_REG_TYPE_COILS, C_REG_TYPE_DISCRETE_INPUTS]:
        dt = C_DT_BITS
    else:
        dt = props.get("DT")
    return props.get("REG"), dt


def get_entity_props(entity: str) -> dict:
    return ENTITIES_DICT[entity]


def get_entity_factor(props: Dict[str, Any]) -> float:
    return props.get("FAKTOR", 1.0)

def get_entity_ha(props: Dict[str, Any]) -> str | None:
    return props.get("HA")

def get_entity_webregler_id(props: Dict[str, Any]) -> str | None:
    return props.get("WEB_ID")


# --------------------------------------------------------------------------------
# Hilfsfunktionen zur Erstellen der aus ENTITIES_DICT abgeleiteten Datenstrukturen
# --------------------------------------------------------------------------------


def _classify_register(props: Dict[str, Any]) -> int | None:
    global \
        C_MIN_INPUT_REGISTER, \
        C_MAX_INPUT_REGISTER, \
        C_MIN_HOLDING_REGISTER, \
        C_MAX_HOLDING_REGISTER, \
        C_MIN_COILS, \
        C_MAX_COILS, \
        C_MIN_DISCRETE_INPUTS, \
        C_MAX_DISCRETE_INPUTS

    reg_type = get_entity_type(props)
    reg_from, dt = get_entity_reg(props)
    if reg_from is None or dt is None:
        return None
    if dt == ModbusTcpClient.DATATYPE.BITS:
        sizeofdt = 1
    else:
        sizeofdt = dt.value[1]
    reg_to = reg_from + sizeofdt - 1

    match reg_type:
        case thismodule.C_REG_TYPE_DISCRETE_INPUTS:
            C_MIN_DISCRETE_INPUTS = min(reg_from, C_MIN_DISCRETE_INPUTS)
            C_MAX_DISCRETE_INPUTS = max(reg_to, C_MAX_DISCRETE_INPUTS)
        case thismodule.C_REG_TYPE_COILS:
            C_MIN_COILS = min(reg_from, C_MIN_COILS)
            C_MAX_COILS = max(reg_to, C_MAX_COILS)
        case thismodule.C_REG_TYPE_INPUT_REGISTERS:
            C_MIN_INPUT_REGISTER = min(reg_from, C_MIN_INPUT_REGISTER)
            C_MAX_INPUT_REGISTER = max(reg_to, C_MAX_INPUT_REGISTER)
        case thismodule.C_REG_TYPE_HOLDING_REGISTERS:
            C_MIN_HOLDING_REGISTER = min(reg_from, C_MIN_HOLDING_REGISTER)
            C_MAX_HOLDING_REGISTER = max(reg_to, C_MAX_HOLDING_REGISTER)

    if is_entity_readonly(props):
        if is_entity_switch(props):
            """Nicht beschreibbar, Schalter (SWITCH!=None)."""
            return MyBinarySensorEntityDescription  # C_REGISTERCLASS_BINARY_SENSOR
        elif is_entity_select(props):
            """Nicht beschreibbar, Auswahl (VALUES enthält mindestens ein Element)."""
            return MySensorEntityDescription  # C_REGISTERCLASS_SELECT_ENTITY
        else:
            """Nicht beschreibbar, kein Schalter (SWITCH=None)."""
            return MySensorEntityDescription  # C_REGISTERCLASS_SENSOR
    else:
        if is_entity_switch(props):
            """Beschreibbar, Schalter (SWITCH!=None)."""
            return MyBinaryEntityDescription  # C_REGISTERCLASS_BINARY_ENTITY
        elif is_entity_select(props):
            """Beschreibbar, Auswahl (VALUES enthält mindestens ein Element)."""
            return MySelectEntityDescription  # C_REGISTERCLASS_SELECT_ENTITY
        elif is_entity_climate(props):
            """Beschreibbar, Nur Temperatureinheiten (°C oder K) zulassen"""
            return MyClimateEntityDescription  # C_REGISTERCLASS_CLIMATE_ENTITY
        else:
            """Beschreibbar, kein Schalter (SWITCH=None), keine Auswahl (VALUES ist None), Einheit optional, aber nicht °C oder K."""
            return MyNumberEntityDescription  # C_REGISTERCLASS_NUMBER_ENTITY


def _unit_mapping(
    unit: Optional[str],
) -> tuple[Optional[str], Optional[SensorDeviceClass], Optional[SensorStateClass]]:
    """
    Mappt unsere Einheit (UNIT) auf Home-Assistant native_unit_of_measurement + device_class + state_class.
    Für unbekannte Einheiten bleiben Klassen leer.
    """
    if unit is None:
        return None, None, None

    u = unit.strip()
    # Temperatur
    if u == "°C":
        return (
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
        )
    if u == "K":
        # Selten als absolute Temperatur; hier i. d. R. Offsets -> als °C nicht sinnvoll.
        return (
            UnitOfTemperature.KELVIN,
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
        )

    # Druck
    if u.lower() in {"bar"}:
        return (
            UnitOfPressure.BAR,
            SensorDeviceClass.PRESSURE,
            SensorStateClass.MEASUREMENT,
        )

    # Energie & Leistung
    if u.lower() in {"kwh", "kW/h".lower()}:  # akzeptiere beide Schreibweisen
        return (
            UnitOfEnergy.KILO_WATT_HOUR,
            SensorDeviceClass.ENERGY,
            SensorStateClass.TOTAL_INCREASING,
        )
    if u.lower() in {"w"}:
        return UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT
    if u.lower() in {"kw"}:
        return (
            UnitOfPower.KILO_WATT,
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
        )

    # Volumenstrom
    if u.lower() in {"l/min", "l/Min", "l pro min"}:
        return "l/min", None, SensorStateClass.MEASUREMENT
    if u.lower() in {"m³/h"}:
        return "m³/h", None, SensorStateClass.MEASUREMENT

    # Drehzahl / Stellgrad
    if u == "‰":
        return "‰", None, SensorStateClass.MEASUREMENT
    if u == "%":
        return "%", None, SensorStateClass.MEASUREMENT

    # PPM, Anteil
    if u == "ppm":
        return "ppm", None, SensorStateClass.MEASUREMENT

    # Zeit/Dauer
    if u.lower() in {"h", "std"}:
        return "h", SensorDeviceClass.DURATION, SensorStateClass.TOTAL_INCREASING
    if u.lower() in {"min"}:
        return "min", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT
    if u.lower() in {"s", "sek", "sec"}:
        return "s", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT

    # Restdauer
    if u.lower() in {"d", "days"}:
        return "d", SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT

    # Fallback: nutze Roh-Einheit ohne Device-Class
    return u, None, SensorStateClass.MEASUREMENT


def build_entities_dict(version: str | None) -> dict[str, dict]:
    entities = deepcopy(BASE_ENTITIES_DICT)

    if not version:
        _LOGGER.debug("Keine Versionsnummer erkannt. Verwende Basis-Konfiguration.")
        return entities
    else:
        _LOGGER.debug(f"Version {version} erkannt. Suche nach Patches...")

    try:
        current = Version(version)
    except InvalidVersion:
        return entities

    for patch in ENTITY_PATCHES:
        min_version = patch["min_version"]
        if current >= Version(min_version):
            _LOGGER.debug(f"Wende Patch {min_version} an.")
            for key in patch.get("remove", []):
                entities.pop(key, None)

            for key, changes in patch.get("update", {}).items():
                if key not in entities:
                    continue

                for prop, value in changes.items():
                    if value is None:
                        entities[key].pop(prop, None)
                    else:
                        entities[key][prop] = value

            entities.update(patch.get("add", {}))

    return entities

def init(detected_version:str|None = None, force: bool = False):
    global \
        ENTITIES_DICT, \
        BINARYSENSOR_TYPES, \
        SENSOR_TYPES, \
        SELECT_TYPES, \
        CLIMATE_TYPES, \
        NUMBER_TYPES, \
        BINARY_TYPES, \
        C_MIN_INPUT_REGISTER, \
        C_MAX_INPUT_REGISTER, \
        C_MIN_HOLDING_REGISTER, \
        C_MAX_HOLDING_REGISTER, \
        C_MIN_COILS, \
        C_MAX_COILS, \
        C_MIN_DISCRETE_INPUTS, \
        C_MAX_DISCRETE_INPUTS


    _LOGGER.info(
        "****************************************  initalizing ***************************************"
    )

    C_MIN_INPUT_REGISTER = sys.maxsize
    C_MAX_INPUT_REGISTER = -1
    C_MIN_HOLDING_REGISTER = sys.maxsize
    C_MAX_HOLDING_REGISTER = -1
    C_MIN_COILS = sys.maxsize
    C_MAX_COILS = -1
    C_MIN_DISCRETE_INPUTS = sys.maxsize
    C_MAX_DISCRETE_INPUTS = -1

    BINARYSENSOR_TYPES = {}
    SENSOR_TYPES = {}
    SELECT_TYPES = {}
    CLIMATE_TYPES = {}
    NUMBER_TYPES = {}
    BINARY_TYPES = {}
    ha_entities = []
    # Companion entities referenced via "HA" are normally kept internal and therefore
    # do not become visible Home Assistant entities. That model is problematic for
    # Rücklaufsolltemperatur: writing REG 102 only makes sense together with REG 103
    # (Hand-Aktiv), and without a visible way to switch REG 103 back to 0 the user
    # cannot reliably return that path to Automatik from HA. For now we expose only
    # this one companion entity as the narrowest fix for the known 102/103 issue
    # discussed in mbuchber/ha_heliotherm#68, without flooding HA with every other
    # hand_aktiv helper before their UX/behavior is reviewed.
    exposed_companion_entities = {C_RUECKLAUFSOLLTEMPERATUR_HAND_AKTIV}

    ENTITIES_DICT = build_entities_dict(detected_version)

    for c_key, props in ENTITIES_DICT.items():
        entity_key: str = c_key
        name: str = get_entity_name(props, entity_key)
        registerclass = _classify_register(props)

        entity_ha = get_entity_ha(props)
        if entity_ha:
            ha_entities.append(entity_ha)

        if (entity_key not in ha_entities) or (entity_key in exposed_companion_entities):

            match registerclass:
                case thismodule.MySensorEntityDescription:
                    unit, device_class, state_class = _unit_mapping(get_entity_unit(props))
                    _LOGGER.debug(f"Sensor {entity_key}: {name}, Einheit {unit}")
                    SENSOR_TYPES[entity_key] = registerclass(
                        name=name,
                        key=entity_key,
                        translation_key=entity_key,
                        native_unit_of_measurement=unit,
                        device_class=device_class,
                        state_class=state_class,
                    )

                case thismodule.MyBinarySensorEntityDescription:
                    _LOGGER.debug(f"Binär-Sensor {entity_key}: {name}")
                    BINARYSENSOR_TYPES[entity_key] = registerclass(
                        name=name,
                        key=entity_key,
                        translation_key=entity_key,
                    )

                case thismodule.MyClimateEntityDescription:
                    #key = f"{C_PREFIX_CLIMATE}_{entity_key}"
                    min_value=get_entity_min(props)
                    max_value=get_entity_max(props)
                    step=get_entity_step(props)
                    hvac_modes=get_entity_hvac_modes(props)
                    temperature_unit=get_entity_unit(props)
                    _LOGGER.debug(
                        f"Temperatur-Stellwert {entity_key}: {name}, {min_value}-{max_value}{temperature_unit} in {step}-er Schritten"
                    )
                    CLIMATE_TYPES[entity_key] = registerclass(
                        name=name,
                        key=entity_key,
                        translation_key=entity_key,
                        min_value=min_value,
                        max_value=max_value,
                        step=step,
                        hvac_modes=hvac_modes,
                        temperature_unit=temperature_unit,
                        supported_features=props.get(
                            "FEATURES", ClimateEntityFeature.TARGET_TEMPERATURE
                        ),
                    )

                case thismodule.MyNumberEntityDescription:
                    #key = f"{C_PREFIX_NUMBER}_{entity_key}"
                    min_value=get_entity_min(props)
                    max_value=get_entity_max(props)
                    step=get_entity_step(props)
                    unit_of_measurement=get_entity_unit(props)
                    _LOGGER.debug(
                        f"Numerischer Stellwert {entity_key}: {name}, {min_value}-{max_value}{unit_of_measurement} in {step}-er Schritten"
                    )
                    NUMBER_TYPES[entity_key] = registerclass(
                        name=name,
                        key=entity_key,
                        translation_key=entity_key,
                        min_value=min_value,
                        max_value=max_value,
                        step=step,
                        unit_of_measurement=unit_of_measurement,
                        editable=is_entity_readwrite(props),
                        mode="box"
                    )

                case thismodule.MyBinaryEntityDescription:
                    #key = f"{C_PREFIX_SWITCH}_{entity_key}"
                    _LOGGER.debug(f"Schalter {entity_key}: {name}")
                    BINARY_TYPES[entity_key] = registerclass(
                        name=name,
                        key=entity_key,
                        translation_key=entity_key,
                    )

                case thismodule.MySelectEntityDescription:
                    #key = f"{C_PREFIX_SELECT}_{entity_key}"
                    values, default = get_entity_select_values_and_default(props)
                    _LOGGER.debug(
                        f"Auswahl-Entität {entity_key}: {name}, Werte-Bereich: {values}, Default: {default}"
                    )
                    SELECT_TYPES[entity_key] = registerclass(
                        name=name,
                        key=entity_key,
                        translation_key=entity_key,
                        options=values,
                        default_select_option=default,
                    )

                case _:
                    _LOGGER.warning(f"Unbekannter Entitätstyp {entity_key}: {props}")
                    print(f"Sensor konnte nicht zugeordnet werden: {entity_key}/{name}")
        else:
            _LOGGER.debug(f"Hand-Aktiv-Schalter {entity_key} wird nur intern genutzt und nicht in HA bereitgestellt.")

    _LOGGER.debug(
        f"Status-Register (r/o) von {C_MIN_INPUT_REGISTER} bis {C_MAX_INPUT_REGISTER}"
    )
    _LOGGER.debug(
        f"Discrete Inputs-Register (r/o) von {C_MIN_DISCRETE_INPUTS} bis {C_MAX_DISCRETE_INPUTS}"
    )
    _LOGGER.debug(f"- {len(SENSOR_TYPES)} Sensoren")
    _LOGGER.debug(f"- {len(BINARYSENSOR_TYPES)} Binär-Sensoren")
    _LOGGER.debug(
        f"Holding-Register (r/w) von {C_MIN_HOLDING_REGISTER} bis {C_MAX_HOLDING_REGISTER}"
    )
    _LOGGER.debug(f"Coils (r/w) von {C_MIN_COILS} bis {C_MAX_COILS}")
    _LOGGER.debug(f"- {len(SELECT_TYPES)} Auswahl-Entitäten")
    _LOGGER.debug(f"- {len(BINARY_TYPES)} Schalter")
    _LOGGER.debug(f"- {len(CLIMATE_TYPES)} Temperatur-Stellwerte")
    _LOGGER.debug(f"- {len(NUMBER_TYPES)} Numerische Stellwerte")
    _LOGGER.info(
        "****************************************  initalized ****************************************"
    )

