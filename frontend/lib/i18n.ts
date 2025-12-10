import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      appName: 'iliketohave',
      heroTitleLine1: 'Collect, share &',
      heroTitleHighlight: 'never forget what you want.',
      heroSubtitle:
        "iliketohave keeps all your wishes in one beautiful place. Create wishlists, share them with friends and family, and track what you've already received.",
      heroCta: 'Login or Register',
      heroNote: "No spam. Just a simple way to share what you'd love to have.",
    },
  },
  fa: {
    translation: {
      appName: 'iliketohave',
      heroTitleLine1: 'جمع کن، به اشتراک بگذار و',
      heroTitleHighlight: 'هیچ‌وقت چیزهایی که می‌خوای رو فراموش نکن.',
      heroSubtitle:
        'iliketohave همه‌ی خواسته‌هات رو یک‌جا نگه می‌داره. لیست آرزو بساز، با بقیه به اشتراک بذار و چیزهایی که گرفتی رو پیگیری کن.',
      heroCta: 'ورود یا ثبت‌نام',
      heroNote:
        'بدون اسپم؛ فقط یک راه ساده برای به اشتراک گذاشتن چیزهایی که دوست داری داشته باشی.',
    },
  },
};

if (!i18n.isInitialized) {
  i18n.use(initReactI18next).init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });
}

export default i18n;