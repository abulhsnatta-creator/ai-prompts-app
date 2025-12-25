import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Copy, Globe, Search, Sparkles, Users, Zap } from 'lucide-react'
import './App.css'
const API_URL = 'https://ai-prompts-app.onrender.com';
function App() {
  const [careers, setCareers] = useState([])
  const [selectedCareer, setSelectedCareer] = useState(null)
  const [promptsData, setPromptsData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [language, setLanguage] = useState('ar')
  const [searchTerm, setSearchTerm] = useState('')

  // --- قائمة الأدوات الافتراضية (الحل السحري) ---
  const defaultTools = [
    { name: "ChatGPT", url: "https://chat.openai.com" },
    { name: "Gemini", url: "https://gemini.google.com" },
    { name: "Midjourney", "url": "https://www.midjourney.com" },
    { name: "Bing AI", "url": "https://www.bing.com/chat" },
    { name: "Canva AI", "url": "https://www.canva.com" }
  ];
  // ---------------------------------------------

  const translations = {
    ar: {
      title: 'منصة أوامر الذكاء الاصطناعي للمحترفين',
      subtitle: 'اكتشف مجموعة شاملة من أوامر الذكاء الاصطناعي المصممة خصيصاً لمهنتك',
      searchPlaceholder: 'ابحث عن مهنة...',
      selectCareer: 'اختر مهنتك',
      promptsCount: 'أمر',
      copyPrompt: 'نسخ الأمر',
      suggestedTools: 'أدوات الذكاء الاصطناعي المقترحة',
      backToCareers: 'العودة للمهن',
      features: {
        title: 'لماذا تختار منصتنا؟',
        feature1: { title: 'أوامر متخصصة', description: 'أوامر مصممة خصيصاً لكل مهنة' },
        feature2: { title: 'سهولة الاستخدام', description: 'واجهة بسيطة وسهلة الاستخدام' },
        feature3: { title: 'نسخ سريع', description: 'انسخ الأوامر بنقرة واحدة' }
      }
    },
    en: {
      title: 'AI Prompts Platform for Professionals',
      subtitle: 'Discover a comprehensive collection of AI prompts designed specifically for your profession',
      searchPlaceholder: 'Search for a career...',
      selectCareer: 'Select Your Career',
      promptsCount: 'prompts',
      copyPrompt: 'Copy Prompt',
      suggestedTools: 'Suggested AI Tools',
      backToCareers: 'Back to Careers',
      features: {
        title: 'Why Choose Our Platform?',
        feature1: { title: 'Specialized Prompts', description: 'Prompts designed specifically for each profession' },
        feature2: { title: 'Easy to Use', description: 'Simple and user-friendly interface' },
        feature3: { title: 'Quick Copy', description: 'Copy prompts with one click' }
      }
    }
  }

  const t = translations[language]

  useEffect(() => {
    fetchCareers()
  }, [])

  const fetchCareers = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/api/careers`)
      const data = await response.json()
      if (data.success) {
        setCareers(data.careers)
      }
    } catch (error) {
      console.error('Error fetching careers:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchCareerPrompts = async (careerName) => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/api/careers/${encodeURIComponent(careerName)}/prompts`)
      const data = await response.json()
      if (data.success) {
        setPromptsData(data)
        setSelectedCareer(careerName)
      }
    } catch (error) {
      console.error('Error fetching prompts:', error)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('تم نسخ الأمر!')
  }

  const filteredCareers = careers.filter(career =>
    career.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const toggleLanguage = () => {
    setLanguage(language === 'ar' ? 'en' : 'ar')
    document.documentElement.lang = language === 'ar' ? 'en' : 'ar'
    document.documentElement.dir = language === 'ar' ? 'ltr' : 'rtl'
  }

  const getCurrentPromptsList = () => {
    if (!promptsData) return []
    if (language === 'ar') {
        return promptsData.prompts_ar && promptsData.prompts_ar.length > 0 
               ? promptsData.prompts_ar 
               : promptsData.prompts_en
    }
    return promptsData.prompts_en
  }

  if (selectedCareer && promptsData) {
    const currentList = getCurrentPromptsList()
    
    // المنطق الجديد: استخدم الأدوات القادمة من السيرفر، وإلا استخدم القائمة الافتراضية
    const toolsToDisplay = (promptsData.suggested_ai_tools && promptsData.suggested_ai_tools.length > 0) 
                            ? promptsData.suggested_ai_tools 
                            : defaultTools;

    return (
      <div className={`min-h-screen bg-slate-50 ${language === 'ar' ? 'rtl' : 'ltr'}`} dir={language === 'ar' ? 'rtl' : 'ltr'}>
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-between items-center mb-8">
            <Button onClick={() => setSelectedCareer(null)} variant="outline" className="flex items-center gap-2">
              ← {t.backToCareers}
            </Button>
            <Button onClick={toggleLanguage} variant="outline" size="sm">
              <Globe className="w-4 h-4 mr-2" />
              {language === 'ar' ? 'English' : 'العربية'}
            </Button>
          </div>

          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">{promptsData.career}</h1>
            <p className="text-gray-600">{promptsData.prompt_count} {t.promptsCount}</p>
          </div>

          {/* عرض الأدوات دائماً الآن */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5" />
                {t.suggestedTools}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {toolsToDisplay.map((tool, index) => (
                  <a 
                    key={index} 
                    href={tool.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="no-underline"
                  >
                    <Badge 
                      variant="secondary" 
                      className="hover:bg-blue-100 hover:text-blue-800 cursor-pointer transition-colors px-4 py-2 text-sm flex items-center gap-1"
                    >
                      {tool.name} ↗
                    </Badge>
                  </a>
                ))}
              </div>
            </CardContent>
          </Card>

          <div className="grid gap-4">
            {currentList.map((prompt, index) => (
              <Card key={index} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex justify-between items-start gap-4">
                    <p className="text-gray-700 flex-1 leading-relaxed">{prompt}</p>
                    <Button onClick={() => copyToClipboard(prompt)} size="sm" variant="outline" className="shrink-0">
                      <Copy className="w-4 h-4 mr-2" />
                      {t.copyPrompt}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen bg-slate-50 ${language === 'ar' ? 'rtl' : 'ltr'}`} dir={language === 'ar' ? 'rtl' : 'ltr'}>
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <div className="flex justify-end mb-4">
            <Button onClick={toggleLanguage} variant="outline" size="sm">
              <Globe className="w-4 h-4 mr-2" />
              {language === 'ar' ? 'English' : 'العربية'}
            </Button>
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">{t.title}</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">{t.subtitle}</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <Card className="text-center pt-6">
            <CardHeader>
              <Users className="w-12 h-12 mx-auto text-blue-600 mb-4" />
              <CardTitle>{t.features.feature1.title}</CardTitle>
            </CardHeader>
            <CardContent><CardDescription>{t.features.feature1.description}</CardDescription></CardContent>
          </Card>
          <Card className="text-center pt-6">
            <CardHeader>
              <Zap className="w-12 h-12 mx-auto text-green-600 mb-4" />
              <CardTitle>{t.features.feature2.title}</CardTitle>
            </CardHeader>
            <CardContent><CardDescription>{t.features.feature2.description}</CardDescription></CardContent>
          </Card>
          <Card className="text-center pt-6">
            <CardHeader>
              <Copy className="w-12 h-12 mx-auto text-purple-600 mb-4" />
              <CardTitle>{t.features.feature3.title}</CardTitle>
            </CardHeader>
            <CardContent><CardDescription>{t.features.feature3.description}</CardDescription></CardContent>
          </Card>
        </div>

        <div className="max-w-md mx-auto mb-8 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder={t.searchPlaceholder}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div className="mb-8">
          <h2 className="text-3xl font-bold text-center mb-8">{t.selectCareer}</h2>
          {loading ? (
            <div className="text-center">جاري التحميل...</div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredCareers.map((career, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow cursor-pointer" onClick={() => fetchCareerPrompts(career.name)}>
                  <CardHeader>
                    <CardTitle className="text-lg">{career.name}</CardTitle>
                    <CardDescription>{career.prompt_count} {t.promptsCount}</CardDescription>
                  </CardHeader>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
