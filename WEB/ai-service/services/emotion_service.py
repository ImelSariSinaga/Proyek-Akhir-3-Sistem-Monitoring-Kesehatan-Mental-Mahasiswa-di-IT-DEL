from config import EMOSI_SCORE_CHANGE, emosi_mapping

user_emotional_scores = {}

def hitung_emosional_score(score_sekarang, emosi_label):
    perubahan = EMOSI_SCORE_CHANGE.get(emosi_label, 0)
    score_baru = max(0, min(100, score_sekarang + perubahan))
    return score_baru

def process_emotion(userId, emosi_kode):
    emosi_label = emosi_mapping.get(emosi_kode, "tidak diketahui")

    if userId not in user_emotional_scores:
        user_emotional_scores[userId] = {"current_score": 100}

    current_score = user_emotional_scores[userId]["current_score"]
    new_score = hitung_emosional_score(current_score, emosi_label)

    user_emotional_scores[userId]["current_score"] = new_score

    return {
        "emosi_terdeteksi": emosi_label,
        "emotional_score_sebelum": current_score,
        "emotional_score_sesudah": new_score,
        "perubahan_score": new_score - current_score
    }