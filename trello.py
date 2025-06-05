import requests
import certifi
from config import API_KEY, TOKEN, BOARD_ID
from utils import convert_to_local_time
from datetime import datetime

def get_all_lists():
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists?key={API_KEY}&token={TOKEN}"
    response = requests.get(url, verify=certifi.where())
    return response.json() if response.status_code == 200 else []

def get_member_name(member_id):
    try:
        url = f"https://api.trello.com/1/members/{member_id}?key={API_KEY}&token={TOKEN}"
        response = requests.get(url, verify=certifi.where())
        if response.status_code == 200:
            full_name = response.json().get("fullName", "Tidak Diketahui")
            return full_name.split()[0] if full_name else "Tidak Diketahui"
    except Exception:
        pass
    return "Tidak Diketahui"

def get_all_cards_from_list(list_id):
    url = f"https://api.trello.com/1/lists/{list_id}/cards?key={API_KEY}&token={TOKEN}&fields=name,due,desc,idMembers,labels,templateCard"
    response = requests.get(url, verify=certifi.where())
    hasil = []

    if response.status_code == 200:
        cards = response.json()
        for card in cards:
            if card.get("templateCard", False):
                continue
            nama_acara = card.get("name", "").strip()
            if not nama_acara or "Nama Acara" in nama_acara:
                continue
            lokasi = card.get("desc", "").strip()
            if not lokasi or lokasi.lower() == "lokasi tidak tersedia":
                continue
            tanggal = card.get("due")
            if not tanggal:
                continue

            try:
                local_time = convert_to_local_time(tanggal)
                tanggal_obj = local_time.date()
                tanggal_str = local_time.strftime("%A, %d %B %Y")
                jam = local_time.strftime("%H.%M")
            except Exception:
                continue

            status = "⏳"
            if card.get("labels"):
                status = card["labels"][0]["name"]

            pic = "Tidak diketahui"
            if card.get("idMembers"):
                pic = ", ".join(get_member_name(mid) for mid in card["idMembers"])

            assignee = ""
            checklist_url = f"https://api.trello.com/1/cards/{card['id']}/checklists?key={API_KEY}&token={TOKEN}"
            checklist_res = requests.get(checklist_url, verify=certifi.where())
            if checklist_res.status_code == 200:
                checklist_data = checklist_res.json()
                checked_items = []
                for cl in checklist_data:
                    for item in cl["checkItems"]:
                        if item["state"] == "complete":
                            checked_items.append(item["name"])
                if checked_items:
                    assignee = ", ".join(checked_items)

            hasil.append({
                "judul": nama_acara,
                "lokasi": lokasi,
                "tanggal_obj": tanggal_obj,
                "tanggal_str": tanggal_str,
                "jam": jam,
                "status": status,
                "pic": pic,
                "assignee": assignee
            })

    return hasil

def get_all_cards():
    lists = get_all_lists()
    semua_kartu = []

    for lst in lists:
        if lst["name"] == "Permintaan Sambutan":
            semua_kartu += get_all_cards_from_list(lst["id"])

    if not semua_kartu:
        return "Tidak ada acara."

    semua_kartu.sort(key=lambda x: (x["tanggal_obj"], x["jam"]))

    pesan = "Permintaan Sambutan\n\n"
    tanggal_sekarang = None
    for kartu in semua_kartu:
        if kartu["tanggal_str"] != tanggal_sekarang:
            if tanggal_sekarang is not None:
                pesan += "\n"
            tanggal_sekarang = kartu["tanggal_str"]
            pesan += f"*{tanggal_sekarang}*\n"

        if kartu.get("assignee"):
            baris = f"{kartu['jam']} - {kartu['assignee']} *{kartu['judul']}* | {kartu['lokasi']} ({kartu['pic']}) {kartu['status']}\n"
        else:
            baris = f"{kartu['jam']} - *{kartu['judul']}* | {kartu['lokasi']} ({kartu['pic']}) {kartu['status']}\n"

        pesan += baris + "\n"

    keterangan = """
Keterangan :
✅ Diterima Sekpri / Satpol
📄 Membacakan Naskah saja
👔 Hanya Menghadiri
👤 Diwakilkan
👩🏻‍💻 Sedang dikerjakan
⚠ Ditunda
"""
    pesan += keterangan

    return pesan.strip()

def wait_for_card_edit_completion(card_id, last_card_status, timeout=60):
    import time
    start_time = time.time()
    while time.time() - start_time < timeout:
        url = f"https://api.trello.com/1/cards/{card_id}?key={API_KEY}&token={TOKEN}"
        response = requests.get(url, verify=certifi.where())
        if response.status_code == 200:
            card_data = response.json()
            if not card_data.get("isEditing", False):
                current_status = card_data.get("labels", [])
                if current_status != last_card_status.get(card_id, []):
                    last_card_status[card_id] = current_status
                    return True
        time.sleep(2)
    return False
