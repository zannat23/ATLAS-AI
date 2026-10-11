import voiceImg from './assets/voice.jpg';
import medicalImg from './assets/medical.jpg';
import resourcesImg from './assets/resources.jpg';
import { VoiceIllustration, MedicalIllustration, ResourcesIllustration } from './illustrations';

export const API_URL = 'http://localhost:8000';

export const PROJECT_TITLE = 'Offline AI-Based Multilingual Communication, Medical Triage and Resource Assistance System for Crisis Response';

export const EXAMPLES = [
  'मुझे मदद चाहिए',
  'I need a doctor',
  'أحتاج إلى مساعدة',
  "J'ai besoin d'aide",
  'Ninahitaji msaada',
  'मला मदत हवी आहे',
];

export const LANGUAGES = [
  "Hindi", "English", "Bengali", "Urdu", "Tamil", "Telugu", "Marathi", "Gujarati",
  "Punjabi", "Kannada", "Malayalam", "Nepali", "Sinhala", "Odia", "Assamese", "Sindhi", "Pashto",
  "Chinese (Simplified)", "Chinese (Traditional)", "Japanese", "Korean", "Thai", "Vietnamese",
  "Indonesian", "Malay", "Javanese", "Sundanese", "Khmer", "Lao", "Burmese", "Tagalog", "Cebuano", "Hmong",
  "Arabic", "Hebrew", "Persian", "Turkish", "Azerbaijani", "Kazakh", "Uzbek", "Mongolian",
  "Tajik", "Kurdish", "Armenian", "Georgian",
  "French", "German", "Spanish", "Portuguese", "Italian", "Dutch", "Russian", "Ukrainian",
  "Polish", "Czech", "Slovak", "Bulgarian", "Serbian", "Croatian", "Bosnian", "Slovenian",
  "Macedonian", "Romanian", "Hungarian", "Finnish", "Estonian", "Latvian", "Lithuanian",
  "Swedish", "Norwegian", "Danish", "Icelandic", "Greek", "Catalan", "Galician", "Basque",
  "Welsh", "Irish", "Scots Gaelic", "Maltese", "Albanian", "Belarusian", "Luxembourgish",
  "Frisian", "Corsican", "Haitian Creole",
  "Swahili", "Amharic", "Somali", "Hausa", "Yoruba", "Igbo", "Zulu", "Xhosa", "Afrikaans",
  "Sesotho", "Shona", "Kinyarwanda", "Malagasy",
  "Hawaiian", "Maori", "Samoan"
];

// Medical page ke liye: Indian languages included, alphabetical order, sirf wahi
// languages jo translation model (NLLB) support karta hai.
const _MEDICAL_LANGUAGES = [
  // Indian languages
  'Assamese', 'Awadhi', 'Bengali', 'Bhojpuri', 'Chhattisgarhi', 'Gujarati', 'Hindi',
  'Kannada', 'Kashmiri', 'Kashmiri (Devanagari)', 'Magahi', 'Maithili', 'Malayalam',
  'Manipuri (Meitei)', 'Marathi', 'Mizo', 'Nepali', 'Odia', 'Punjabi', 'Sanskrit',
  'Santali', 'Sindhi', 'Tamil', 'Telugu', 'Urdu',
  // South / South-East / East Asia
  'Burmese', 'Cebuano', 'Chinese', 'Chinese (Simplified)', 'Chinese (Traditional)',
  'Filipino', 'Indonesian', 'Japanese', 'Javanese', 'Khmer', 'Korean', 'Lao', 'Malay',
  'Mongolian', 'Sinhala', 'Sundanese', 'Tagalog', 'Thai', 'Tibetan', 'Vietnamese',
  // Middle East / Central Asia / Caucasus
  'Arabic', 'Armenian', 'Azerbaijani', 'Dari', 'Georgian', 'Hebrew', 'Kazakh', 'Kurdish',
  'Kurdish (Kurmanji)', 'Kyrgyz', 'Pashto', 'Persian', 'Tajik', 'Tatar', 'Turkish',
  'Turkmen', 'Uyghur', 'Uzbek',
  // Europe
  'Albanian', 'Basque', 'Belarusian', 'Bosnian', 'Bulgarian', 'Catalan', 'Croatian',
  'Czech', 'Danish', 'Dutch', 'English', 'Esperanto', 'Estonian', 'Finnish', 'French',
  'Galician', 'German', 'Greek', 'Hungarian', 'Icelandic', 'Irish', 'Italian', 'Latvian',
  'Lithuanian', 'Luxembourgish', 'Macedonian', 'Maltese', 'Norwegian', 'Polish',
  'Portuguese', 'Romanian', 'Russian', 'Scots Gaelic', 'Serbian', 'Slovak', 'Slovenian',
  'Spanish', 'Swedish', 'Ukrainian', 'Welsh', 'Yiddish',
  // Africa
  'Afrikaans', 'Amharic', 'Chichewa', 'Hausa', 'Igbo', 'Kinyarwanda', 'Lingala',
  'Malagasy', 'Haitian Creole', 'Oromo', 'Sesotho', 'Shona', 'Somali', 'Swahili',
  'Tigrinya', 'Tswana', 'Wolof', 'Xhosa', 'Yoruba', 'Zulu',
  // Pacific / Americas
  'Fijian', 'Maori', 'Quechua', 'Samoan',
];

