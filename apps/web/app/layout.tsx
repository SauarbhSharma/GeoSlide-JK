import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'GeoSlide J&K | Landslide Risk Prediction & Decision Support',
  description: 'Explainable landslide susceptibility and rainfall-triggered risk decision-support platform for Jammu and Kashmir',
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
