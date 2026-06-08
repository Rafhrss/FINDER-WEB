import json
import logging
from django.conf import settings
import google.generativeai as genai

logger = logging.getLogger(__name__)

# Configure Gemini
if getattr(settings, "GEMINI_API_KEY", None):
    genai.configure(api_key=settings.GEMINI_API_KEY)


def extract_keywords_with_gemini(query: str) -> dict:
    """
    Extracts search intent and keywords from a natural language query using Gemini.
    """
    if getattr(settings, "MOCK_AI_SERVICES", False):
        import time
        time.sleep(1) # Simulasi loading
        return {"keywords": query.split()}
        
    if not getattr(settings, "GEMINI_API_KEY", None):
        return {"keywords": query.split()}

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = f"""
        Anda adalah asisten AI ekstraksi kata kunci.
        Pengguna memasukkan kueri pencarian barang hilang/ditemukan: "{query}"
        
        Tugas Anda adalah mengekstrak kata kunci utama menjadi format JSON sederhana.
        Hanya kembalikan objek JSON dengan SATU key "keywords" yang berisi ARRAY dari kata-kata penting (misalnya nama barang, merk, ciri fisik) yang cocok untuk pencarian database. JANGAN masukkan kata sambung atau kata depan.
        
        Contoh:
        Query: "tolong carikan tas punggung hitam saya yang tertinggal di kantin kemarin"
        Output JSON: {{"keywords": ["tas", "punggung", "hitam", "kantin"]}}
        
        Query: "saya menemukan kunci mobil honda di area parkir rektorat"
        Output JSON: {{"keywords": ["kunci", "mobil", "honda", "parkir"]}}
        
        Kembalikan HANYA JSON murni tanpa markdown formatter.
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            ),
        )
        
        result = json.loads(response.text)
        return result
    except Exception as e:
        logger.error(f"Error extracting keywords with Gemini: {e}")
        return {"keywords": query.split()}


def analyze_matches_with_gemini(query: str, reports: list) -> list:
    """
    Analyzes how well database records match the user's natural language query using Gemini.
    """
    if not reports:
        return []
        
    if getattr(settings, "MOCK_AI_SERVICES", False):
        import time
        import random
        time.sleep(1.5) # Simulasi loading AI
        for report in reports:
            report.match_percentage = random.randint(15, 60)
            report.justification = "[MOCK MODE] Ini adalah analisis bohongan untuk menghemat kuota API saat development. Karena ini mock, skor selalu rendah (15-60%)."
        return reports
        
    if not getattr(settings, "GEMINI_API_KEY", None):
        return reports

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        reports_data = [
            {
                "id": str(r.id),
                "title": r.title,
                "description": r.description,
                "location": r.location,
                "status": r.get_status_display()
            } for r in reports
        ]
        
        prompt = f"""
        Anda adalah asisten AI untuk CampusTracer (Lost & Found).
        Pengguna mencari barang dengan deskripsi alami: "{query}"
        
        Berikut adalah barang dari database yang ditemukan melalui pencarian keyword:
        {json.dumps(reports_data, indent=2)}
        
        Tugas Anda:
        1. Evaluasi seberapa cocok setiap barang dengan deskripsi asli pengguna (berikan match_percentage dari 0 hingga 100).
           PANDUAN SKOR STRICT:
           - 90-100%: Sangat identik (jenis barang, warna, dan ciri-ciri khusus sama persis).
           - 70-89%: Cukup cocok (jenis barang sama, tapi ada 1 atau 2 detail seperti warna yang kurang spesifik/berbeda).
           - 40-69%: Kurang cocok (hanya 1 kata yang mirip, atau jenis barang utamanya berbeda sama sekali).
           - 0-39%: Tidak cocok (salah sasaran).
           SANGAT PENTING: Jangan pernah memberikan skor di atas 80% jika warna atau jenis barang spesifiknya berbeda!
        2. Berikan "justification" singkat (maksimal 2 kalimat dalam bahasa Indonesia) yang jujur mengapa ini cocok atau kurang cocok.
        
        Kembalikan hasilnya DALAM FORMAT JSON array persis seperti ini:
        [
          {{
            "id": "UUID_BARANG",
            "match_percentage": 85,
            "justification": "Alasan singkat."
          }}
        ]
        """
        
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            ),
        )
        
        analysis_list = json.loads(response.text)
        
        # Combine analysis with original report objects
        results = []
        for report in reports:
            # Find matching analysis by stringified UUID
            report_id_str = str(report.id)
            match_data = next((item for item in analysis_list if str(item.get("id")) == report_id_str), None)
            
            if match_data:
                # Add dynamic attributes to the report object for the template to use
                report.match_percentage = match_data.get("match_percentage", 0)
                report.justification = match_data.get("justification", "")
            else:
                report.match_percentage = 0
                report.justification = ""
                
            results.append(report)
            
        # Sort by match percentage
        results.sort(key=lambda x: getattr(x, 'match_percentage', 0), reverse=True)
        return results

    except Exception as e:
        logger.error(f"Error analyzing matches with Gemini: {e}")
        error_msg = "Maaf, sistem AI sedang terlalu sibuk (Limit Kuota API). Silakan coba lagi dalam satu menit." if "429" in str(e) else "Terjadi kesalahan saat memproses data AI."
        
        # Tambahkan error state ke setiap report agar card tetap menampilkan UI AI
        for report in reports:
            report.match_percentage = "???"
            report.justification = error_msg
            
        return reports