// Alphabetical order, duplicates removed
export const MEDICAL_LANGUAGES = [...new Set(_MEDICAL_LANGUAGES)].sort((a, b) => a.localeCompare(b));

export const RESOURCE_TYPES = [
  { id: 'hospital', label: 'Hospital' },
  { id: 'water',    label: 'Water' },
  { id: 'shelter',  label: 'Shelter' },
  { id: 'food',     label: 'Food' },
  { id: 'ngo',      label: 'NGO' },
];

export const MODULES = [
  { path: '/voice',     name: 'Voice Bridge',     desc: 'Real-time multilingual translation', image: voiceImg,     Illustration: VoiceIllustration,     iconKey: 'mic' },
  { path: '/medical',   name: 'Medical Triage',   desc: 'Wound classification & first aid',    image: medicalImg,   Illustration: MedicalIllustration,   iconKey: 'pulse' },
  { path: '/resources', name: 'Resource Locator', desc: 'Find nearby help & shelter',          image: resourcesImg, Illustration: ResourcesIllustration, iconKey: 'pin' },
];

export const NAV_ITEMS = [
  { path: '/voice',     label: 'Voice' },
  { path: '/medical',   label: 'Medical' },
  { path: '/resources', label: 'Resources' },
  { path: '/dashboard', label: 'Dashboard' },
  { path: '/how',       label: 'How it works' },
  { path: '/team',      label: 'Team' },
  { path: '/about',     label: 'About' },
];

export const VOICE_PIPELINE = [
  { name: 'Text or audio input', desc: 'User speaks or types in any language' },
  { name: 'Whisper transcription', desc: 'Audio converted to text, language auto-detected' },
  { name: 'NLLB-200 translation', desc: 'Text translated to English for processing' },
  { name: 'Response generation', desc: 'The system composes a reply in English' },
  { name: 'Translate and speak', desc: 'Reply translated back and read aloud via gTTS' },
];

export const MEDICAL_PIPELINE = [
  { name: 'Wound photo', desc: 'User uploads or captures a wound image' },
  { name: 'Preprocessing', desc: 'Image resized to 224x224 and normalized' },
  { name: 'EfficientNet-B0', desc: 'CNN classifies wound into one of 6 categories' },
  { name: 'Severity mapping', desc: 'Class mapped to a 1-5 severity score' },
  { name: 'First aid output', desc: 'WHO-style first aid instructions returned' },
];

export const RESOURCE_PIPELINE = [
  { name: 'Query or location', desc: 'User types a need or shares GPS location' },
  { name: 'Intent detection', desc: 'Keyword matching maps query to a resource type' },
  { name: 'Database search', desc: 'SQLite lookup filtered by resource type' },
  { name: 'Distance ranking', desc: 'Haversine formula sorts results by distance' },
];

export const TEAM_MEMBERS = [
  { name: 'Zannat', role: 'Lead Developer', meta: 'AI & ML Dept.' },
  { name: 'Zannat', role: 'Backend Developer', meta: 'AI & ML Dept.' },
  { name: 'Zannat', role: 'Frontend Developer', meta: 'AI & ML Dept.' },
];