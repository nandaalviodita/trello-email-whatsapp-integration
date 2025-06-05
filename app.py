from flask import Flask, request, jsonify
import logging
from trello_api import get_all_cards
from selenium_whatsapp import init_driver, kirim_pesan, buka_chat_me
from email_sender import send_email
from config import NOMOR_WHATSAPP

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

driver = None

@app.before_first_request
def setup_driver():
    global driver
    driver = init_driver()
    buka_chat_me(driver)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info("Webhook diterima: %s", data)

    try:
        pesan = get_all_cards()
        kirim_pesan(driver, NOMOR_WHATSAPP, pesan)
        send_email("Update Permintaan Sambutan", pesan)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error saat memproses webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
