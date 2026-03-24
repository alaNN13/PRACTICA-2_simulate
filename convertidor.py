import os
import xml.etree.ElementTree as ET
import json
from xml.dom import minidom

def convertir_jflap():
    carpeta_actual = os.getcwd()
    archivos_jff = [f for f in os.listdir(carpeta_actual) if f.endswith('.jff')]
    
    if not archivos_jff:
        print("⚠️ No hay archivos .jff aquí.")
        return

    print(f"🚀 Encontrados {len(archivos_jff)} archivos JFLAP. Iniciando conversión...\n")

    for archivo in archivos_jff:
        nombre_base = archivo.replace('.jff', '')
        try:
            tree = ET.parse(archivo)
            root = tree.getroot()
            automaton = root.find('automaton')

            # 1. SALVAVIDAS: Si no es un autómata, lo saltamos elegantemente
            if automaton is None:
                tipo = root.find('type')
                tipo_str = tipo.text if tipo is not None else "Vacío/Desconocido"
                print(f"⏭️ SALTADO: {archivo} (Motivo: No contiene un autómata. Tipo detectado: {tipo_str})")
                continue

            # --- EXTRACCIÓN DE DATOS ---
            datos = {"estados": [], "alfabeto": [], "transiciones": [], "inicial": "", "finales": []}
            alfabeto_temp = set()

            for state in automaton.findall('state'):
                id_estado = state.get('id')
                nombre_estado = state.get('name')
                datos["estados"].append({"id": id_estado, "nombre": nombre_estado})
                if state.find('initial') is not None: datos["inicial"] = id_estado
                if state.find('final') is not None: datos["finales"].append(id_estado)

            for trans in automaton.findall('transition'):
                origen = trans.find('from').text
                destino = trans.find('to').text
                read_tag = trans.find('read')
                
                simbolo = read_tag.text if read_tag is not None and read_tag.text else "λ"
                if simbolo != "λ": alfabeto_temp.add(simbolo)
                
                datos["transiciones"].append({"de": origen, "a": destino, "lee": simbolo})

            datos["alfabeto"] = sorted(list(alfabeto_temp))

            # --- CREACIÓN DEL JSON ---
            with open(f"{nombre_base}.json", 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

            # --- CREACIÓN DEL XML ---
            xml_root = ET.Element("automata")
            ET.SubElement(xml_root, "tipo").text = "AFND" # Lo dejamos genérico
            
            alf = ET.SubElement(xml_root, "alfabeto")
            for s in datos["alfabeto"]: ET.SubElement(alf, "simbolo").text = s
            
            est_node = ET.SubElement(xml_root, "estados", inicial=datos["inicial"], finales=",".join(datos["finales"]))
            for e in datos["estados"]: ET.SubElement(est_node, "estado", id=e["id"], nombre=e["nombre"])
            
            trans_node = ET.SubElement(xml_root, "transiciones")
            for t in datos["transiciones"]: ET.SubElement(trans_node, "tr", origen=t["de"], destino=t["a"], leer=t["lee"])

            xml_str = minidom.parseString(ET.tostring(xml_root, 'utf-8')).toprettyxml(indent="  ")
            with open(f"{nombre_base}.xml", 'w', encoding='utf-8') as f:
                f.write(xml_str)
            
            print(f"✅ ÉXITO: {nombre_base} -> .json y .xml generados.")

        except ET.ParseError as e:
            # 2. SALVAVIDAS: Capturamos archivos corruptos como el 254.jff
            print(f"❌ ERROR CRÍTICO en {archivo}: El archivo está corrupto ({e}).")
        except Exception as e:
            print(f"❌ ERROR DESCONOCIDO con {archivo}: {e}")

if __name__ == '__main__':
    convertir_jflap()