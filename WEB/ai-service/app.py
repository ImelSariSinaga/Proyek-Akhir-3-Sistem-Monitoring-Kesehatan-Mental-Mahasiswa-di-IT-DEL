from flask import Flask, jsonify
import json
import os
import logging
from services.translate_service import translate_id_to_en, translate_en_to_id
from services.summary_service import summarize_text_en
from services.emotion_service import process_emotion

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route("/analyze", methods=["GET"])
def analyze():
    try:
        # Gunakan absolute path untuk data.json
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "data.json")
        
        # baca data.json
        with open(file_path, "r", encoding="utf-8") as f:
            data_list = json.load(f)
            
        logger.info(f"Successfully loaded {len(data_list)} items from data.json")
        
    except FileNotFoundError:
        logger.error("data.json not found")
        return jsonify({"error": "data.json not found"}), 404
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in data.json: {str(e)}")
        return jsonify({"error": "Invalid JSON in data.json"}), 400
    except Exception as e:
        logger.error(f"Unexpected error reading data.json: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    results = []

    for idx, data in enumerate(data_list):
        text_id = data.get("note")
        user_id = data.get("userId")
        emosi_kode = data.get("emosi_kode")

        if not text_id:
            logger.warning(f"Skipping item {idx}: no note field")
            continue

        logger.info(f"Processing user {user_id or 'unknown'}...")

        try:
            # Step 1: translate ID -> EN
            logger.debug(f"Translating text from ID to EN: {text_id[:50]}...")
            text_en = translate_id_to_en(text_id)
            logger.debug(f"Translated to EN: {text_en[:50]}...")
            
            # Step 2: summarize in English
            logger.debug("Summarizing text...")
            summary_en = summarize_text_en(text_en)
            logger.debug(f"Summarized: {summary_en[:50]}...")
            
            # Step 3: translate back EN -> ID
            logger.debug("Translating summary back to ID...")
            summary_id = translate_en_to_id(summary_en)
            
        except Exception as e:
            logger.error(f"Error in translation/summary for user {user_id}: {str(e)}")
            summary_id = f"Error dalam pemrosesan: {str(e)}"

        # Prepare base result
        result = {
            "user_id": user_id,
            "ringkasan": summary_id
        }

        # Process emotion if both user_id and emosi_kode exist
        if user_id is not None and emosi_kode is not None:
            try:
                logger.info(f"Processing emotion for user {user_id} with code {emosi_kode}")
                emotion_result = process_emotion(user_id, emosi_kode)
                
                # emotion_result sudah berupa dictionary dari service Anda
                result.update(emotion_result)
                    
            except Exception as e:
                logger.error(f"Error processing emotion for user {user_id}: {str(e)}")
                result["emotion_error"] = f"Gagal memproses emosi: {str(e)}"

        results.append(result)

    logger.info(f"Successfully processed {len(results)} items")
    return jsonify(results)


@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint untuk mengecek kesehatan service"""
    try:
        # Test translation service
        test_text = "test"
        translate_id_to_en(test_text)
        translate_en_to_id(test_text)
        
        # Test summary service
        summarize_text_en("This is a test text for summarization.")
        
        # Test emotion service (dengan dummy data)
        process_emotion("test_user", 4)  # kode 4 = netral
        
        services_status = {
            "translate": "available",
            "summary": "available", 
            "emotion": "available"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        services_status = {
            "translate": "unavailable",
            "summary": "unavailable",
            "emotion": "unavailable",
            "error": str(e)
        }
    
    return jsonify({
        "status": "healthy" if all(v == "available" for v in services_status.values() if isinstance(v, str)) else "degraded",
        "services": services_status,
        "device": str(config.device)  # Menampilkan device yang digunakan (cuda/cpu)
    })


@app.route("/emotion/<int:user_id>", methods=["GET"])
def get_user_emotion(user_id):
    """Endpoint untuk mendapatkan emotional score user tertentu"""
    from services.emotion_service import user_emotional_scores
    
    if user_id in user_emotional_scores:
        return jsonify({
            "user_id": user_id,
            "emotional_data": user_emotional_scores[user_id]
        })
    else:
        return jsonify({"error": "User not found"}), 404


@app.route("/reset", methods=["POST"])
def reset_emotion_scores():
    """Endpoint untuk mereset semua emotional scores (untuk testing)"""
    from services.emotion_service import user_emotional_scores
    user_emotional_scores.clear()
    return jsonify({"message": "All emotion scores reset successfully"})


if __name__ == "__main__":
    # Import config untuk akses device
    import config
    logger.info(f"Starting application on device: {config.device}")
    logger.info(f"Available services: Translation (ID-EN, EN-ID), Summarization, Emotion")
    
    app.run(debug=True, host="0.0.0.0", port=5000)