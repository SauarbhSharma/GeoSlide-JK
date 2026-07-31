import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  metadataBase: new URL('https://geoslide-jk.onrender.com'),
  title: {
    default: 'GeoSlide-JK | Landslide Risk Intelligence',
    template: '%s | GeoSlide-JK',
  },
  description:
    'Machine-learning landslide susceptibility mapping and rainfall-triggered dynamic hazard decision support for Jammu and Kashmir.',
  icons: {
    icon: [
      { url: '/branding/geoslide-jk-icon-32.png', sizes: '32x32', type: 'image/png' },
      { url: '/branding/geoslide-jk-icon-64.png', sizes: '64x64', type: 'image/png' },
    ],
    apple: [
      { url: '/branding/geoslide-jk-icon-180.png', sizes: '180x180', type: 'image/png' },
    ],
    other: [
      { rel: 'icon', url: '/branding/geoslide-jk-icon-192.png', sizes: '192x192', type: 'image/png' },
      { rel: 'icon', url: '/branding/geoslide-jk-icon-512.png', sizes: '512x512', type: 'image/png' },
    ],
  },
  openGraph: {
    title: 'GeoSlide-JK | Landslide Risk Intelligence',
    description:
      'Machine-learning landslide susceptibility mapping and rainfall-triggered dynamic hazard decision support for Jammu and Kashmir.',
    url: 'https://geoslide-jk.onrender.com',
    siteName: 'GeoSlide-JK',
    images: [
      {
        url: '/branding/geoslide-jk-og-image.png',
        width: 1200,
        height: 630,
        alt: 'GeoSlide-JK — Landslide Risk Intelligence',
      },
    ],
    locale: 'en_IN',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'GeoSlide-JK | Landslide Risk Intelligence',
    description:
      'Machine-learning landslide susceptibility mapping and rainfall-triggered dynamic hazard decision support for Jammu and Kashmir.',
    images: ['/branding/geoslide-jk-og-image.png'],
  },
  other: {
    'theme-color': '#0b1329',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-navy-950 text-slate-100 antialiased">{children}</body>
    </html>
  );
}
