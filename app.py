import sys
sys.path.append(".")

import gradio as gr
import os
from src.voice.pipeline import transcribe, translate, speak

os.makedirs("outputs", exist_ok=True)

def atlas_process(audio, text_input, target_language):
    try:
        if audio is not None:
            result        = transcribe(audio)
            original_text = result["text"]
            detected_lang = result["language"]
            input_method  = "🎤 Voice"
        elif text_input and text_input.strip():
            original_text = text_input.strip()
            detected_lang = "en"
            input_method  = "⌨️ Text"
        else:
            return "❌ Please provide audio or text input.", "", "", None

        if detected_lang != "en":
            english_text = translate(
                original_text,
                src_lang=detected_lang,
                tgt_lang="eng_Latn"
            )
        else:
            english_text = original_text

        response_english = f"I understand. You said: {english_text}. ATLAS is here to help you."

        target_codes = {
            "Hindi":    ("hin_Deva", "hi"),
            "Arabic":   ("ara_Arab", "ar"),
            "Bengali":  ("ben_Beng", "bn"),
            "Urdu":     ("urd_Arab", "ur"),
            "French":   ("fra_Latn", "fr"),
            "German":   ("deu_Latn", "de"),
            "Spanish":  ("spa_Latn", "es"),
            "Russian":  ("rus_Cyrl", "ru"),
            "Turkish":  ("tur_Latn", "tr"),
            "Swahili":  ("swh_Latn", "sw"),
            "Tamil":    ("tam_Taml", "ta"),
            "Telugu":   ("tel_Telu", "te"),
            "Marathi":  ("mar_Deva", "mr"),
            "Gujarati": ("guj_Gujr", "gu"),
            "Punjabi":  ("pan_Guru", "pa"),
            "English":  ("eng_Latn", "en"),
        }

        nllb_code, tts_code = target_codes.get(
            target_language, ("eng_Latn", "en"))

        if target_language != "English":
            response_translated = translate(
                response_english,
                src_lang="en",
                tgt_lang=nllb_code
            )
        else:
            response_translated = response_english

        audio_output = "outputs/atlas_response.mp3"
        speak(response_translated,
              language=tts_code,
              filename=audio_output)

        status = f"""
✅ ATLAS Response
─────────────────────────────
{input_method} Input Detected
🌍 Language     : {detected_lang.upper()}
📝 You said     : {original_text}
🔄 In English   : {english_text}
💬 Response     : {response_translated}
─────────────────────────────
        """.strip()

        return status, original_text, response_translated, audio_output

    except Exception as e:
        return f"❌ Error: {str(e)}", "", "", None


with gr.Blocks(
    title="ATLAS AI",
    theme=gr.themes.Soft(),
) as demo:

    gr.HTML("""
        <div style="text-align:center; padding:20px">
            <h1>🌍 ATLAS AI</h1>
            <h3>Offline Multilingual Crisis Assistance System</h3>
            <p>Speak or type in any language — ATLAS understands and responds</p>
        </div>
    """)

    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 🎤 Input")
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="Speak in any language"
            )
            text_input = gr.Textbox(
                label="Or type your message",
                placeholder="Type in any language...",
                lines=3
            )
            target_lang = gr.Dropdown(
                choices=[
                    "Hindi", "Arabic", "Bengali", "Urdu",
                    "French", "German", "Spanish", "Russian",
                    "Turkish", "Swahili", "Tamil", "Telugu",
                    "Marathi", "Gujarati", "Punjabi", "English"
                ],
                value="Hindi",
                label="Respond in language"
            )
            submit_btn = gr.Button(
                "🚀 Send to ATLAS",
                variant="primary",
                size="lg"
            )
            clear_btn = gr.Button(
                "🗑️ Clear",
                variant="secondary"
            )

        with gr.Column(scale=1):
            gr.Markdown("## 📤 Output")
            status_output = gr.Textbox(
                label="ATLAS Status",
                lines=8
            )
            original_output = gr.Textbox(
                label="What you said",
                lines=2
            )
            response_output = gr.Textbox(
                label="ATLAS Response",
                lines=3
            )
            audio_output = gr.Audio(
                label="🔊 Listen to response",
                type="filepath",
                autoplay=True
            )

    gr.Markdown("---")
    gr.Markdown("## 💡 Try these examples")
    gr.Examples(
        examples=[
            [None, "मुझे पानी चाहिए", "English"],
            [None, "I need a doctor", "Hindi"],
            [None, "أحتاج إلى مساعدة", "English"],
            [None, "J'ai besoin d'aide", "Hindi"],
            [None, "Ninahitaji msaada", "English"],
        ],
        inputs=[audio_input, text_input, target_lang],
    )

    gr.Markdown("---")
    gr.HTML("""
        <div style="text-align:center; color:gray; font-size:12px">
            ATLAS AI — B.Tech Final Year Project | AI & ML Department
        </div>
    """)

    submit_btn.click(
        fn=atlas_process,
        inputs=[audio_input, text_input, target_lang],
        outputs=[status_output, original_output,
                 response_output, audio_output]
    )

    clear_btn.click(
        fn=lambda: (None, "", "Hindi", "", "", "", None),
        outputs=[audio_input, text_input, target_lang,
                 status_output, original_output,
                 response_output, audio_output]
    )

if __name__ == "__main__":
    print("=" * 50)
    print("   ATLAS AI — Starting Web Interface")
    print("=" * 50)
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=True,
        show_error=True,
        inbrowser=True
    )
    
    
    
    
    
    
    
    